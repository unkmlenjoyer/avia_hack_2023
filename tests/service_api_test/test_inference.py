"""
Test script for service working with json data
"""

# %%
import json

import pandas as pd
import requests

# %%
pd.set_option("display.max_rows", 1000)
pd.set_option("display.max_columns", 50)

# %%
with open("test_request.json", "r") as f:
    data = json.loads(f.read())

# %%
res = requests.request("POST", "http://0.0.0.0:8001/predict_batch", json=data)

# %%
final = pd.DataFrame.from_dict(res.json(), orient="index")

# %%
final
