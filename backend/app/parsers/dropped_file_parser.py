def extract(report):
    extensions, file_types = set(), set()
    for item in report.get("dropped", []):
        name, file_type = item.get("name", ""), item.get("type", "")
        if "." in name:
            extensions.add(name.rsplit(".", 1)[-1].lower())
        if file_type:
            file_types.add(file_type.replace(" ", "_").lower())
    return ({f"DROP:EXTENSION:{value}" for value in extensions} |
            {f"DROP:TYPE:{value}" for value in file_types})

