import pandas as pd
import os

def obtenerInstitucionesYCursos(conexion):
    cursor = conexion.cursor()
    query = """
        SELECT DISTINCT i.codinse, c.codcur
        FROM alctreva a
        JOIN almatric m ON a.codalu = m.codalu AND a.codcur = m.codcur
        JOIN prinstit i ON m.codfac = i.codinse
        JOIN prcursos c ON m.codcur = c.codcur
        WHERE a.noteva IS NOT NULL
        ORDER BY i.codinse, c.codcur
    """
    cursor.execute(query)
    return cursor.fetchall()

def generarReporteRespuestas(conexion, anomat, numper, codeva, codcur, codinse):
    cursor = conexion.cursor()
    query = """
        SELECT 
            a.codalu,
            b.apelli || ' ' || b.nombre AS estudiante,
            i.nominse AS institucion,
            m.grupo,
            c.nomcur AS materia,
            a.nroopo,
            a.codpre,
            a.opcion,
            r.vlropc
        FROM aldeteva a
        JOIN aldatbas b ON a.codalu = b.codalu
        JOIN almatric m ON a.codalu = m.codalu AND a.codcur = m.codcur AND m.anomat = a.anomat AND m.numper = a.numper
        JOIN prinstit i ON m.codfac = i.codinse
        JOIN prcursos c ON a.codcur = c.codcur
        JOIN evressel r ON a.codpre = r.codpre AND a.opcion = r.opcion
        WHERE 
            a.anomat = %s AND
            a.numper = %s AND
            a.codeva = %s AND
            a.codcur = %s AND
            i.codinse = %s AND
            a.nroopo = 2
        ORDER BY a.codalu, a.codpre
    """
    cursor.execute(query, (anomat, numper, codeva, codcur, codinse))
    datos = cursor.fetchall()
    if not datos:
        print(f"No hay respuestas para el curso {codcur} en la institución {codinse}")
        return
    
    estudiantes = {}
    for row in datos:
        codalu, estudiante, institucion, grupo, materia, nroopo, codpre, opcion, vlropc = row
        clave = (codalu, estudiante, institucion, grupo, materia, nroopo)
        if clave not in estudiantes:
            estudiantes[clave]={}
        resultado = f"{opcion} - {'Correcta' if vlropc == 1 else 'Incorrecta'}"
        estudiantes[clave][codpre] = resultado

    columnas_codpre = sorted({row[6] for row in datos})
    filas = []
    for clave, respuestas in estudiantes.items():
        fila = list(clave)
        for codpre in columnas_codpre:
            fila.append(respuestas.get(codpre, ""))
        filas.append(fila)
    
    columnas = ["Código del alumno", "Estudiante", "Institución", "Grupo", "Materia", "Oportunidad"] + columnas_codpre
    df = pd.DataFrame(filas, columns= columnas)
    carpeta = "reports/outputs/comparar_respuestas"
    os.makedirs(carpeta, exist_ok=True)
    nombre_archivo = os.path.join(carpeta, f"respuestas_{institucion.replace(' ', '_').replace('/', '-')}_{materia.replace('SABER 11 ', '').replace(' ', '_')}.xlsx")
    df.to_excel(nombre_archivo, index=False)
    print(f"\nReporte generado: {nombre_archivo}")
