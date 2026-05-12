import protocol
import sys


def main() -> None:
    while True:
        message = protocol.read_message()
        method = message.get("method")
        if method == "initialize":
            protocol.send_response(message["id"], {"capabilities": {}})
        elif method == "initialized":
            pass
        elif method == "shutdown":
            protocol.send_response(message["id"])
        elif method == "exit":
            sys.exit(0)


if __name__ == "__main__":
    main()
