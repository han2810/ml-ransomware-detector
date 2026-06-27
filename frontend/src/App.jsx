import { NavLink, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import SubmitPage from "./pages/SubmitPage";
import TaskDetailPage from "./pages/TaskDetailPage";
import HistoryPage from "./pages/HistoryPage";

export default function App() {
  return <>
    <header className="topbar">
      <NavLink className="brand" to="/">CUCKOO<span>WEB</span></NavLink>
      <nav>
        <NavLink to="/submit">Phân tích</NavLink>
        <NavLink to="/history">Lịch sử</NavLink>
      </nav>
    </header>
    <main className="container">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/submit" element={<SubmitPage />} />
        <Route path="/tasks/:taskId" element={<TaskDetailPage />} />
        <Route path="/history" element={<HistoryPage />} />
      </Routes>
    </main>
  </>;
}

