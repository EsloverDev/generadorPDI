import pandas as pd

def generarReporteRespuestas(conexion, anomat, numper, codeva):
    query = """
        SELECT 
            e.codalu,
            db.apelli || ' ' || db.nombre AS estudiante,
            inst.nominse AS institucion,
            m.grupo,
            e.codcur,
            e.codeva,
            e.nroopo,
            e.codpre,
            e.opcion,
            p.opcsal AS opcion_correcta,
            CASE 
                WHEN e.opcion = p.opcsal THEN 1
                ELSE 0
            END AS acierto
        FROM aldeteva e
        JOIN evpregun p ON e.codpre = p.codpre
        JOIN aldatbas db ON e.codalu = db.codalu
        JOIN almatric m ON e.codalu = m.codalu AND e.codcur = m.codcur
        JOIN prinstit inst ON m.codfac = inst.codinse
        WHERE 
            e.anomat = %s AND
            e.numper = %s AND
            e.codeva = %s AND
            e.nroopo = 1
        ORDER BY e.codalu, e.codpre
    """
    df = pd.read_sql_query(query, conexion, params=(anomat, numper, codeva))

    output_path = "reports/outputs/respuestas_evaluacion.xlsx"
    df.to_excel(output_path, index=False)
    print(f"\nReporte exportado a: {output_path}")
