import json
import re
import sys

print("Python version:", sys.version)
print("Starting test...")

# Load ticker mappings from JSON
try:
    with open("ticker.json", "r") as f:
        raw_company_data = json.load(f)
    print(f"Successfully loaded ticker.json with {len(raw_company_data)} entries")
except Exception as e:
    print(f"Error loading ticker.json: {str(e)}")
    sys.exit(1)

def normalize_title(name):
    name = name.lower()
    name = re.sub(r'[^a-z0-9\s]', '', name)
    name = re.sub(r'\b(inc|corp|co|ltd|plc|sa|nv|se|llc|lp|group|holdings|international|limited|technologies|solutions|systems|enterprises?)\b', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

name_to_ticker = {}
# Convert the numbered indices to a ticker-based mapping
for item in raw_company_data.values():
    title = normalize_title(item['title'])
    ticker = item['ticker'].upper()
    name_to_ticker[title] = ticker
    name_to_ticker[ticker] = ticker

def get_ticker_from_name(input_text):
    print(f"Looking up: '{input_text}'")
    input_text_norm = normalize_title(input_text)
    print(f"Normalized to: '{input_text_norm}'")
    
    ticker_upper = name_to_ticker.get(input_text.upper())
    if ticker_upper:
        print(f"Found via uppercase ticker lookup: {ticker_upper}")
        return ticker_upper
        
    ticker_norm = name_to_ticker.get(input_text_norm)
    if ticker_norm:
        print(f"Found via normalized name lookup: {ticker_norm}")
        return ticker_norm
        
    return f"Could not find ticker for input: '{input_text}'. Please try a valid company name or ticker."

# Test cases
test_inputs = [
    "AAPL",          # Direct ticker lookup
    "Apple Inc.",    # Full company name
    "Apple",         # Partial company name
    "apple",         # Lowercase company name
    "Microsoft",     # Another company
    "MSFT",          # Another ticker
    "NVIDIA CORP",   # Company with common suffix
    "Invalid Company" # Invalid input
]

print("\nTesting ticker lookup functionality:")
print("-" * 50)
for test_input in test_inputs:
    result = get_ticker_from_name(test_input)
    print(f"Final result for '{test_input}': '{result}'")
    print("-" * 30)

# Print name_to_ticker map size
print(f"Total entries in name_to_ticker map: {len(name_to_ticker)}")
print(f"Total companies in raw_company_data: {len(raw_company_data)}")

# Print some sample mappings
print("-" * 50)
print("Sample normalized company names to tickers:")
count = 0
for key, value in name_to_ticker.items():
    if key.lower() != value.lower():  # Skip ticker to ticker mappings
        print(f"  '{key}' -> '{value}'")
        count += 1
        if count >= 5:
            break 