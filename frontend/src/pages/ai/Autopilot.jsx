import { useEffect, useState } from "react";
import Card from "../../components/ui/Card.jsx";
import AutoReplyToggle from "../../components/ai/autopilot/AutoReplyToggle.jsx";
import AutopilotRules from "../../components/ai/autopilot/AutopilotRules.jsx";
import TimeSettings from "../../components/ai/autopilot/TimeSettings.jsx";
import Button from "../../components/ui/Button.jsx";
import { fetchAutopilot, updateAutopilot } from "../../lib/autopilotApi";
import { getErrorMessage } from "../../lib/error";

export default function Autopilot() {
  const [config, setConfig] = useState({ enabled: false, rules: [], hours: { start: 9, end: 17 } });
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchAutopilot();
        if (data) {
          setConfig({
            enabled: data.enabled ?? false,
            rules: data.rules || [],
            hours: data.hours || { start: 9, end: 17 },
          });
        }
      } catch (err) {
        setError(getErrorMessage(err));
      }
    };
    load();
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      await updateAutopilot(config);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs font-semibold text-indigo-600 uppercase tracking-[0.3em]">Autopilot</p>
        <h1 className="text-2xl font-semibold text-slate-900">Autopilot Settings</h1>
        <p className="text-sm text-slate-500">Atur autoreply, jam operasional, dan rules intent.</p>
      </div>
      {error && <p className="text-sm text-red-500">Note: {error} (endpoint mungkin belum tersedia)</p>}
      <Card className="space-y-4">
        <AutoReplyToggle enabled={config.enabled} onChange={(v) => setConfig({ ...config, enabled: v })} />
        <TimeSettings hours={config.hours} onChange={(hours) => setConfig({ ...config, hours })} />
        <AutopilotRules rules={config.rules} onChange={(rules) => setConfig({ ...config, rules })} />
        <Button onClick={handleSave} disabled={saving}>
          {saving ? "Saving..." : "Save Autopilot"}
        </Button>
      </Card>
    </div>
  );
}
