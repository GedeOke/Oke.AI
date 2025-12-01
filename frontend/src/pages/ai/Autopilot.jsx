import { useEffect, useState } from "react";
import Card from "../../components/ui/Card.jsx";
import AutoReplyToggle from "../../components/ai/autopilot/AutoReplyToggle.jsx";
import AutopilotRules from "../../components/ai/autopilot/AutopilotRules.jsx";
import TimeSettings from "../../components/ai/autopilot/TimeSettings.jsx";
import { fetchAutopilot, updateAutopilot } from "../../lib/autopilotApi";
import Button from "../../components/ui/Button.jsx";

export default function Autopilot() {
  const [config, setConfig] = useState({ enabled: false, rules: [], hours: { start: 9, end: 17 } });

  useEffect(() => {
    const load = async () => {
      const data = await fetchAutopilot();
      setConfig({
        enabled: data?.enabled ?? false,
        rules: data?.rules || [],
        hours: data?.hours || { start: 9, end: 17 },
      });
    };
    load();
  }, []);

  const handleSave = async () => {
    await updateAutopilot(config);
  };

  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs font-semibold text-indigo-600 uppercase tracking-[0.3em]">Autopilot</p>
        <h1 className="text-2xl font-semibold text-slate-900">Autopilot Settings</h1>
        <p className="text-sm text-slate-500">Atur autoreply, jam operasional, dan rules intent.</p>
      </div>
      <Card className="space-y-4">
        <AutoReplyToggle enabled={config.enabled} onChange={(v) => setConfig({ ...config, enabled: v })} />
        <TimeSettings hours={config.hours} onChange={(hours) => setConfig({ ...config, hours })} />
        <AutopilotRules rules={config.rules} onChange={(rules) => setConfig({ ...config, rules })} />
        <Button onClick={handleSave}>Save Autopilot</Button>
      </Card>
    </div>
  );
}
