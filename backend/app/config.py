import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
APP_DIR = Path(__file__).resolve().parent


def load_env_file(path):
    """Load simple KEY=VALUE entries without adding a runtime dependency."""
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file(BACKEND_DIR / ".env")


class Config:
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_SIZE_MB", "100")) * 1024 * 1024
    SAMPLES_DIR = APP_DIR / "storage" / "samples"
    REPORTS_DIR = APP_DIR / "storage" / "reports"
    EXCELS_DIR = APP_DIR / "storage" / "excels"
    RESULTS_DIR = APP_DIR / "storage" / "results"
    MAPPINGS_DIR = APP_DIR / "mappings"

    CUCKOO_API_URL = os.getenv("CUCKOO_API_URL", "http://127.0.0.1:8090").rstrip("/")
    CUCKOO_API_TOKEN = os.getenv("CUCKOO_API_TOKEN", "")
    CUCKOO_POLL_INTERVAL = float(os.getenv("CUCKOO_POLL_INTERVAL", "10"))
    CUCKOO_ANALYSIS_TIMEOUT = int(os.getenv("CUCKOO_ANALYSIS_TIMEOUT", "3600"))
    ALLOWED_EXTENSIONS = {
        f".{value.strip().lower().lstrip('.')}"
        for value in os.getenv("ALLOWED_EXTENSIONS", "exe,dll,msi,scr,com,bin").split(",")
        if value.strip()
    }
