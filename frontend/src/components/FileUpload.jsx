import { useRef, useState } from "react";

export default function FileUpload({ onSubmit, busy }) {
  const inputRef = useRef();
  const [file, setFile] = useState(null);
  const select = (event) => setFile(event.target.files?.[0] || null);

  return <div className="upload-card">
    <div className="upload-icon">↑</div>
    <h2>Chọn mẫu cần phân tích</h2>
    <p>Hỗ trợ EXE, DLL, MSI, SCR, COM và BIN — tối đa 100 MB.</p>
    <input ref={inputRef} hidden type="file" onChange={select} />
    <button className="secondary" onClick={() => inputRef.current.click()}>Chọn file</button>
    {file && <div className="selected-file"><span>{file.name}</span><small>{(file.size / 1024 / 1024).toFixed(2)} MB</small></div>}
    <button className="primary" disabled={!file || busy} onClick={() => onSubmit(file)}>
      {busy ? "Đang tải lên…" : "Bắt đầu phân tích"}
    </button>
  </div>;
}

