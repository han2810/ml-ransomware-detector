import json
import time
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor

from .excel_service import ExcelService
from .feature_service import FeatureService
from .predict_service import PredictService


class CuckooService:
    def __init__(self, config, report_service):
        self.base_url = config["CUCKOO_API_URL"]
        self.token = config["CUCKOO_API_TOKEN"]
        self.poll_interval = config["CUCKOO_POLL_INTERVAL"]
        self.analysis_timeout = config["CUCKOO_ANALYSIS_TIMEOUT"]
        self.reports_dir = config["REPORTS_DIR"]
        self.excels_dir = config["EXCELS_DIR"]
        self.report_service = report_service
        self.feature_service = FeatureService(config["MAPPINGS_DIR"])
        self.excel_service = ExcelService()
        self.predict_service = PredictService()
        self._executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="cuckoo")

    def start(self, task_id, sample_path):
        self._executor.submit(self._run, task_id, sample_path)

    def submit_sample(self, sample_path):
        errors = []
        boundary = f"----CuckooWeb{uuid.uuid4().hex}"
        file_bytes = sample_path.read_bytes()
        body = (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"platform\"\r\n\r\nwindows\r\n"
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"priority\"\r\n\r\n2\r\n"
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{sample_path.name}\"\r\n"
            "Content-Type: application/octet-stream\r\n\r\n"
        ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")
        for endpoint in ("/tasks/create/file", "/api/tasks/create/file"):
            try:
                payload = self._request_json(
                    self.base_url + endpoint, data=body, timeout=120,
                    content_type=f"multipart/form-data; boundary={boundary}",
                )
                cuckoo_id = payload.get("task_id") or payload.get("taskid") or payload.get("id")
                if cuckoo_id is None and payload.get("task_ids"):
                    cuckoo_id = payload["task_ids"][0]
                if cuckoo_id is not None:
                    return str(cuckoo_id)
                errors.append(f"{endpoint}: response khong co task_id")
            except (OSError, ValueError, urllib.error.URLError) as exc:
                errors.append(f"{endpoint}: {exc}")
        raise RuntimeError("Khong submit duoc mau len Cuckoo. " + " | ".join(errors))

    def task_status(self, cuckoo_id):
        for endpoint in (f"/tasks/view/{cuckoo_id}", f"/api/tasks/view/{cuckoo_id}"):
            try:
                payload = self._request_json(self.base_url + endpoint, timeout=30)
                task = payload.get("task", payload.get("data", payload))
                return str(task.get("status", "")).lower()
            except (OSError, ValueError, urllib.error.URLError):
                continue
        raise RuntimeError(f"Khong lay duoc trang thai Cuckoo task {cuckoo_id}.")

    def download_report(self, cuckoo_id, output_path):
        endpoints = (
            f"/tasks/report/{cuckoo_id}/json", f"/tasks/report/{cuckoo_id}",
            f"/api/tasks/report/{cuckoo_id}/json", f"/api/tasks/report/{cuckoo_id}",
        )
        for endpoint in endpoints:
            try:
                payload = self._request_json(self.base_url + endpoint, timeout=300)
                output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                                       encoding="utf-8")
                return output_path
            except (OSError, ValueError, urllib.error.URLError):
                continue
        raise RuntimeError(f"Khong tai duoc report cua Cuckoo task {cuckoo_id}.")

    def _request_json(self, url, data=None, timeout=30, content_type=None):
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if content_type:
            headers["Content-Type"] = content_type
        request = urllib.request.Request(
            url, data=data, headers=headers, method="POST" if data is not None else "GET"
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8", errors="replace"))

    def _run(self, task_id, sample_path):
        try:
            self.report_service.update_task(task_id, status="submitting", progress=5,
                                            message="Dang gui mau len Cuckoo...")
            cuckoo_id = self.submit_sample(sample_path)
            self.report_service.update_task(task_id, cuckoo_task_id=cuckoo_id,
                                            status="analysing", progress=15,
                                            message="Cuckoo dang phan tich mau...")

            started = time.monotonic()
            while time.monotonic() - started < self.analysis_timeout:
                status = self.task_status(cuckoo_id)
                if status == "reported":
                    break
                if status in {"failed", "failed_analysis", "failed_processing", "failed_reporting"}:
                    raise RuntimeError(f"Cuckoo phan tich that bai: {status}")
                elapsed = time.monotonic() - started
                progress = min(75, 15 + int(elapsed / self.analysis_timeout * 60))
                self.report_service.update_task(task_id, progress=progress,
                                                message=f"Cuckoo: {status or 'dang cho'}")
                time.sleep(self.poll_interval)
            else:
                raise TimeoutError("Qua thoi gian cho Cuckoo phan tich.")

            report_path = self.reports_dir / f"{task_id}.json"
            self.download_report(cuckoo_id, report_path)
            self.report_service.update_task(task_id, status="extracting", progress=82,
                                            report_path=str(report_path),
                                            message="Dang trich xuat dac trung...")
            frame, warnings = self.feature_service.build(report_path)
            excel_path = self.excels_dir / f"{task_id}.xlsx"
            self.excel_service.write(frame, excel_path)
            self.report_service.update_task(task_id, status="predicting", progress=95,
                                            excel_path=str(excel_path),
                                            message="Dang du doan...")
            prediction = self.predict_service.predict(frame)
            self.report_service.update_task(task_id, status="completed", progress=100,
                                            prediction=prediction, warnings=warnings,
                                            message="Phan tich hoan tat.")
        except Exception as exc:
            self.report_service.update_task(task_id, status="failed", message="Phan tich that bai.",
                                            error=str(exc))
