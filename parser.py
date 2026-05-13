def parse(text: str) -> dict:
    data = {"preamble": [], "sections": []}
    current_section = None
    for (line_num, original_line) in enumerate(text.splitlines()):
        line = original_line.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if line.startswith("[") and "]" in line:
            start_idx = original_line.find("[")
            end_idx = original_line.rfind("]") + 1
            new_section = {
                "glob": original_line[start_idx:end_idx],
                "line": line_num,
                "range": {"start": start_idx, "end": end_idx},
                "properties": []
            }
            data["sections"].append(new_section)
            current_section = data["sections"][-1]
            continue
        if "=" in line:
            key_raw, val_raw = original_line.split("=", 1)
            key = key_raw.strip()
            value = val_raw.strip()
            key_start = original_line.find(key)
            value_start = original_line.find(value, key_start + len(key))
            prop= {
                "key": key,
                "value": value,
                "line": line_num,
                "key_range": {"start": key_start, "end": key_start + len(key)},
                "value_range": {"start": value_start, "end": value_start + len(value)}
            }
            if current_section is None:
                data["preamble"].append(prop)
            else:
                current_section["properties"].append(prop)
            continue
    return data
