import json

with open("Generate subtitles on video (FFMPEG).json", "r") as f:
    data = json.load(f)

for n in data["nodes"]:
    if n["name"] == "Extract ElevenLabs Payload":
        print(n["parameters"]["jsCode"])
