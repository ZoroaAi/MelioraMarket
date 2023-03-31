import json

try:
    # Open the JSON file for reading
    with open('src/scraped_data/total_data.json', 'r') as f:
        data = json.load(f)

    # Loop through each object in the list
    for obj in data:
        # Check if the 'price' value has one decimal place
        if isinstance(obj['price'], float) and obj['price'] == round(obj['price'], 1):
            # Update the value with two decimal places
            obj['price'] = round(obj['price'], 2)

    # Write the updated data back to the file
    with open('src/scraped_data/total_data.json', 'w') as f:
        json.dump(data, f, indent=2)

except Exception as e:
    print(f"Error: {e}")
