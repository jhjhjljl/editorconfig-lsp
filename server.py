import sys

from protocols import (
    read_message,
    send_response
)


def main():
    documents = {}
    while True:
        try:
            message = read_message()
        except EOFError:
            break
        method = message.get("method")

        if method == "initialize":
            result = {
                "capabilities": {
                    "textDocumentSync": 1,
                    "hoverProvider": True,
                    "completionProvider": {
                        "resolveProvider": False,
                        "triggerCharacters": ["="]
                    }
                }
            }
            send_response(message["id"], result)
        elif method == "initialized":
            pass
        elif method == "textDocument/didOpen":
            uri = message["params"]["textDocument"]["uri"]
            text = message["params"]["textDocument"]["text"]
            documents[uri] = text
        elif method == "textDocument/didChange":
            uri = message["params"]["textDocument"]["uri"]
            text = message["params"]["contentChanges"][0]["text"]
            documents[uri] = text
        elif method == "shutdown":
            send_response(message["id"], None)
        elif method == "exit":
            sys.exit(0)


if __name__ == "__main__":
    main()
