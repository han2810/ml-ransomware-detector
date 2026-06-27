const API_BASE = import.meta.env.VITE_API_URL || "/api";

async function request(path, options) {
  const response = await fetch(`${API_BASE}${path}`, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return data;
}

export function uploadSample(file, modelId) {
  const body = new FormData();
  body.append("file", file);
  body.append("model_id", modelId);
  return request("/upload", { method: "POST", body });
}

export const getModels = () => request("/models");
export const getTasks = () => request("/tasks");
export const getTask = (id) => request(`/tasks/${id}`);
export const predictAgain = (id) => request(`/predict/${id}`, { method: "POST" });
export const artifactUrl = (path) => `${API_BASE}${path.replace(/^\/api/, "")}`;
