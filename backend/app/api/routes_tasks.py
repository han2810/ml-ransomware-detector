from flask import Blueprint, current_app, jsonify

from ..utils.response_utils import public_task


tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


@tasks_bp.get("")
def list_tasks():
    tasks = current_app.extensions["report_service"].list_tasks()
    return jsonify([public_task(task) for task in tasks])


@tasks_bp.get("/<task_id>")
def task_detail(task_id):
    task = current_app.extensions["report_service"].get_task(task_id)
    if task is None:
        return jsonify(error="Khong tim thay task."), 404
    return jsonify(public_task(task))

