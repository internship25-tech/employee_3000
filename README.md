#  Employee Data ZIP Scraper & Processor

This Python-based pipeline automates the downloading, extraction, validation, and transformation of employee data provided in a ZIP file (containing Excel sheets). It is designed to support automated ingestion and cleaning workflows for HR or data analytics use.

---

##  Overview

The project is split into two main components:

- **Ingestion**: Downloads a ZIP file containing employee data and extracts it.
- **Processing**: Parses the extracted Excel file, validates required fields, and exports cleaned data as CSV.

---

##  Project Structure

```
employee_3000/
├── ingestion/
│   ├── main_scraper.py        # Entry point to run the scraper
│   ├── run_scraper.py         # Logic for downloading and extracting the ZIP
│   └── src/
│       └── scraper.json       # Configuration file with ZIP URL
├── processing/
│   ├── main_processor.py      # Entry point to run the processor
│   └── processing.py          # Logic to process the extracted Excel file
├── logs/                      # Logging output for traceability
├── extracted/                 # Extracted Excel files from ZIP
├── output/                    # Final cleaned CSV output
└── README.md                  # Project documentation
```

---

## 🔧 Configuration

Edit the ZIP file URL in: `ingestion/src/scraper.json`

```json
{
  "employee_zip_url": "https://www.thespreadsheetguru.com/wp-content/uploads/2022/12/EmployeeSampleData.zip"
}
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/employee-data-pipeline.git
cd employee-data-pipeline
```

### 2. Install Required Packages

```bash
pip install pandas openpyxl requests
```

---

##  How to Run the Pipeline

### Step 1: Download & Extract ZIP

```bash
python ingestion/main_scraper.py
```

- Downloads the ZIP from the configured URL
- Extracts the Excel file into `extracted/`
- Logs actions to `logs/scraper.log`

### Step 2: Process Extracted Data

```bash
python processing/main_processor.py
```

- Validates required fields in Excel
- Exports `processed_employees.csv` to `output/`
- Logs issues to `logs/processing.log`



##  Required Fields

The processor expects the following columns in the Excel sheet:

- `Employee ID`
- `First Name`
- `Last Name`
- `Email`
- `Job Title`
- `Phone Number`
- `Hire Date`

Missing any of these fields will result in a logged error.



##  Output

-  Cleaned data is saved to: `output/processed_employees.csv`
-  Logs are generated in `logs/` for debugging and traceability



##  Possible Enhancements

- CLI arguments for file paths or custom config
- Streamlit dashboard for data exploration
- Unit tests for file validation and processing
- Schedule jobs using cron or Airflow




