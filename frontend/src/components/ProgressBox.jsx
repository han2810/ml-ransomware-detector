const labels = {
  queued: "Trong hàng đợi", submitting: "Đang gửi mẫu", analysing: "Cuckoo đang phân tích",
  extracting: "Trích xuất đặc trưng", predicting: "Đang dự đoán",
  completed: "Hoàn tất", failed: "Thất bại",
};

export default function ProgressBox({ task }) {
  return <section className="panel">
    <div className="row"><h2>{labels[task.status] || task.status}</h2><strong>{task.progress || 0}%</strong></div>
    <div className="progress"><span style={{ width: `${task.progress || 0}%` }} /></div>
    <p className="muted">{task.message}</p>
    {task.error && <p className="error">{task.error}</p>}
  </section>;
}

