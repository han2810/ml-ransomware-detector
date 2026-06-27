from pathlib import Path

import pandas as pd
from flask import Blueprint, current_app, jsonify

from ..services.predict_service import PredictService
from ..utils.response_utils import public_task


predict_bp = Blueprint("predict", __name__, url_prefix="/api")


@predict_bp.post("/predict/<task_id>")
def predict_again(task_id):
    report_service = current_app.extensions["report_service"]
    task = report_service.get_task(task_id)
    excel_path = Path(task["excel_path"]) if task and task.get("excel_path") else None
    if excel_path is None or not excel_path.is_file():
        return jsonify(error="File dac trung chua san sang."), 409
    try:
        frame = pd.read_excel(excel_path, engine="openpyxl")
        prediction = PredictService().predict(frame)
        task = report_service.update_task(task_id, prediction=prediction)
        return jsonify(public_task(task))
    except Exception as exc:
        return jsonify(error=str(exc)), 500

