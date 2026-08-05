import os
import json
import subprocess
import sys

# Récupération du port injecté par Upsun
port = int(os.environ.get("PORT", 8080))
print(f"Lancement de Xray sur le port : {port}", flush=True)

# Mise à jour du port dans config.json
try:
    with open("config.json", "r") as f:
        config = json.load(f)

    config["inbounds"][0]["port"] = port

    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
except Exception as e:
    print(f"Erreur lors de la mise à jour de config.json: {e}", sys.stderr)

# Droits d'exécution sur le binaire
subprocess.run(["chmod", "+x", "./xray"], check=False)

# Exécution de Xray
subprocess.run(["./xray", "run", "-config", "config.json"])
