import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import FileUpload from "../components/FileUpload";
import { getModels, uploadSample } from "../services/api";

export default function SubmitPage() {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [models, setModels] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    getModels()
      .then((data) => setModels(data.models || []))
      .catch((err) => setError(err.message));
  }, []);

  const submit = async (file, modelId) => {
    setBusy(true); setError("");
    try { const task = await uploadSample(file, modelId); navigate(`/tasks/${task.task_id}`); }
    catch (err) { setError(err.message); setBusy(false); }
  };

  return <section className="narrow"><span className="eyebrow">NEW ANALYSIS</span><h1>Gửi mẫu phân tích</h1>
    <p className="muted">Không tải lên dữ liệu cá nhân hoặc file không được phép kiểm thử.</p>
    <FileUpload onSubmit={submit} busy={busy} models={models} />{error && <p className="error">{error}</p>}
  </section>;
}
