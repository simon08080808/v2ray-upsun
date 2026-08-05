import os
import json
import subprocess

port = int(os.environ.get("PORT", 8080))

with open("config.json", "r") as f:
    config = json.load(f)

config["inbounds"][0]["port"] = port

with open("config.json", "w") as f:
    json.dump(config, f, indent=2)

subprocess.run(["./xray", "run", "-c", "config.json"])
