import sys

import definitions
import diagnostics
import parser
import protocols


def publish_diagnostics(uri: str, text: str) -> None:
    parsed = parser.parse(text)
    diags = diagnostics.validate(parsed)
    protocols.send_notification("textDocument/publishDiagnostics", {
        "uri": uri,
        "diagnostics": diags
    })


def main():
    documents = {}
    while True:
        try:
            message = protocols.read_message()
        except EOFError:
            break
        method = message.get("method")
        params = message.get("params", {})

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
            protocols.send_response(message["id"], result)
        elif method == "initialized":
            pass
        elif method == "textDocument/didOpen":
            uri = params["textDocument"]["uri"]
            text = params["textDocument"]["text"]
            documents[uri] = text
            publish_diagnostics(uri, text)
        elif method == "textDocument/didChange":
            uri = params["textDocument"]["uri"]
            text = params["contentChanges"][0]["text"]
            documents[uri] = text
            publish_diagnostics(uri, text)
        elif method == "textDocument/didClose":
            uri = params["textDocument"]["uri"]
            if uri in documents:
                del documents[uri]
        elif method == "textDocument/hover":
            uri = params["textDocument"]["uri"]
            pos = params["position"]
            text = documents.get(uri, "")

            parsed = parser.parse(text)
            description = None

            for prop in parsed["preamble"]:
                if prop["line"] == pos["line"]:
                    if prop["key_range"]["start"] <= pos["character"] <= prop["key_range"]["end"]:
                        key = prop["key"]
                        if key in definitions.PROPERTIES:
                            description = definitions.PROPERTIES[key]["description"]
                        break

            if not description:
                for section in parsed["sections"]:
                    for prop in section["properties"]:
                        if prop["line"] == pos["line"]:
                            if prop["key_range"]["start"] <= pos["character"] <= prop["key_range"]["end"]:
                                key = prop["key"]
                                if key in definitions.PROPERTIES:
                                    description = definitions.PROPERTIES[key]["description"]
                                break
                    if description:
                        break

            if description:
                protocols.send_response(message["id"], {
                    "contents": {
                        "kind": "markdown",
                        "value": description
                    }
                })
            else:
                protocols.send_response(message["id"], None)

        elif method == "textDocument/completion":
            uri = params["textDocument"]["uri"]
            pos = params["position"]
            text = documents.get(uri, "")
            lines = text.splitlines()

            current_line = ""
            if pos["line"] < len(lines):
                current_line = lines[pos["line"]]

            line_before_cursor = current_line[:pos["character"]]

            items = []
            if "=" in line_before_cursor:
                key_part = current_line.split("=", 1)[0].strip()
                if key_part in definitions.PROPERTIES:
                    prop_def = definitions.PROPERTIES[key_part]
                    if prop_def["values"]:
                        for v in prop_def["values"]:
                            items.append({
                                "label": v,
                                "kind": 12, # Value
                                "detail": f"Value for {key_part}"
                            })
                    elif key_part == "indent_size":
                        items.append({"label": "tab", "kind": 12})
            else:
                for key, prop_def in definitions.PROPERTIES.items():
                    items.append({
                        "label": key,
                        "kind": 10,
                        "detail": prop_def["description"]
                    })

            protocols.send_response(message["id"], items)

        elif method == "shutdown":
            protocols.send_response(message["id"], None)
        elif method == "exit":
            sys.exit(0)


if __name__ == "__main__":
    main()
