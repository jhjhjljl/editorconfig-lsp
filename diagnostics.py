import definitions


def create_diagnostic_message(
    line: int,
    start: int,
    end: int,
    message: str,
    severity: int
):
    return {
        "range": {
            "start": {
                "line": line,
                "character": start
            },
            "end": {
                "line": line,
                "character": end
            }
        },
        "message": message,
        "severity": severity
    }


def validate(parsed_data: dict):
    diagnostics = []
    for prop in parsed_data["preamble"]:
        key = prop["key"]
        value = prop["value"]
        line = prop["line"]
        if key != "root":
            diag = create_diagnostic_message(
                line,
                prop["key_range"]["start"],
                prop["key_range"]["end"],
                f"Unknown preamble key '{key}'. Only 'root' is allowed at the top of the file.",
                1
            )
            diagnostics.append(diag)
            continue
        if value not in definitions.PROPERTIES["root"]["values"]:
            diag = create_diagnostic_message(
                line,
                prop["value_range"]["start"],
                prop["value_range"]["end"],
                f"Invalid value '{value}' for 'root'. Expected 'true' or 'false'.",
                1
            )
            diagnostics.append(diag)
            continue
    for section in parsed_data["sections"]:
        for prop in section["properties"]:
            key = prop["key"]
            value = prop["value"]
            line = prop["line"]
            if key == "root":
                diag = create_diagnostic_message(
                    line,
                    prop["key_range"]["start"],
                    prop["key_range"]["end"],
                    "The 'root' property must be defined at the top of the file, before any sections.",
                    1
                )
                diagnostics.append(diag)
                continue
            if key not in definitions.PROPERTIES:
                diag = create_diagnostic_message(
                    line,
                    prop["key_range"]["start"],
                    prop["key_range"]["end"],
                    f"Unknown property key '{key}'.",
                    1
                )
                diagnostics.append(diag)
                continue
            if definitions.PROPERTIES[key]["values"] is None:
                if key == "indent_size" and value != "tab":
                    try:
                        if int(value) <= 0:
                            diag = create_diagnostic_message(
                                line,
                                prop["value_range"]["start"],
                                prop["value_range"]["end"],
                                "'indent_size' must be a positive integer or 'tab'.",
                                1
                            )
                            diagnostics.append(diag)
                    except ValueError:
                        diag = create_diagnostic_message(
                            line,
                            prop["value_range"]["start"],
                            prop["value_range"]["end"],
                            "'indent_size' must be a positive integer or 'tab'.",
                            1
                        )
                        diagnostics.append(diag)
                elif key == "tab_width":
                    try:
                        if int(value) <= 0:
                            diag = create_diagnostic_message(
                                line,
                                prop["value_range"]["start"],
                                prop["value_range"]["end"],
                                "'tab_width' must be a positive integer.",
                                1
                            )
                            diagnostics.append(diag)
                    except ValueError:
                        diag = create_diagnostic_message(
                            line,
                            prop["value_range"]["start"],
                            prop["value_range"]["end"],
                            "'tab_width' must be a positive integer.",
                            1
                        )
                        diagnostics.append(diag)
                elif key == "spelling_language" and len(value) not in (2, 5):
                    diag = create_diagnostic_message(
                        line,
                        prop["value_range"]["start"],
                        prop["value_range"]["end"],
                        "'spelling_language' must be a 2 or 5 character code (e.g., 'en' or 'en-US').",
                        1
                    )
                    diagnostics.append(diag)
                continue
            if value not in definitions.PROPERTIES[key]["values"]:
                valid_vals = ", ".join([f"'{v}'" for v in definitions.PROPERTIES[key]["values"]])
                diag = create_diagnostic_message(
                    line,
                    prop["value_range"]["start"],
                    prop["value_range"]["end"],
                    f"Invalid value '{value}' for '{key}'. Expected one of: {valid_vals}.",
                    1
                )
                diagnostics.append(diag)
    return diagnostics
