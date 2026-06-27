from pathlib import Path

from flask import Blueprint, current_app, jsonify, send_file


reports_bp = Blueprint("reports", __name__, url_prefix="/api")


def _download(task_id, key, suffix):
    task = current_app.extensions["report_service"].get_task(task_id)
    path = Path(task[key]) if task and task.get(key) else None
    if path is None or not path.is_file():
        return jsonify(error="File chua san sang."), 404
    return send_file(path, as_attachment=True, download_name=f"{task_id}{suffix}")


@reports_bp.get("/reports/<task_id>")
def download_report(task_id):
    return _download(task_id, "report_path", "_report.json")


@reports_bp.get("/excels/<task_id>")
def download_excel(task_id):
    return _download(task_id, "excel_path", "_features.xlsx")

