import os
import pandas as pd
import logging

EXTRACT_DIR = "extracted"
OUTPUT_DIR = "output"

# Ensure logs directory exists before logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename='logs/processing.log', level=logging.INFO)

REQUIRED_FIELDS = ["Employee ID", "First Name", "Last Name", "Email", "Job Title", "Phone Number", "Hire Date"]

def find_excel_file(directory):
    for file in os.listdir(directory):
        if file.endswith((".xlsx", ".xls")):
            return os.path.join(directory, file)
    return None

def process_employee_data():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    excel_path = find_excel_file(EXTRACT_DIR)
    if not excel_path:
        logging.error("No Excel file found in extracted data.")
        return

    try:
        df = pd.read_excel(excel_path)

        # Validate required fields
        missing = [field for field in REQUIRED_FIELDS if field not in df.columns]
        if missing:
            logging.error(f"Missing required fields: {missing}")
            return

        output_path = os.path.join(OUTPUT_DIR, "processed_employees.csv")
        df[REQUIRED_FIELDS].to_csv(output_path, index=False)
        logging.info(f"Processed data written to: {output_path}")
    except Exception as e:
        logging.error(f"Error processing Excel file: {e}")
