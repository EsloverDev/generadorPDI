from dotenv import load_dotenv
from db.conexion import obtenerConexion
from logic.calculador import notasPorTema
from logic.generador import generarPdi

load_dotenv()

if __name__ == "__main__":
    anomat = 2025
    numper = 'P1'
    codeva = '10'
    nroopo = 2

    print("Calculando notas por tema...\n")
    conexion = obtenerConexion()

    if conexion:
        resultados = notasPorTema(anomat, numper, codeva, nroopo)
        for r in resultados:
            print(f"Estudiante: {r['codalu']} | Curso: {r['codcur']} | Oportunidad: {r['nroopo']} | Código de la evaluación: {r['codeva']} Tema: {r['codtem']} | Aciertos: {r['aciertos']}/{r['total_preguntas']} | Nota: {r['nota']}")

        print("\nGenerando actividades del PDI...")
        generarPdi(conexion, resultados)
        conexion.close()
