import { useEffect, useState } from "react";
import Card from "../../components/ui/Card.jsx";
import ToolList from "../../components/ai/tools/ToolList.jsx";
import ToolConfigForm from "../../components/ai/tools/ToolConfigForm.jsx";
import { fetchTools, updateTools } from "../../lib/toolsApi";
import Button from "../../components/ui/Button.jsx";

export default function Tools() {
  const [tools, setTools] = useState([]);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    const load = async () => {
      const data = await fetchTools();
      setTools(data || []);
    };
    load();
  }, []);

  const toggleTool = (tool) => {
    const updated = tools.map((t) => (t.id === tool.id ? { ...t, enabled: !t.enabled } : t));
    setTools(updated);
  };

  const saveTools = async () => {
    await updateTools({ tools });
  };

  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs font-semibold text-indigo-600 uppercase tracking-[0.3em]">AI Tools</p>
        <h1 className="text-2xl font-semibold text-slate-900">Function Calling Manager</h1>
        <p className="text-sm text-slate-500">Aktifkan tools, konfigurasi schema, dan test planner.</p>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card>
          <ToolList tools={tools} onToggle={toggleTool} onConfigure={setSelected} />
          <Button className="mt-4" onClick={saveTools}>
            Save Tools
          </Button>
        </Card>
        <Card>
          <ToolConfigForm tool={selected} onSave={saveTools} />
        </Card>
      </div>
    </div>
  );
}
