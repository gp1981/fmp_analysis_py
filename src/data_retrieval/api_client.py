# src/data_retrieval/api_client.py
from typing import List, Dict
import requests
import keyring

class FinancialModelingPrepClient:
    """
    A robust client for retrieving financial data from Financial Modeling Prep API.
    
    Attributes:
        api_key (str): API key for authentication
        base_url (str): Base URL for API endpoints
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Financial Modeling Prep API client.
        
        Args:
            api_key (str): API authentication token
        """
        if api_key is None:
            # Retrieve API key from keyring
            service_name = 'your_service_name'
            username = 'your_username'
            api_key = keyring.get_password(service_name, username)
            if not api_key:
                raise ValueError("API key not found in keyring. Please set the 'API_FMP_KEY' environment variable or store it in keyring.")
        self.api_key = api_key
        self.base_url = "https://financialmodelingprep.com/api/v3"
    
    def get_symbol_list(self) -> List[Dict]:
        """
        Retrieve the list of available stock symbols and filter them based on exchangeShortName.
        
        Returns:
            List[Dict]: Filtered list of stock symbols with financial statements
        """
        # Retrieve stock list data
        url_stock_list = f"{self.base_url}/stock/list?apikey={self.api_key}"
        response_stock_list = requests.get(url_stock_list)
        response_stock_list.raise_for_status()
        stock_list_data = response_stock_list.json()
        
        # Retrieve financial statement symbol list
        url_financial_statement_list = f"{self.base_url}/financial-statement-symbol-lists?apikey={self.api_key}"
        response_financial_statement_list = requests.get(url_financial_statement_list)
        response_financial_statement_list.raise_for_status()
        financial_statement_list = response_financial_statement_list.json()
        
        # Convert lists to dictionaries for easy lookup
        financial_statement_symbols = {item: item for item in financial_statement_list}
        
        # Filter stock list data to include only those with financial statements
        filtered_stock_list = [
            stock for stock in stock_list_data
            if stock['symbol'] in financial_statement_symbols and stock['exchangeShortName'] in {"AMEX", "ETF", "NASDAQ", "NYSE", "OTC"}
        ]
        
        return filtered_stock_list
    
    def get_company_profile(self, symbol: str) -> Dict:
        """
        Retrieve company profile for a given stock symbol.
        
        Args:
            symbol (str): Stock symbol
        
        Returns:
            Dict: Company profile information
        """
        url = f"{self.base_url}/profile/{symbol}?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()[0]
    
    def get_financial_statements(self, symbol: str, statement_type: str, 
                                 period: str = 'quarter', limit: int = 4) -> List[Dict]:
        """
        Retrieve financial statements for a given symbol.
        
        Args:
            symbol (str): Stock symbol
            statement_type (str): Type of financial statement 
                                  ('income-statement', 'balance-sheet-statement', 'cash-flow-statement')
            period (str, optional): Statement period. Defaults to 'quarter'.
            limit (int, optional): Number of statements to retrieve. Defaults to 4.
        
        Returns:
            List[Dict]: Financial statement data
        """
        url = f"{self.base_url}/{statement_type}/{symbol}?period={period}&limit={limit}&apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_key_metrics(self, symbol: str, period: str = 'annual', is_ttm: bool = False) -> List[Dict]:
        """
        Retrieve key metrics for a given symbol.
        
        Args:
            symbol (str): Stock symbol
            period (str, optional): Metrics period. Defaults to 'annual'.
            is_ttm (bool, optional): Whether to retrieve TTM metrics. Defaults to False.
        
        Returns:
            List[Dict]: Key metrics data
        """
        endpoint = 'key-metrics-ttm' if is_ttm else 'key-metrics'
        url = f"{self.base_url}/{endpoint}/{symbol}?period={period}&apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_financial_ratios(self, symbol: str, period: str = 'quarter', is_ttm: bool = False) -> List[Dict]:
        """
        Retrieve financial ratios for a given symbol.
        
        Args:
            symbol (str): Stock symbol
            period (str, optional): Ratios period. Defaults to 'quarter'.
            is_ttm (bool, optional): Whether to retrieve TTM ratios. Defaults to False.
        
        Returns:
            List[Dict]: Financial ratios data
        """
        endpoint = 'ratios-ttm' if is_ttm else 'ratios'
        url = f"{self.base_url}/{endpoint}/{symbol}?period={period}&apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()