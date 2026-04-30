import sys

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

    failed_modules = []
    modules = [
        ("Contratos", talana_contratos),
        ("Ausentismo", talana_ausentismo),
        ("Vacaciones", talana_vacaciones),
        ("Liquidaciones", talana_liquidaciones),
        #("Firmas", talana_firmas),
        ("Marcaciones", talana_marcaciones),
        ("Centralización", talana_centralizacion),
        ("Bases", talana_bases),
    ]

    for name, module in modules:
        try:
            print(f"▶ Procesando módulo: {name}")
            module.procesar()
        except Exception as e:
            print(f"❌ Error en módulo '{name}': {e}")
            failed_modules.append(name)
        else:
            print(f"✅ Módulo '{name}' procesado correctamente")

    if failed_modules:
        print(f"\n❌ Error Crítico: La ejecución finalizó con fallos en: {', '.join(failed_modules)}")
        sys.exit(1)

    print("\n=== Proceso global finalizado con éxito ===")

if __name__ == "__main__":
    main()