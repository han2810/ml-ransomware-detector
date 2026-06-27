import { useEffect, useState } from "react";
import TaskTable from "../components/TaskTable";
import { getTasks } from "../services/api";

export default function HistoryPage() {
  const [tasks, setTasks] = useState([]); const [error, setError] = useState("");
  useEffect(() => { getTasks().then(setTasks).catch((err) => setError(err.message)); }, []);
  return <section><span className="eyebrow">ANALYSIS LOG</span><h1>Lịch sử phân tích</h1>
    {error ? <p className="error">{error}</p> : <TaskTable tasks={tasks} />}
  </section>;
}
