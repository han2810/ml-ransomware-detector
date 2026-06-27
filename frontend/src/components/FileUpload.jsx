import { useEffect, useRef, useState } from "react";

export default function FileUpload({ onSubmit, busy, models }) {
  const inputRef = useRef();
  const [file, setFile] = useState(null);
  const [modelId, setModelId] = useState("");
  const select = (event) => setFile(event.target.files?.[0] || null);

  useEffect(() => {
    if (!models.some((model) => model.id === modelId)) {
      setModelId(models[0]?.id || "");
    }
  }, [models, modelId]);

  return <div className="upload-card">
    <div className="upload-icon">↑</div>
    <h2>Chọn mẫu cần phân tích</h2>
    <p>Hỗ trợ EXE, DLL, MSI, SCR, COM và BIN — tối đa 100 MB.</p>
    <input ref={inputRef} hidden type="file" onChange={select} />
    <div className="upload-controls">
      <div className="upload-control">
        <label>Mẫu phân tích</label>
        <button className="secondary" onClick={() => inputRef.current.click()}>Chọn file</button>
      </div>
      <div className="upload-control">
        <label htmlFor="model-select">Model</label>
        <select id="model-select" value={modelId} onChange={(event) => setModelId(event.target.value)}>
          {models.map((model) => <option key={model.id} value={model.id}>{model.name}</option>)}
        </select>
      </div>
    </div>
    {file && <div className="selected-file"><span>{file.name}</span><small>{(file.size / 1024 / 1024).toFixed(2)} MB</small></div>}
    <button className="primary" disabled={!file || busy || !modelId} onClick={() => onSubmit(file, modelId)}>
      {busy ? "Đang tải lên…" : "Bắt đầu phân tích"}
    </button>
  </div>;
}
