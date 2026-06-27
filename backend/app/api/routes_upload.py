from pathlib import Path
from uuid import uuid4

from flask import Blueprint, current_app, jsonify, request

from ..services.predict_service import DEFAULT_MODEL_ID, PredictService
from ..utils.file_utils import validate_and_normalize
from ..utils.response_utils import public_task


upload_bp = Blueprint("upload", __name__, url_prefix="/api")


@upload_bp.post("/upload")
def upload_sample():
    model_id = request.form.get("model_id", DEFAULT_MODEL_ID)
    try:
        model = PredictService.get_model(model_id)
    except ValueError as exc:
        return jsonify(error=str(exc)), 400

    uploaded_file = request.files.get("file")
    filename, error = validate_and_normalize(
        uploaded_file, current_app.config["ALLOWED_EXTENSIONS"]
    )
    if error:
        return jsonify(error=error), 400

    task_id = uuid4().hex
    sample_path = Path(current_app.config["SAMPLES_DIR"]) / f"{task_id}_{filename}"
    uploaded_file.save(sample_path)
    if sample_path.stat().st_size == 0:
        sample_path.unlink(missing_ok=True)
        return jsonify(error="File upload rong."), 400

    report_service = current_app.extensions["report_service"]
    task = report_service.create_task({
        "task_id": task_id,
        "filename": filename,
        "model_id": model_id,
        "model_name": model["name"],
        "sample_path": str(sample_path),
        "status": "queued",
        "progress": 0,
        "message": "Da dua vao hang doi.",
    })
    current_app.extensions["cuckoo_service"].start(task_id, sample_path, model_id)
    return jsonify(public_task(task)), 202


@upload_bp.get("/models")
def list_models():
    return jsonify(models=PredictService.available_models())
