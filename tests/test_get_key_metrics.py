from src.data_retrieval.api_client import FinancialModelingPrepClient

# Initialize the API client
# api_key = "your_actual_api_key"  # Replace with your actual API key
# client = FinancialModelingPrepClient(api_key=api_key)

# Define the arguments
symbol = 'AAPL'
period = 'annual'
is_ttm = False

# Construct the URL manually
endpoint = 'key-metrics-ttm' if is_ttm else 'key-metrics'
expected_url = f"{client.base_url}/{endpoint}/{symbol}?period={period}&apikey={client.api_key}"

# Call the method and print the URL
url = f"{client.base_url}/{endpoint}/{symbol}?period={period}&apikey={client.api_key}"
print(f"Expected URL: {expected_url}")
print(f"Constructed URL: {url}")

# Optionally, you can also print the response to see the data
response = client.get_key_metrics(symbol, period, is_ttm)
print(response)