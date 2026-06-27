import os

from flask import Flask, jsonify

from .api.routes_predict import predict_bp
from .api.routes_reports import reports_bp
from .api.routes_tasks import tasks_bp
from .api.routes_upload import upload_bp
from .config import Config
from .services.cuckoo_service import CuckooService
from .services.report_service import ReportService


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response

    for key in ("SAMPLES_DIR", "REPORTS_DIR", "EXCELS_DIR", "RESULTS_DIR"):
        app.config[key].mkdir(parents=True, exist_ok=True)

    report_service = ReportService(app.config["RESULTS_DIR"])
    app.extensions["report_service"] = report_service
    app.extensions["cuckoo_service"] = CuckooService(app.config, report_service)

    app.register_blueprint(upload_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(predict_bp)

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", service="cuckoo-web-api")

    @app.errorhandler(413)
    def too_large(_error):
        return jsonify(error="File vuot qua gioi han upload."), 413

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
    )
