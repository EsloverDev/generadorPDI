from dotenv import load_dotenv
from db.conexion import obtenerConexion
from logic.calculador import notasPorTema
from logic.generador import generarPdi
from reports.respuestas import generarReporteRespuestas, obtenerInstitucionesYCursos
from reports.comparativo import generarReporteComparativo

load_dotenv()

def menu():
    print("\nSelecciona una opción:")
    print("\n1. Generar informes de respuestas.\n2. Calcular notas por tema y generar PDI.\n3. Generar reporte comparativo.\n4. Salir")
    return input("Opción: ")

if __name__ == "__main__":
    anomat = 2025
    numper = 'P1'
    codeva = '10'
    nroopo = 2

    opcion = menu()
    conexion = obtenerConexion()
    
    if conexion:
        if opcion == '1':
            combinaciones = obtenerInstitucionesYCursos(conexion)
            print(f"Generando {len(combinaciones)} reportes...\n")

            for codinse, codcur in combinaciones:
                print(f"Generando reporte para institución {codinse} y curso {codcur}")
                generarReporteRespuestas(conexion, anomat, numper, codeva, codcur, codinse)
        elif opcion == '2':
            print("Calculando notas por tema...\n")
            resultados = notasPorTema(anomat, numper, codeva, nroopo)
            for r in resultados:
                print(f"Estudiante: {r['codalu']} | Curso: {r['codcur']} | Oportunidad: {r['nroopo']} | Código de la evaluación: {r['codeva']} Tema: {r['codtem']} | Aciertos: {r['aciertos']}/{r['total_preguntas']} | Nota: {r['nota']}")

            print("\nGenerando actividades del PDI...")
            generarPdi(conexion, resultados)
        elif opcion == '3':
            generarReporteComparativo(conexion, 2025, 'P1')
        else:
            print("Saliendo...")
        conexion.close()
