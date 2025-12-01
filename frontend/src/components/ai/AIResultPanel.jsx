import Card from "../ui/Card";
import AIInsightBar from "./AIInsightBar.jsx";

export default function AIResultPanel({ result }) {
  if (!result) return <Card>Belum ada hasil.</Card>;

  const ragText =
    (result.chunks || result.rag_chunks || [])
      .map((c) => (typeof c === "string" ? c : c.content))
      .join("\n\n") || "Tidak ada RAG yang relevan.";

  return (
    <div className="space-y-4">
      <Card className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-800">AI Reply</h3>
          <AIInsightBar intent={result.classification?.intent} sentiment={result.sentiment} safety={result.safety} />
        </div>
        <p className="text-slate-800 whitespace-pre-wrap leading-relaxed">{result.reply || "-"}</p>
      </Card>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card>
          <h3 className="text-sm font-semibold mb-2 text-slate-800">RAG Chunks</h3>
          <pre className="text-xs bg-slate-50 border border-slate-200 p-3 rounded-xl overflow-auto max-h-64 whitespace-pre-wrap text-slate-700">
{ragText}
          </pre>
        </Card>
        <Card className="space-y-3">
          <div>
            <h3 className="text-sm font-semibold mb-1 text-slate-800">Function Planner</h3>
            <pre className="text-xs bg-slate-50 border border-slate-200 p-3 rounded-xl overflow-auto max-h-64 whitespace-pre-wrap text-slate-700">
{JSON.stringify(result.action || {}, null, 2)}
            </pre>
          </div>
          <div>
            <h3 className="text-sm font-semibold mb-1 text-slate-800">Safety</h3>
            <pre className="text-xs bg-slate-50 border border-slate-200 p-3 rounded-xl overflow-auto whitespace-pre-wrap text-slate-700">
{JSON.stringify(result.safety || {}, null, 2)}
            </pre>
          </div>
        </Card>
      </div>
    </div>
  );
}
