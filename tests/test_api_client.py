import unittest
from unittest.mock import patch, MagicMock
from src.data_retrieval.api_client import FinancialModelingPrepClient

class TestFinancialModelingPrepClient(unittest.TestCase):

    @patch('src.data_retrieval.api_client.keyring.get_password')
    def test_init_with_keyring(self, mock_get_password):
        # Mock keyring to return a test API key
        mock_get_password.return_value = 'test_api_key'
        
        client = FinancialModelingPrepClient()
        self.assertEqual(client.api_key, 'test_api_key')
    
    @patch('src.data_retrieval.api_client.requests.get')
    def test_get_symbol_list(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = ['AAPL', 'MSFT', 'GOOGL']
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        client = FinancialModelingPrepClient(api_key='test_api_key')
        symbols = client.get_symbol_list()
        self.assertEqual(symbols, ['AAPL', 'MSFT', 'GOOGL'])
        mock_get.assert_called_once_with('https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey=test_api_key')

    @patch('src.data_retrieval.api_client.requests.get')
    def test_get_company_profile(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = [{'industry': 'tech'}]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        client = FinancialModelingPrepClient(api_key='test_api_key')
        profile = client.get_company_profile('AAPL')
        self.assertEqual(profile, {'industry': 'tech'})
        mock_get.assert_called_once_with('https://financialmodelingprep.com/api/v3/profile/AAPL?apikey=test_api_key')
        if __name__ == '__main__':
            unittest.main()
