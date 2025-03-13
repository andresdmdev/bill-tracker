"""Test cases for PhotoService class."""
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from models.bill import Bill, BillStatus
from services.photo_service import PhotoService

class TestPhotoService(unittest.TestCase):
    """Test cases for PhotoService class."""

    def setUp(self):
        """Set up test cases."""
        self.photo_service = PhotoService()
        self.test_bill = Bill(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            category="Test",
            medium="Cash",
            amount="100",
            dollar_amount="5",
            status=BillStatus.Unpaid,
            notes="Test notes"
        )

    @patch('services.photo_service.build')
    @patch('services.photo_service.service_account.Credentials.from_service_account_info')
    def test_insert_bill_data_in_sheet_row_success(self, mock_credentials, mock_build):
        """Test successful insertion of bill data in sheet."""
        # Mock the Google Sheets API response
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_execute = MagicMock(return_value={'updates': {'updatedCells': 7}})
        mock_service.spreadsheets().values().append().execute = mock_execute

        # Execute the method
        self.photo_service.insert_bill_data_in_sheet_row(self.test_bill)

        # Verify the API was called with correct parameters
        mock_build.assert_called_once_with('sheets', 'v4', credentials=mock_credentials.return_value)
        mock_service.spreadsheets().values().append.assert_called_once()

    @patch('services.photo_service.build')
    @patch('services.photo_service.service_account.Credentials.from_service_account_info')
    def test_insert_bill_data_in_sheet_row_failure(self, mock_credentials, mock_build):
        """Test handling of API error when inserting bill data."""
        # Mock the Google Sheets API to raise an exception
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_service.spreadsheets().values().append().execute.side_effect = Exception("API Error")

        # Verify that the method raises an IOError
        with self.assertRaises(IOError) as context:
            self.photo_service.insert_bill_data_in_sheet_row(self.test_bill)

        self.assertIn("Error al ingresar datos a Google Sheets", str(context.exception))
