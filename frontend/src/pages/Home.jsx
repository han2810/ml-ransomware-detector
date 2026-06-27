import { Link } from "react-router-dom";

export default function Home() {
  return <section className="hero">
    <span className="eyebrow">AUTOMATED MALWARE ANALYSIS</span>
    <h1>Phân tích ransomware</h1>
    <p>Gửi mẫu tới Cuckoo Sandbox, trích xuất đặc trưng hành vi và nhận dự đoán từ mô hình máy học trong một quy trình duy nhất.</p>
    <div className="actions"><Link className="primary button-link" to="/submit">Phân tích mẫu</Link><Link className="secondary button-link" to="/history">Xem lịch sử</Link></div>
    <div className="feature-grid">
      <article><b>01</b><h3>Cuckoo Sandbox</h3><p>Mẫu chỉ được thực thi trong môi trường sandbox.</p></article>
      <article><b>02</b><h3>9 nhóm đặc trưng</h3><p>API, registry, file, network, signature và nhiều hơn.</p></article>
      <article><b>03</b><h3>ML Prediction</h3><p>Chuẩn hóa đặc trưng và dự đoán tự động.</p></article>
    </div>
  </section>;
}

