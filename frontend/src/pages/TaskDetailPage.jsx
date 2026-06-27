import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import ProgressBox from "../components/ProgressBox";
import ResultCard from "../components/ResultCard";
import { getTask } from "../services/api";

export default function TaskDetailPage() {
  const { taskId } = useParams();
  const [task, setTask] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let timer; let active = true;
    const load = async () => {
      try {
        const value = await getTask(taskId); if (!active) return; setTask(value);
        if (!["completed", "failed"].includes(value.status)) timer = setTimeout(load, 2500);
      } catch (err) { if (active) setError(err.message); }
    };
    load(); return () => { active = false; clearTimeout(timer); };
  }, [taskId]);
  if (error) return <p className="error">{error}</p>;
  if (!task) return <p className="muted">Đang tải task…</p>;
  return <section className="narrow"><Link className="back" to="/history">← Lịch sử</Link>
    <span className="eyebrow">TASK {task.task_id.slice(0, 8)}</span><h1>{task.filename}</h1>
    <ProgressBox task={task} /><ResultCard task={task} />
  </section>;
}

