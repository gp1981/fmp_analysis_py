import pandas as pd

def rank_companies_by_metrics(companies_data: List[Dict]) -> pd.DataFrame:
    """
    Rank companies based on Return on Capital Employed and EV/Operating Cash Flow.
    
    Args:
        companies_data (List[Dict]): List of company financial data
    
    Returns:
        pd.DataFrame: Ranked companies DataFrame
    """
    ranking_df = pd.DataFrame([
        {
            'symbol': company['symbol'],
            'return_on_capital_employed': company.get('returnOnCapitalEmployedTTM', 0),
            'ev_to_operating_cash_flow': company.get('evToOperatingCashFlowTTM', 0)
        } 
        for company in companies_data
    ])
    
    # Normalize and combine rankings
    ranking_df['return_on_capital_employed_rank'] = ranking_df['return_on_capital_employed'].rank(ascending=False)
    ranking_df['ev_to_operating_cash_flow_rank'] = ranking_df['ev_to_operating_cash_flow'].rank(ascending=True)
    
    ranking_df['total_rank'] = ranking_df['return_on_capital_employed_rank'] + ranking_df['ev_to_operating_cash_flow_rank']
    
    return ranking_df.sort_values('total_rank')