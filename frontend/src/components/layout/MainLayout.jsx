import { useState } from "react";
import Sidebar from "./Sidebar.jsx";
import Topbar from "./Topbar.jsx";

export default function MainLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Topbar onToggleSidebar={() => setSidebarOpen((v) => !v)} />
      <div className="flex">
        <div className={`fixed z-30 md:static md:block ${sidebarOpen ? "block" : "hidden"} md:w-64 w-64`}>
          <Sidebar onSelect={() => setSidebarOpen(false)} />
        </div>
        <main className="flex-1 md:ml-0 p-4 md:p-6 min-w-0">{children}</main>
      </div>
    </div>
  );
}
