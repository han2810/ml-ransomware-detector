import json
from copy import deepcopy
from datetime import datetime, timezone
from threading import RLock


def utc_now():
    return datetime.now(timezone.utc).isoformat()


class ReportService:
    """Persists task metadata as one JSON document per task."""

    def __init__(self, results_dir):
        self.results_dir = results_dir
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self._lock = RLock()

    def _path(self, task_id):
        return self.results_dir / f"{task_id}.json"

    def create_task(self, task):
        now = utc_now()
        task = {**task, "created_at": now, "updated_at": now}
        self._write(task)
        return deepcopy(task)

    def update_task(self, task_id, **changes):
        with self._lock:
            task = self.get_task(task_id)
            if task is None:
                raise KeyError(task_id)
            task.update(changes, updated_at=utc_now())
            self._write(task)
            return deepcopy(task)

    def get_task(self, task_id):
        path = self._path(task_id)
        with self._lock:
            if not path.is_file():
                return None
            return json.loads(path.read_text(encoding="utf-8"))

    def list_tasks(self):
        with self._lock:
            tasks = []
            for path in self.results_dir.glob("*.json"):
                try:
                    tasks.append(json.loads(path.read_text(encoding="utf-8")))
                except (json.JSONDecodeError, OSError):
                    continue
        return sorted(tasks, key=lambda item: item.get("created_at", ""), reverse=True)

    def _write(self, task):
        with self._lock:
            path = self._path(task["task_id"])
            temporary = path.with_suffix(".tmp")
            temporary.write_text(
                json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            temporary.replace(path)

