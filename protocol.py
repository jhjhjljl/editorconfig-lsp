import json
import sys


def read_message() -> dict:
    header = sys.stdin.buffer.readline()
    sys.stdin.buffer.readline()
    length = int(header.split(b":")[1].strip())
    body = sys.stdin.buffer.read(length)
    return json.loads(body)


def write_message(msg: dict) -> None:
    body = json.dumps(msg).encode()
    message = f"Content-Length: {len(body)}\r\n\r\n".encode() + body
    sys.stdout.buffer.write(message)
    sys.stdout.buffer.flush()


def send_response(id: int, result: dict | None = None) -> None:
    write_message({"jsonrpc": "2.0", "id": id, "result": result})


def send_error(id: int, code: int, message: str) -> None:
    write_message({"jsonrpc": "2.0", "id": id, "error": {"code": code, "message": message}})


def send_notification(method: str, params: dict):
    write_message({"jsonrpc": "2.0", "method": method, "params": params})
