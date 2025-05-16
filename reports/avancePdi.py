import pandas as pd
import os

def generarReporteAvancePdi(conexion, anomat, numper):
    cursor = conexion.cursor()
    cursor.execute("""
            SELECT DISTINCT m.grupo, i.nominse, i.codinse
            FROM almatric m
            JOIN prinstit i ON m.codfac = i.codinse
        """)
    grupos = cursor.fetchall()

    for grupo, nominse, codinse in grupos:
        print(f"Generando reporte para {nominse} - {grupo}...")

        cursor.execute("""
                    SELECT 
                        a.codalu,
                        CONCAT(a.apelli, ' ', a.nombre) AS estudiante,
                        cur.nomcur AS materia,
                        tem.descri AS tema,
                        act.activi,
                        CASE 
                            WHEN p.codevidencia IS NOT NULL AND p.codevidencia <> '' THEN 'Sí'
                            ELSE 'No'
                        END AS tiene_evidencia,
                        c.feccre AS fecha_evidencia,
                        p.porava,
                        CASE 
                            WHEN p.indseg = 'S' THEN 'Sí'
                            ELSE 'No'
                        END AS finalizada
                    FROM alplades p
                    JOIN aldatbas a ON a.codalu = p.codalu
                    JOIN almatric m ON m.codalu = a.codalu AND m.anomat = p.anomat AND m.numper = p.numper AND p.codcur = m.codcur
                    JOIN prcursos cur ON p.codcur = cur.codcur
                    JOIN prtemas tem ON p.codtem = tem.codtem
                    JOIN prtemact act ON p.codtem = act.codtem AND p.nrosec = act.nrosec
                    LEFT JOIN (
                        SELECT codevidencia, MAX(feccre) AS feccre, codusuario
                        FROM coversiones
                        GROUP BY codevidencia, codusuario
                    ) c ON p.codevidencia = c.codevidencia AND a.codalu = c.codusuario
                    WHERE m.grupo = %s
                    AND m.codfac = %s
                    AND p.anomat = %s
                    AND p.numper = %s
                    AND act.estado = 'A'
                    ORDER BY a.codalu, tem.descri;
                    """, (grupo, codinse, anomat, numper))
        
        resultados = cursor.fetchall()
        columnas = ['Código del estudiante', 'Nombre del estudiante', 'Materia', 'Tema', 'Descripción de la actividad', '¿Tiene evidencia?', 'Fecha en la que subió la evidencia', 'Porcentaje de avance', '¿Actividad finalizada?']

        if resultados:
            df = pd.DataFrame(resultados, columns=columnas)
            carpeta = f"reports/outputs/{nominse.replace(' ', '_').replace('/', '-')}"
            os.makedirs(carpeta, exist_ok=True)
            nombre_archivo = f"{nominse.replace(' ', '_').replace('/', '-')}_{grupo}_avance_PDI.xlsx"
            ruta_archivo = os.path.join(carpeta, nombre_archivo)
            df.to_excel(ruta_archivo, index=False)
            print(f"Reporte guardado: {ruta_archivo}")
        else:
            print(f"No hay datos para {nominse}-{grupo}")
    cursor.close()