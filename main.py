# main.py

from utils import (
    talana_contratos,
    talana_ausentismo,
    talana_vacaciones,
    talana_liquidaciones,
    talana_firmas,
    talana_marcaciones,
    talana_centralizacion,
    talana_bases
)

def main():
    print("=== Iniciando ejecución del Job Talana ===")

    # Llama solo los módulos que quieras ejecutar en esta corrida
    talana_contratos.procesar()
    #talana_ausentismo.procesar()
    #talana_vacaciones.procesar()
    #talana_liquidaciones.procesar()
    #talana_firmas.procesar()
    #talana_marcaciones.procesar()
    #talana_centralizacion.procesar()
    #talana_bases.procesar()

    print("=== Proceso finalizado correctamente ===")

if __name__ == "__main__":
    main()