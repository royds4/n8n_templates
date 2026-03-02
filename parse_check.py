import json
try:
    with open("BTC Scrapping.json", "r") as f:
        data = json.load(f)
        for node in data["nodes"]:
            if node["name"] == "Data Clean and Debug":
                print(node["parameters"]["jsCode"])
except Exception as e:
    pass
