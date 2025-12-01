import Button from "../../ui/Button.jsx";

export default function ToolCard({ tool, onToggle, onConfigure }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm space-y-2">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold text-slate-800">{tool.name}</p>
          <p className="text-xs text-slate-500">{tool.description}</p>
        </div>
        <Button variant="secondary" onClick={() => onToggle(tool)}>{tool.enabled ? "Disable" : "Enable"}</Button>
      </div>
      <Button variant="ghost" onClick={() => onConfigure(tool)}>
        Configure
      </Button>
    </div>
  );
}
