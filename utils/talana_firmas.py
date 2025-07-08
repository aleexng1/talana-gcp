import os
import requests
import json
from google.cloud import storage
from datetime import datetime, timedelta
import re
import unicodedata
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dotenv import load_dotenv
load_dotenv()

# Configuration
USERNAME = os.getenv("TALANA_USERNAME")
PASSWORD = os.getenv("TALANA_PASSWORD")
PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'dimarh')
BUCKET_NAME = os.getenv('GCP_BUCKET_NAME', 'talana_bases')


# Configuración de logging
logging.basicConfig(level=logging.INFO)

def get_session_with_retries():
    """Get a requests session with retry logic."""
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504]
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def get_auth_token(username, password):
    """Fetch authentication token from the server."""
    url = "https://talana.com/es/api/api-token-auth/"
    session = get_session_with_retries()
    try:
        logging.info(f"Fetching authentication token from {url}")
        response = session.post(url, json={"username": username, "password": password}, timeout=500)
        response.raise_for_status()
        logging.info("Authentication token fetched successfully")
        return response.json()["token"]
    except requests.RequestException as e:
        logging.error(f"Error occurred while fetching authentication token: {e}")
        return None

def fetch_data(url, token):
    """Fetch data from the given URL using the provided token."""
    results = []
    session = get_session_with_retries()
    while url:
        try:
            logging.info(f"Fetching data from URL: {url}")
            response = session.get(url, headers={"Authorization": f"Token {token}"}, timeout=500)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                results.extend(data)
                break
            else:
                results.extend(data.get('results', []))
                url = data.get('next')
        except requests.RequestException as e:
            logging.error(f"Error occurred while fetching data from {url}: {e}")
            break
    logging.info(f"Data fetched successfully from URL: {url}")
    return results

def remove_user_defined_fields(data):
    """Remove user defined fields and sanitize the data."""
    if isinstance(data, dict):
        data.pop("user_defined_fields", None)
        rename_duplicate_sueldo_mensual(data)
        keys_to_update = list(data.keys())
        for key in keys_to_update:
            new_key = sanitize_field_name(key)
            if new_key != key:
                data[new_key] = data.pop(key)
            remove_user_defined_fields(data[new_key])
    elif isinstance(data, list):
        for item in data:
            remove_user_defined_fields(item)

def sanitize_field_name(name):
    """Sanitize field names according to Google Cloud Storage specifications."""
    name = unicodedata.normalize('NFC', name)
    name = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    name = name.replace("ñ", "n")
    special_chars = {
        '!': '\u0021', '"': '\u0022', '$': '\u0024', '(': '\u0028', ')': '\u0029', '*': '\u002A',
        ',': '\u002C', '.': '\u002E', '/': '\u002F', ';': '\u003B', '?': '\u003F', '@': '\u0040',
        '[': '\u005B', '\\': '\u005C', ']': '\u005D', '^': '\u005E', '`': '\u0060', '{': '\u007B',
        '}': '\u007D', '~': '\u007E', '°': ''
    }
    for char, replacement in special_chars.items():
        name = name.replace(char, '_')
    name = re.sub(r'[^\w_]', '', name)
    if name and name[0].isdigit():
        name = '_' + name
    return name[:300]

def rename_duplicate_sueldo_mensual(data):
    if isinstance(data, dict):
        lower_case_keys = {k.lower(): k for k in data.keys()}
        if 'sueldo mensual' in lower_case_keys and 'sueldo mensual' in lower_case_keys:
            original_key = lower_case_keys['sueldo mensual']
            new_key = 'Sueldo_mensual_duplicated'
            while new_key in data:
                new_key += '_1'
            data[new_key] = data.pop(original_key)
        for key, value in data.items():
            rename_duplicate_sueldo_mensual(value)

def write_to_ndjson(data, filename):
    """Write data to an NDJSON file."""
    logging.info(f"Writing data to file: {filename}")
    with open(filename, "w", encoding="utf-8") as json_file:
        for item in data:
            remove_user_defined_fields(item)
            json.dump(item, json_file, ensure_ascii=False)
            json_file.write("\n")
    logging.info(f"Data written to file: {filename} successfully")

def upload_to_gcs(local_filename, bucket_name, remote_filename):
    """Upload a local file to Google Cloud Storage."""
    logging.info(f"Uploading file to GCS: {remote_filename}")
    client = storage.Client(project=PROJECT_ID)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(remote_filename)
    blob.upload_from_filename(local_filename)
    logging.info(f"{remote_filename} uploaded to {bucket_name} successfully.")

def process_data(username, password, url, output_filename, remote_filename):
    """Process data from the given URL and upload it to GCS."""
    logging.info(f"Processing endpoint: {url}")
    token = get_auth_token(username, password)
    if not token:
        logging.error(f"Failed to get auth token for {url}")
        return
    data = fetch_data(url, token)
    if not data:
        logging.error(f"No data fetched for {url}")
        return
    write_to_ndjson(data, output_filename)
    upload_to_gcs(output_filename, BUCKET_NAME, remote_filename)
    logging.info(f"Processed endpoint: {url}")

def get_yesterday_date():
    """Get yesterday's date in YYYY-MM-DD format."""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def get_last_month():
    """Get the last month and year."""
    today = datetime.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)
    return last_month.strftime('%Y'), last_month.strftime('%m')

def main(data, context=None):
    """Main function to process data from endpoints and upload to GCS."""
    yesterday = get_yesterday_date()
    last_year, last_month = get_last_month()
    
    endpoints = [
        #Firmas
        ("https://talana.com/es/api/integration-signature-requests", "Firmas_output.ndjson", "Firmas.ndjson"),
    ]

    for url, output_filename, remote_filename in endpoints:
        logging.info(f"Starting processing for endpoint: {url}")
        try:
            process_data(USERNAME, PASSWORD, url, output_filename, remote_filename)
        except Exception as e:
            logging.error(f"Error processing {url}: {e}")
        logging.info(f"Finished processing for endpoint: {url}")

    logging.info("All endpoints processed")

def procesar():
    """Función de entrada para main.py"""
    logging.info("=== Ejecutando talana_firmas.procesar() ===")
    main(data=None)
