import json

with open('src/scraped_data/final_tesco_data.json','r') as f:
    data1 = json.load(f)
with open('src/scraped_data/final_morrison_data.json','r') as f:
    data2 = json.load(f)

merged_data = data1 + data2

with open('src/scraped_data/total_data.json','w') as f:
    json.dump(merged_data,f)