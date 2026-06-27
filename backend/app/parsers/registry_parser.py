def extract(report):
    summary = report.get("behavior", {}).get("summary", {})
    features = set()
    for source, label in (
        ("regkey_opened", "OPENED"),
        ("regkey_deleted", "DELETED"),
        ("regkey_read", "READ"),
        ("regkey_written", "WRITTEN"),
    ):
        features.update(f"REG:{label}:{value}" for value in summary.get(source, []))
    return features

