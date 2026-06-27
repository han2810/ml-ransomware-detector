def extract(report):
    summary = report.get("behavior", {}).get("summary", {})
    sources = ("dll_loaded", "command_line", "mutex", "guid")
    return {
        f"SYSTEM:{source.upper()}:{str(value).lower()}"
        for source in sources
        for value in summary.get(source, [])
    }

