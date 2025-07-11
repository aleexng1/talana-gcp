✅ README.md
markdown
Copiar
Editar
# Talana GCP Integration

Automatización del proceso de extracción de datos desde la API de Talana, transformación y carga en Google Cloud (BigQuery y Cloud Storage), listo para ejecución en entornos automatizados como Cloud Run Jobs o Cloud Scheduler.

---

## 📦 Estructura del Proyecto

TALANA-GCP/
├── src/
│ ├── main.py # Punto de entrada principal
│ ├── config.py # Variables y configuración global
│ └── utils/ # Módulos reutilizables y específicos por endpoint
│ ├── auth.py
│ ├── fetch.py
│ ├── sanitize.py
│ ├── storage.py
│ ├── dates.py
│ ├── talana_*.py
├── .env # Variables de entorno (local)
├── requirements.txt # Dependencias del proyecto
├── Dockerfile # (opcional) Imagen para ejecución en Cloud Run Job

yaml
Copiar
Editar

---

## ⚙️ Variables de entorno

Define estas variables en un archivo `.env` o como variables de entorno en Cloud Run Job:

```env
TALANA_USERNAME=correo@empresa.cl
TALANA_PASSWORD=clave_de_api
GCP_PROJECT_ID=mi-proyecto
GCP_BUCKET_NAME=nombre-del-bucket
GOOGLE_APPLICATION_CREDENTIALS=/ruta/credenciales.json  # Solo en local
🚀 Ejecución local
Crear entorno virtual:

bash
Copiar
Editar
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
Instalar dependencias:

bash
Copiar
Editar
pip install -r requirements.txt
Ejecutar desde raíz del proyecto:

bash
Copiar
Editar
python -m src.main
🐳 Ejecución como Docker Job (opcional)
Crear imagen Docker:

bash
Copiar
Editar
docker build -t talana-job .
Ejecutar localmente:

bash
Copiar
Editar
docker run --env-file .env talana-job
Subir a Artifact Registry y ejecutar como Cloud Run Job (ver documentación GCP).

📌 Módulos disponibles
talana_contratos

talana_ausentismo

talana_vacaciones

talana_liquidaciones

talana_firmas

talana_marcaciones

talana_centralizacion

talana_bases

Cada módulo puede ejecutarse individualmente o en conjunto desde main.py.

✅ Estado del Proyecto
 Modularización por endpoint

 Refactor con funciones reutilizables

 Logging unificado

 Preparado para Docker y Cloud Run Jobs

 Validación de esquema BigQuery (próximamente)

 Tests automáticos (próximamente)

📫 Contacto
Proyecto desarrollado por Alex Andrés Nail Gallardo para Dimarsa
📧 alex.nail@dimarsa.cl