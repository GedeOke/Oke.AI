const navItems = [
  { key: "ai", label: "AI Playground" },
  { key: "inbox", label: "Inbox" },
];

export default function Sidebar({ current, onSelect }) {
  return (
    <aside className="w-full md:w-64 bg-white border-r border-gray-200 p-4">
      <h2 className="text-lg font-semibold mb-4">OkeAI Dashboard</h2>
      <nav className="space-y-2">
        {navItems.map((item) => (
          <button
            key={item.key}
            onClick={() => onSelect(item.key)}
            className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium ${
              current === item.key ? "bg-indigo-600 text-white" : "hover:bg-gray-100"
            }`}
          >
            {item.label}
          </button>
        ))}
      </nav>
    </aside>
  );
}
