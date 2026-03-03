import json

with open("Generate subtitles on video (FFMPEG).json", "r") as f:
    data = json.load(f)

for n in data["nodes"]:
    if n["name"] == "Extract ElevenLabs Payload":
        print("Extract ElevenLabs Payload exists.")
    if n["name"] == "Execute Command2":
        print("Execute Command2 exists.")
