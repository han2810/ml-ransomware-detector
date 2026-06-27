def extract(report):
    return {
        f"SIGNATURE:{item['name'].lower()}"
        for item in report.get("signatures", [])
        if item.get("name")
    }
