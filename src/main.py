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

    modules = [
        ("Contratos", talana_contratos),
        ("Ausentismo", talana_ausentismo),
        ("Vacaciones", talana_vacaciones),
        ("Liquidaciones", talana_liquidaciones),
        ("Firmas", talana_firmas),
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
        else:
            print(f"✅ Módulo '{name}' procesado correctamente")

    print("=== Proceso global finalizado ===")

if __name__ == "__main__":
    main()