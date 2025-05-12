from db.conexion import obtenerConexion
import psycopg2.extras

"""Calcula la nota obtenida por cada estudiante en cada tema evaluado, basándose en las preguntas acertadas y la cantidad total de preguntas por tema"""
def notasPorTema(anomat, numper, codeva, nroopo=2):
    try:
        conexion = obtenerConexion()
        cursor = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """
            SELECT 
                a.codalu,
                a.codcur,
                a.anomat,
                a.numper,
                a.codeva,
                a.nroopo,
                p.codtem,
                COUNT(*) FILTER (WHERE a.estres = 'A') AS correctas,
                COUNT(*) AS total_preguntas,
                ROUND(50.0 / COUNT(*) * COUNT(*) FILTER (WHERE a.estres = 'A'), 2) AS nota
            FROM 
                aldeteva a
            JOIN 
                evpregun p ON a.codpre = p.codpre
            where
                a.anomat = %s and
                a.numper = %s and
                a.codeva = %s and
                a.nroopo = %s AND
                p.estpre = 'A'
            GROUP BY 
                a.codalu, a.codcur, a.anomat, a.numper, a.codeva, a.nroopo, p.codtem
            """
        cursor.execute(query, (anomat, numper, codeva, nroopo))
        resultados = cursor.fetchall()
        notas = []
        for fila in resultados:
            notas.append({
                "codalu": fila["codalu"],
                "codcur": fila["codcur"],
                "anomat": fila["anomat"],
                "numper": fila["numper"],
                "codeva": fila["codeva"],
                "nroopo": fila["nroopo"],
                "codtem": fila["codtem"],
                "aciertos": fila["correctas"],
                "total_preguntas": fila["total_preguntas"],
                "nota": fila["nota"]
            })
        cursor.close()
        conexion.close()
        return notas
    except Exception as e:
        print(f"Error al calcular notas por tema: {e}")
        return []