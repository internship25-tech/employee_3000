import os
import pandas as pd
import logging

EXTRACT_DIR = "extracted"
OUTPUT_DIR = "output"

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

        # Rename EEID → Employee ID
        if "EEID" in df.columns:
            df["Employee ID"] = df["EEID"]

        # Split Full Name into First Name and Last Name
        if "Full Name" in df.columns:
            df[["First Name", "Last Name"]] = df["Full Name"].str.split(" ", n=1, expand=True)

        # Add placeholder Email and Phone Number
        if "Email" not in df.columns:
            df["Email"] = "unknown@example.com"
        if "Phone Number" not in df.columns:
            df["Phone Number"] = "0000000000"

        # Check required fields
        missing = [field for field in REQUIRED_FIELDS if field not in df.columns]
        if missing:
            logging.error(f"Missing required fields: {missing}")
            return

        # Export to CSV
        output_path = os.path.join(OUTPUT_DIR, "processed_employees.csv")
        df[REQUIRED_FIELDS].to_csv(output_path, index=False)
        logging.info(f"Processed data written to: {output_path}")
        print("✔️ Processed data saved to:", output_path)

    except Exception as e:
        logging.error(f"Error processing Excel file: {e}")
