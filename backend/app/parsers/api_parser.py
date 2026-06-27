def extract(report):
    apistats = report.get("behavior", {}).get("apistats", {})
    calls = {api for process in apistats.values() for api in process}
    return {f"API:{api}" for api in calls}

