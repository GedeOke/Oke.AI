import Button from "../../ui/Button.jsx";

export default function ToolConfigForm({ tool, onSave }) {
  if (!tool) return null;

  const handleSave = () => {
    onSave(tool);
  };

  return (
    <div className="space-y-3">
      <p className="text-sm text-slate-700">Edit konfigurasi untuk <strong>{tool.name}</strong></p>
      <pre className="text-xs bg-slate-50 border border-slate-200 rounded-xl p-3 overflow-auto whitespace-pre-wrap">
{JSON.stringify(tool.schema || {}, null, 2)}
      </pre>
      <Button onClick={handleSave}>Save Tool</Button>
    </div>
  );
}
