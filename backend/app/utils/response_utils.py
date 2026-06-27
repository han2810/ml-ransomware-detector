from pathlib import Path


def public_task(task):
    if task is None:
        return None
    data = {key: value for key, value in task.items() if not key.endswith("_path")}
    task_id = task["task_id"]
    if task.get("report_path") and Path(task["report_path"]).is_file():
        data["report_url"] = f"/api/reports/{task_id}"
    if task.get("excel_path") and Path(task["excel_path"]).is_file():
        data["excel_url"] = f"/api/excels/{task_id}"
    return data
