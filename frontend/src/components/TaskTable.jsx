import { Link } from "react-router-dom";

export default function TaskTable({ tasks }) {
  if (!tasks.length) return <div className="empty">Chưa có lần phân tích nào.</div>;
  return <div className="table-wrap"><table>
    <thead><tr><th>File</th><th>Trạng thái</th><th>Kết quả</th><th>Thời gian</th><th /></tr></thead>
    <tbody>{tasks.map((task) => <tr key={task.task_id}>
      <td>{task.filename}</td><td><span className={`status ${task.status}`}>{task.status}</span></td>
      <td>{task.prediction || "—"}</td><td>{new Date(task.created_at).toLocaleString("vi-VN")}</td>
      <td><Link to={`/tasks/${task.task_id}`}>Chi tiết →</Link></td>
    </tr>)}</tbody>
  </table></div>;
}

