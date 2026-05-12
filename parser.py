def parse(text: str):
    data = {
        "preamble": [],
        "sections": []
    }
    current_section = None
    for i, line in enumerate(text.split("\n")):
        line = line.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        elif line.startswith("["):
            data["sections"].append({
                "glob": line[1:-1],
                "line": i,
                "props": []
            })
            current_section = data["sections"][-1]
        elif "=" in line:
            key, value = (part.strip() for part in line.split("=", 1))
            target = data["preamble"] if current_section is None else current_section["props"]
            target.append({
                "key": key,
                "value": value,
                "line": i
            })
        else:
            continue
    return data
