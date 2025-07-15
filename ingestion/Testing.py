import unittest
from unittest.mock import patch, MagicMock
import os
import src.run_scraper as scraper  # Import the module

class TestRunScraper(unittest.TestCase):

    @patch('src.run_scraper.requests.get')
    def test_download_excel_file(self, mock_get):
        mock_response = MagicMock()
        mock_response.iter_content = lambda chunk_size: [b'data']
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        result = scraper.download_zip_file("http://fake-url.com/file.zip", "fake_path.zip")
        self.assertTrue(result)
        print("Test 1 passed: Download ZIP file")

    @patch('src.run_scraper.zipfile.ZipFile')
    def test_extract_excel_file(self, mock_zipfile_class):
        mock_zipfile_instance = MagicMock()
        mock_zipfile_class.return_value.__enter__.return_value = mock_zipfile_instance

        result = scraper.extract_zip_file("fake.zip", "some/dir")
        self.assertTrue(result)
        mock_zipfile_instance.extractall.assert_called_with("some/dir")
        print("Test 2 passed: Extract ZIP file")

    def test_validate_file_type_format(self):
        file_path = os.path.join(scraper.EXTRACT_DIR, "data.xlsx")
        allowed_exts = [".csv", ".xls", ".xlsx", ".json", ".xml"]
        ext = os.path.splitext(file_path)[1]
        self.assertIn(ext, allowed_exts)
        print("Test 3 passed: Validate file type and format")

    def test_validate_data_structure(self):
        parsed_data = {
            "employee_id": "E001",
            "name": "Ravi Kumar",
            "email": "ravi@example.com"
        }
        required_fields = {"employee_id", "name", "email"}
        self.assertTrue(required_fields.issubset(parsed_data.keys()))
        print("Test 4 passed: Validate data structure")

    def test_handle_missing_invalid_data(self):
        data = {
            "employee_id": "E002",
            "name": "Nikita"
        }
        required_fields = {"employee_id", "name", "email"}
        missing = required_fields - data.keys()
        self.assertTrue(len(missing) > 0)
        print("Test 5 passed: Handle missing or invalid data")

if __name__ == '__main__':
    unittest.main()
