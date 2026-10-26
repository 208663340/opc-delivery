import hashlib
import json
from pathlib import Path

payload = Path("source.txt").read_bytes()
Path("artifact.txt").write_bytes(payload)
receipt = {"version": "demo-B", "sha256": hashlib.sha256(payload).hexdigest(), "bytes": len(payload)}
Path("build.json").write_text(json.dumps(receipt) + "\n")
print(json.dumps(receipt))
