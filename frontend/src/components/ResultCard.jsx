import DownloadButton from "./DownloadButton";

export default function ResultCard({ task }) {
  if (task.status !== "completed") return null;
  const dangerous = task.prediction?.toLowerCase() === "ransomware";
  return <section className={`result-card ${dangerous ? "danger" : "safe"}`}>
    <span className="eyebrow">KẾT QUẢ MÔ HÌNH</span>
    <h2>{task.prediction}</h2>
    <p>{dangerous ? "Mẫu có dấu hiệu ransomware. Không chạy file này trên máy thật." : "Mô hình chưa phát hiện dấu hiệu ransomware trong mẫu."}</p>
    <div className="actions">
      <DownloadButton url={task.report_url}>Tải report JSON</DownloadButton>
      <DownloadButton url={task.excel_url}>Tải feature Excel</DownloadButton>
    </div>
    {task.warnings?.length > 0 && <p className="warning">Có {task.warnings.length} cảnh báo mapping.</p>}
  </section>;
}

