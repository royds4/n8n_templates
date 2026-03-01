import json

with open("BTC Scrapping.json", "r") as f:
    data = json.load(f)

for node in data["nodes"]:
    if node["name"] in ["Top & Bottom Watchout1", "BTC Meso Market Analysis1", "Micro Market Analysis", "Market Stance1", "Data Clean and Debug", "Send a text message"]:
        print(f"--- Node: {node['name']} ---")
        if "messages" in node.get("parameters", {}):
            print(json.dumps(node["parameters"]["messages"]["values"][0]["content"], indent=2))
        elif "jsCode" in node.get("parameters", {}):
            print(node["parameters"]["jsCode"])
        elif "text" in node.get("parameters", {}):
            print(json.dumps(node["parameters"], indent=2))
        print("\n")
