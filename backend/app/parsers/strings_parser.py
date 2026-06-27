def extract(report):
    return {f"STRING:{str(value).lower()}" for value in report.get("strings", [])}

