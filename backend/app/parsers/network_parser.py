def extract(report):
    summary = report.get("behavior", {}).get("summary", {})
    sources = ("connects_ip", "connects_host", "resolves_host")
    return {
        f"NETWORK:{source.upper()}:{str(value).lower()}"
        for source in sources
        for value in summary.get(source, [])
    }

