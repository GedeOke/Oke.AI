export default function MetricsCards({ metrics }) {
  const cards = [
    { label: "Avg Latency", value: metrics?.avg_latency ? `${metrics.avg_latency} ms` : "-" },
    { label: "RAG Coverage", value: metrics?.rag_coverage ? `${metrics.rag_coverage}%` : "-" },
    { label: "Safety Compliance", value: metrics?.safety_compliance ? `${metrics.safety_compliance}%` : "-" },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
      {cards.map((c) => (
        <div key={c.label} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <p className="text-xs uppercase text-slate-500 tracking-wide font-semibold">{c.label}</p>
          <p className="text-lg font-semibold text-slate-900">{c.value}</p>
        </div>
      ))}
    </div>
  );
}
