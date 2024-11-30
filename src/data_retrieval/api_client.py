# src/data_retrieval/api_client.py
import os
import requests
import pandas as pd
from typing import List, Dict

class FinancialModelingPrepClient:
    """
    A robust client for retrieving financial data from Financial Modeling Prep API.
    
    Attributes:
        api_key (str): API key for authentication
        base_url (str): Base URL for API endpoints
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Financial Modeling Prep API client.
        
        Args:
            api_key (str): API authentication token
        """
        self.api_key = api_key
        self.base_url = "https://financialmodelingprep.com/api/v3"
    
    def get_symbol_list(self) -> List[str]:
        """
        Retrieve the list of available stock symbols.
        
        Returns:
            List[str]: List of stock symbols
        """
        url = f"{self.base_url}/financial-statement-symbol-lists?apikey={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
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