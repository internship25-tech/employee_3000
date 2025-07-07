import os
import zipfile
import requests
import json
import logging

EXTRACT_DIR = "extracted"
ZIP_FILE_PATH = os.path.join(EXTRACT_DIR, "employee_data.zip")

# Ensure logs directory exists before logging setup
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename='logs/scraper.log', level=logging.INFO)

def download_zip_file(url, dest_path):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info("ZIP file downloaded successfully.")
        return True
    except Exception as e:
        logging.error(f"Failed to download ZIP file: {e}")
        return False

def extract_zip_file(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        logging.info("ZIP file extracted successfully.")
        return True
    except zipfile.BadZipFile as e:
        logging.error(f"Invalid ZIP file: {e}")
        return False

def run_scraper():
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    # Correct path to scraper.json inside src/
    config_path = os.path.join(os.path.dirname(__file__), "src", "scraper.json")

    if not os.path.exists(config_path):
        logging.error(f"Config file not found at {config_path}")
        return

    with open(config_path, "r") as f:
        config = json.load(f)

    url = config.get("employee_zip_url")
    if not url:
        logging.error("No URL found in scraper.json.")
        return

    if download_zip_file(url, ZIP_FILE_PATH):
        extract_zip_file(ZIP_FILE_PATH, EXTRACT_DIR)
