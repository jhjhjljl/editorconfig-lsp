import definitions


def validate(data: dict) -> dict:
    diagnostics = []
    all_props = data["preamble"]
    for section in data["sections"]:
        for prop in section["props"]:
            if prop["key"] == "root":
                diagnostics.append({
                    "line": prop["line"],
                    "message": "'root' must be in preamble, not inside a section.",
                    "severity": 1
                })
        all_props += section["props"]
    for prop in all_props:
        key = prop["key"]
        value = prop["value"]
        line = prop["line"]
        if key not in definitions.PROPERTIES:
            diagnostics.append({
                "line": line,
                "message": f"Unknown key '{key}'.",
                "severity": 2
            })
            continue
        if definitions.PROPERTIES[key]["values"] is None:
            if key == "indent_size":
                if value == "tab":
                    continue
                else:
                    try:
                        if int(value) <= 0:
                            diagnostics.append({
                                "line": line,
                                "message": f"'{key}' must be a positive integer or 'tab'.",
                                "severity": 1
                            })
                    except ValueError:
                        diagnostics.append({
                            "line": line,
                            "message": f"'{key}' must be a positive integer or 'tab'.",
                            "severity": 1
                        })
                continue
            if key == "tab_width":
                try:
                    if int(value) <= 0:
                        diagnostics.append({
                            "line": line,
                            "message": f"'{key}' must be a positive integer.",
                            "severity": 1
                        })
                except ValueError:
                    diagnostics.append({
                        "line": line,
                        "message": f"'{key}' must be a positive integer.",
                        "severity": 1
                    })
                continue
            if key == "spelling_language":
                if len(value) not in (2, 5):
                    diagnostics.append({
                        "line": line,
                        "message": f"'{key}' must be a 2 or 5 character language code (e.g. 'en' or 'en-US').",
                        "severity": 1
                    })
                continue
        if value.lower() not in definitions.PROPERTIES[key]["values"]:
            diagnostics.append({
                "line": line,
                "message": f"Invalid value '{value}' for '{key}'.",
                "severity": 1
            })
    return diagnostics
