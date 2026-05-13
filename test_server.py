import subprocess
import json
import time

def format_message(payload):
    body = json.dumps(payload).encode("utf-8")
    header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
    return header + body

def test_handshake():
    # Start the server
    process = subprocess.Popen(
        ["python3", "server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # 1. Send Initialize Request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "capabilities": {}
        }
    }
    
    print("Sending initialize request...")
    process.stdin.write(format_message(init_request))
    process.stdin.flush()

    # 2. Read Response
    # First line should be Content-Length
    header = process.stdout.readline().decode("ascii")
    print(f"Received header: {header.strip()}")
    
    # Skip the blank line
    process.stdout.readline()
    
    # Read body
    length = int(header.split(":")[1].strip())
    body = process.stdout.read(length).decode("utf-8")
    response = json.loads(body)
    
    print("Received response body:")
    print(json.dumps(response, indent=2))

    # Assertions
    assert response["id"] == 1
    assert "capabilities" in response["result"]
    print("\n✅ Handshake successful!")

    # Cleanup
    process.terminate()

if __name__ == "__main__":
    try:
        test_handshake()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
