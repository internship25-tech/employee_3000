import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os

import processing  # your main code file (processing.py)

class TestProcessing(unittest.TestCase):

    @patch("processing.os.listdir")
    def test_find_excel_file(self, mock_listdir):
        # Test Case 1: Verify EXCEL File Detection
        mock_listdir.return_value = ["dummy.xlsx", "note.txt"]
        result = processing.find_excel_file("some_dir")
        self.assertEqual(result, os.path.join("some_dir", "dummy.xlsx"))
        print("Test 1 passed: Excel file correctly found")

    @patch("processing.pd.read_excel")
    @patch("processing.find_excel_file")
    @patch("processing.os.makedirs")
    @patch("processing.pd.DataFrame.to_csv")
    def test_process_employee_data_success(self, mock_to_csv, mock_makedirs, mock_find, mock_read_excel):
        # Test Case 2: Verify EXCEL File Extraction & Processing
        mock_find.return_value = "dummy.xlsx"
        mock_df = pd.DataFrame({
            "EEID": [1],
            "Full Name": ["Alice Smith"],
            "Job Title": ["Developer"],
            "Hire Date": ["2021-01-01"]
        })
        mock_read_excel.return_value = mock_df

        processing.process_employee_data()
        self.assertTrue(mock_to_csv.called)
        print("Test 2 passed: Excel processed and CSV written")

    def test_validate_file_type_format(self):
        # Test Case 3: Validate File Type and Format
        valid_files = ["employee.xlsx", "employee.xls"]
        invalid_files = ["data.csv", "image.png"]

        for file in valid_files:
            self.assertTrue(file.endswith((".xlsx", ".xls")))

        for file in invalid_files:
            self.assertFalse(file.endswith((".xlsx", ".xls")))

        print("Test 3 passed: File type and format validated")

    def test_validate_data_structure(self):
        # Test Case 4: Validate Data Structure
        df = pd.DataFrame(columns=[
            "Employee ID", "First Name", "Last Name", "Email", "Job Title", "Phone Number", "Hire Date"
        ])
        missing = [field for field in processing.REQUIRED_FIELDS if field not in df.columns]
        self.assertEqual(missing, [])
        print("Test 4 passed: Required data structure is present")

    @patch("processing.pd.read_excel")
    @patch("processing.find_excel_file")
    def test_handle_missing_invalid_data(self, mock_find, mock_read_excel):
        #  Test Case 5: Handle Missing or Invalid Data
        mock_find.return_value = "dummy.xlsx"
        mock_df = pd.DataFrame({
            "Full Name": ["Bob Jones"]  # Missing all required fields
        })
        mock_read_excel.return_value = mock_df

        # Use root logger since processing.py uses logging.basicConfig()
        with self.assertLogs(level="ERROR") as log_output:
            processing.process_employee_data()

        self.assertTrue(any("Missing required fields" in msg for msg in log_output.output))
        print("Test 5 passed: Handled missing/invalid fields correctly")

if __name__ == '__main__':
    unittest.main()
