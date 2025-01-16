import unittest
from unittest.mock import patch, MagicMock
from src.data_retrieval.api_client import FinancialModelingPrepClient

class TestFinancialModelingPrepClient(unittest.TestCase):

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

    @patch('src.data_retrieval.api_client.requests.get')
    def test_get_company_profile(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = [{'industry': 'industrial'}]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = FinancialModelingPrepClient(api_key='test_api_key')
        profile = client.get_company_profile('AAPL')
        self.assertEqual(profile, {'industry': 'industrial'})

    @patch('src.data_retrieval.api_client.requests.get')
    def test_get_key_metrics(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = [{'returnOnCapitalEmployedTTM': 10}]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = FinancialModelingPrepClient(api_key='test_api_key')
        metrics = client.get_key_metrics('AAPL', is_ttm=True)
        self.assertEqual(metrics, [{'returnOnCapitalEmployedTTM': 10}])

    @patch('src.data_retrieval.api_client.requests.get')
    def test_get_financial_ratios(self, mock_get):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = [{'evToOperatingCashFlowTTM': 5}]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = FinancialModelingPrepClient(api_key='test_api_key')
        ratios = client.get_financial_ratios('AAPL', is_ttm=True)
        self.assertEqual(ratios, [{'evToOperatingCashFlowTTM': 5}])

if __name__ == '__main__':
    unittest.main()