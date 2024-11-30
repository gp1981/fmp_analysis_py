import os
from src.data_retrieval.api_client import FinancialModelingPrepClient
from src.data_processing.ranking import rank_companies_by_metrics

def main():
    # Load API key from environment variable
    API_KEY = os.getenv('FINANCIAL_MODELING_PREP_API_KEY')
    
    # Initialize API client
    client = FinancialModelingPrepClient(API_KEY)
    
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