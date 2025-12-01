import ToolCard from "./ToolCard.jsx";

export default function ToolList({ tools, onToggle, onConfigure }) {
  return (
    <div className="space-y-2">
      {(tools || []).map((tool) => (
        <ToolCard key={tool.id} tool={tool} onToggle={onToggle} onConfigure={onConfigure} />
      ))}
      {(!tools || tools.length === 0) && <p className="text-sm text-slate-500">Belum ada tools.</p>}
    </div>
  );
}
