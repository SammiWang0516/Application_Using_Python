import json
import os

# get the directory where this script file is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# join that directory with file name
json_file = os.path.join(script_dir, 'redlines_data.json')

f = open(json_file)
data = json.load(f)
f.close()

print(data)

import requests
r = requests.get("https://geo.fcc.gov/api/census/area", 
                 params={"lat": 42.3456, "lon": -83.1234, "censusYear": 2010, "format": "json"})
print(r.status_code)
print(r.json())