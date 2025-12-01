import { useState } from "react";
import Sidebar from "./components/layout/Sidebar.jsx";
import Topbar from "./components/layout/Topbar.jsx";
import AiPlayground from "./pages/AiPlayground.jsx";
import Inbox from "./pages/Inbox.jsx";

function App() {
  const [page, setPage] = useState("ai");

  return (
    <div className="min-h-screen bg-gray-100">
      <Topbar />
      <div className="flex flex-col md:flex-row">
        <Sidebar current={page} onSelect={setPage} />
        <main className="flex-1 p-4">
          {page === "ai" ? <AiPlayground /> : <Inbox />}
        </main>
      </div>
    </div>
  );
}

export default App;
