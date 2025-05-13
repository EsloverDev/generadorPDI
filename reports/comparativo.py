import pandas as pd
import os

def generarReporteComparativo(conexion, anomat, numper):
    cursor = conexion.cursor()
    materias = {
        'FX0075': 'Matemáticas',
        'FX0076': 'Lenguaje',
        'FX0077': 'Sociales',
        'FX0078': 'Ciencias',
        'FX0079': 'Inglés'
    }

    cursor.execute("SELECT codinse, nominse FROM prinstit ORDER BY nominse")
    instituciones = cursor.fetchall()

    for codinse, nominse in instituciones:
        print(f"Generando reporte para: {nominse}")

        cursor.execute(f"""
                SELECT
                    a.codalu,
                    b.apelli || ' ' || b.nombre AS estudiante,
                    m.grupo,
                    a.codcur,
                    a.nroopo,
                    a.noteva
                FROM alctreva a
                JOIN aldatbas b ON a.codalu = b.codalu
                JOIN almatric m ON a.codalu = m.codalu AND a.codcur = m.codcur
                JOIN prinstit p ON m.codfac = p.codinse
                WHERE a.anomat = %s AND a.numper = %s AND a.codcur IN %s AND a.noteva IS NOT NULL AND p.codinse = %s
            """, (anomat, numper, tuple(materias.keys()), codinse))
        filas = cursor.fetchall()

        if not filas:
            print(f"No hay datos para {nominse}")
            return

        estudiantes = {}
        for codalu, estudiante, grupo, codcur, nroopo, noteva in filas:
            clave = (codalu, estudiante, grupo)
            if clave not in estudiantes:
                estudiantes[clave] = {
                    "1P": {},
                    "2P": {}
                }
            if nroopo == 1:
                estudiantes[clave]["1P"][codcur] = noteva
            elif nroopo == 2:
                estudiantes[clave]["2P"][codcur] = noteva
        
        data = []
        for clave, notas in estudiantes.items():
            fila = list(clave)
            total_1p = 0
            count_1p = 0
            for codcur in materias:
                nota = notas["1P"].get(codcur, "")
                fila.append(nota)
                if isinstance(nota, (int, float)):
                    total_1p += nota
                    count_1p += 1
            promedio_1p = round(total_1p / count_1p, 1) if count_1p > 0 else ""
            fila.append(promedio_1p)

            total_2p = 0
            count_2p = 0
            for codcur in materias:
                nota = notas["2P"].get(codcur, "")
                fila.append(nota)
                if isinstance(nota, (int, float)):
                    total_2p += nota
                    count_2p += 1
            promedio_2p = round(total_2p / count_2p, 1) if count_2p > 0 else ""
            fila.append(promedio_2p)
            data.append(fila)
        
        columnas = ["Código del alumno", "Estudiante", "Grupo"]
        columnas += [f"{nombre}" for nombre in materias.values()] + ["Promedio 1P"]
        columnas += [f"{nombre}" for nombre in materias.values()] + ["Promedio 2P"]

        carpeta = "reports/outputs/comparativo_resultados"
        os.makedirs(carpeta, exist_ok=True)
        df = pd.DataFrame(data, columns = columnas)
        nombre_archivo = f"{nominse.replace(' ', '_').replace('/', '-')}.xlsx"
        ruta = os.path.join(carpeta, nombre_archivo)
        df.to_excel(ruta, index=False)
        print(f"\nReporte generado: {ruta}")