def extract(report):
    summary = report.get("behavior", {}).get("summary", {})
    labels = {
        "file_created": "CREATED", "file_recreated": "RECREATED",
        "file_opened": "OPENED", "file_written": "WRITTEN",
        "file_deleted": "DELETED", "file_exists": "EXISTS",
        "file_failed": "FAILED", "file_read": "READ",
    }
    return {
        f"FILE:{label}:{value.lower()}"
        for source, label in labels.items()
        for value in summary.get(source, [])
    }

