def extract(report):
    summary = report.get("behavior", {}).get("summary", {})
    labels = {"directory_created": "CREATED", "directory_enumerated": "ENUMERATED"}
    return {
        f"DIRECTORY:{label}:{value.lower()}"
        for source, label in labels.items()
        for value in summary.get(source, [])
    }

