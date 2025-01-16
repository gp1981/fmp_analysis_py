import os
from src.data_retrieval.api_client import FinancialModelingPrepClient
from src.data_processing.ranking import rank_companies_by_metrics
import keyring
from keyring.backends.macOS import Keyring

def main():
    # Set the macOS keyring explicitly
    keyring.set_keyring(Keyring())
    
    # Use the correct service name and account name
    service_name = 'RStudio Keyring Secrets'
    username = 'API_FMP_KEY'
    
    # Retrieve the API key
    api_key = keyring.get_password(service_name, username)
    
    if not api_key:
        raise ValueError("API key not found in keyring. Please ensure it is stored with service name 'RStudio Keyring Secrets' and username 'API_FMP_KEY'.")
    
    # Initialize API client
    client = FinancialModelingPrepClient(api_key)
    
    # Get symbol list
    symbols = client.get_symbol_list()
    
    # Filter symbols (example: filter industrial companies)
    industrial_symbols = [
        symbol for symbol in symbols 
        if client.get_company_profile(symbol).get('industry', '').lower() == 'industrial'
    ]
    
    # Collect company data
    companies_data = []
    for symbol in industrial_symbols:
        try:
            # Retrieve TTM metrics and ratios
            key_metrics_ttm = client.get_key_metrics(symbol, is_ttm=True)
            ratios_ttm = client.get_financial_ratios(symbol, is_ttm=True)
            
            # Combine data
            company_data = {
                'symbol': symbol,
                **key_metrics_ttm[0],
                **ratios_ttm[0]
            }
            companies_data.append(company_data)
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
    
    # Rank companies
    ranked_companies = rank_companies_by_metrics(companies_data)
    
    # Export to Excel
    ranked_companies.to_excel('output/company_rankings.xlsx', index=False)

if __name__ == "__main__":
    main()