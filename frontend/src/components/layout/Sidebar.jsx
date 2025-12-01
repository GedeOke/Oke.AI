import { Link, useLocation } from "react-router-dom";

const navItems = [
  { to: "/ai", label: "AI Playground" },
  { to: "/inbox", label: "Inbox" },
];

export default function Sidebar() {
  const location = useLocation();
  return (
    <aside className="w-full md:w-64 bg-white border-r border-gray-200 p-4">
      <h2 className="text-lg font-semibold mb-4">OkeAI Dashboard</h2>
      <nav className="space-y-2">
        {navItems.map((item) => (
          <Link
            key={item.to}
            to={item.to}
            className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium ${
              location.pathname === item.to ? "bg-indigo-600 text-white" : "hover:bg-gray-100"
            }`}
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
