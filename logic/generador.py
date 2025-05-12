import random
from recolector import actividadYaAsignada

def insertarActividad(cursor, codalu, codcur, anomat, numper, codeva, nroopo, codtem, nrosec):
    cursor.execute("""
        INSERT INTO alplades (
            codalu, codcur, anomat, numper, codeva, nroopo, codtem, nrosec, fecgen, fecobj, forgen, loggen, porava, fecseg, indseg, logseg, coment, feclim, codevidencia
        )VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, '2025.05.12', '2025.06.08', 'A', '1188964953', 0, NULL, 'N', NULL, '', '2025.06.08', ''
        )
        """, (codalu, codcur, anomat, numper, codeva, nroopo, codtem, nrosec))

def generarPdi(conexion, resultados):
    cursor = conexion.cursor()
    insertados = 0
    for r in resultados:
        if r["nota"] < 30:
            codalu = r["codalu"]
            codcur = r["codcur"]
            anomat = r["anomat"]
            numper = r["numper"]
            codeva = r["codeva"]
            nroopo = r["nroopo"]
            codtem = r["codtem"]
            cursor.execute(
                """
                SELECT nrosec
                FROM prtemact
                WHERE codtem = %s AND estado = 'A'
            """, (codtem,))
            actividades = cursor.fetchall()
            if actividades:
                actividadSeleccionada = random.choice(actividades)[0]
                if not actividadYaAsignada(cursor, codalu, codcur, anomat, numper, codeva, nroopo, codtem, actividadSeleccionada):
                    try:
                        insertarActividad(cursor, codalu, codcur, anomat, numper, codeva, nroopo, codtem, actividadSeleccionada)
                        insertados += 1
                    except Exception as e:
                        print(f"Error al insertar actividad para {codalu} - {codtem}: {e}")
                else:
                    print(f"No hay actividades activas para el tema {codtem}")
    conexion.commit()
    print(f"\nActividades asignadas: {insertados}")

