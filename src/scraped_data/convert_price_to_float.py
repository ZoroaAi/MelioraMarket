import json

def convert_price(price_str):
    """Converts a string with a currency symbol and a number to a float"""
    if price_str.endswith('p'):
        price_str = price_str[:-1]  # remove the 'p' suffix
        price_float = float(price_str) / 100
    else:
        price_float = float(price_str)
    return price_float

# Load the JSON file
with open('src/scraped_data/total_data.json') as f:
    data = json.load(f)

# Modify the price values
for obj in data:
    if 'price' in obj:
        price_str = obj['price']
        obj['price'] = convert_price(price_str)

# Save the modified data back to the file
with open('src/scraped_data/total_data1.json', 'w') as f:
    json.dump(data, f, indent=2)
