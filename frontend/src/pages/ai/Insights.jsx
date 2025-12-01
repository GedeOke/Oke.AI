import { useEffect, useState } from "react";
import Card from "../../components/ui/Card.jsx";
import LogsTable from "../../components/ai/insights/LogsTable.jsx";
import ResponseDetailDrawer from "../../components/ai/insights/ResponseDetailDrawer.jsx";
import MetricsCards from "../../components/ai/insights/MetricsCards.jsx";
import { fetchLogs, fetchLogDetail, fetchMetrics } from "../../lib/insightsApi";

export default function Insights() {
  const [logs, setLogs] = useState([]);
  const [metrics, setMetrics] = useState({});
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    const load = async () => {
      const l = await fetchLogs();
      setLogs(l || []);
      const m = await fetchMetrics();
      setMetrics(m || {});
    };
    load();
  }, []);

  const handleSelect = async (log) => {
    const detail = await fetchLogDetail(log.id);
    setSelected(detail || log);
  };

  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs font-semibold text-indigo-600 uppercase tracking-[0.3em]">AI Insights</p>
        <h1 className="text-2xl font-semibold text-slate-900">Logging & Metrics</h1>
        <p className="text-sm text-slate-500">Lihat log AI, prompt, RAG chunks, dan metrik kinerja.</p>
      </div>
      <MetricsCards metrics={metrics} />
      <Card>
        <LogsTable logs={logs} onSelect={handleSelect} />
      </Card>
      <ResponseDetailDrawer open={!!selected} log={selected} onClose={() => setSelected(null)} />
    </div>
  );
}
