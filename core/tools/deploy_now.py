import json
import subprocess
import os

auth_path = os.path.expanduser(r"~\AppData\Roaming\com.vercel.cli\Data\auth.json")
with open(auth_path, "r", encoding="utf-8") as f:
    auth_data = json.load(f)

token = auth_data["token"]
cwd = os.path.abspath("code/projeto_ead_tutores")

cmd = ["npx", "vercel", "deploy", "--prod", "--yes", "--token", token]
print(f"Deploying to Vercel production from {cwd}...")

res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
print("STDOUT:\n", res.stdout)
print("STDERR:\n", res.stderr)
print("Exit code:", res.returncode)
