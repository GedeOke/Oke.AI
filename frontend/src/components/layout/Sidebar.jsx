import { Link, useLocation } from "react-router-dom";

const navItems = [
  { to: "/ai", label: "AI Playground" },
  { to: "/inbox", label: "Inbox" },
];

export default function Sidebar() {
  const location = useLocation();
  return (
    <aside className="w-full md:w-64 p-4">
      <div className="glass-card rounded-2xl border border-white/10 p-4 space-y-2">
        <h2 className="text-sm font-semibold text-slate-50">Navigation</h2>
        <nav className="space-y-2">
          {navItems.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={`block w-full text-left px-3 py-2 rounded-xl text-sm font-medium transition ${
                location.pathname === item.to
                  ? "bg-gradient-to-r from-indigo-500 to-sky-500 text-white shadow-md shadow-indigo-500/30"
                  : "text-slate-100 hover:bg-white/10"
              }`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>
    </aside>
  );
}
