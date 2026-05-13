import json
import sys


def read_message() -> dict:
    line = sys.stdin.buffer.readline()
    if not line:
        raise EOFError()
    length = int(line.split(b":")[1].strip())
    sys.stdin.buffer.readline()
    return json.loads(sys.stdin.buffer.read(length))


def send_message(content: dict) -> None:
    content = json.dumps(content).encode("utf-8")
    header = f"Content-Length: {len(content)}\r\n\r\n".encode("ascii")
    sys.stdout.buffer.write(header)
    sys.stdout.buffer.write(content)
    sys.stdout.buffer.flush()


def send_response(
    id: int,
    result: dict | None = None
) -> None:
    send_message({
        "jsonrpc": "2.0",
        "id": id,
        "result": result
    })


def send_error(
    id: int,
    code: int,
    message: str
) -> None:
    send_message({
        "jsonrpc": "2.0",
        "id": id,
        "error": {
            "code": code,
            "message": message
        }
    })


def send_notification(
    method: str,
    params: dict
) -> None:
    send_message({
        "jsonrpc": "2.0",
        "method": method,
        "params": params
    })
