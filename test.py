import json
import subprocess


body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}).encode()
message = f"Content-Length: {len(body)}\r\n\r\n".encode() + body


proc = subprocess.run(
    ["python3", "server.py"],
    input=message,
    capture_output=True
)

print(proc.stdout)
