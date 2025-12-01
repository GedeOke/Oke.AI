import { Link, useLocation } from "react-router-dom";

const navItems = [
  { to: "/ai", label: "AI Playground" },
  { to: "/inbox", label: "Inbox" },
];

export default function Sidebar({ onSelect }) {
  const location = useLocation();
  return (
    <aside className="w-full md:w-64 p-4 bg-white h-full shadow-lg">
      <div className="space-y-2">
        <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-[0.2em]">Navigation</h2>
        <nav className="space-y-2">
          {navItems.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              onClick={onSelect}
              className={`block w-full text-left px-3 py-2 rounded-xl text-sm font-medium transition ${
                location.pathname === item.to
                  ? "bg-gradient-to-r from-indigo-500 to-blue-500 text-white shadow-md"
                  : "text-slate-700 hover:bg-slate-100"
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
