import pandas as pd
import json

with open('survivors_data.json') as f:
    data = json.load(f)

df = pd.json_normalize(data)

df.to_excel('output.xlsx', index=False)
