import Card from "../ui/Card";

export default function AIResultPanel({ result }) {
  if (!result) return <Card>Belum ada hasil.</Card>;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <Card>
        <h3 className="text-sm font-semibold mb-2">Reply</h3>
        <p className="text-gray-800 whitespace-pre-wrap">{result.reply || "-"}</p>
      </Card>
      <Card>
        <h3 className="text-sm font-semibold mb-2">Intent</h3>
        <p className="text-gray-800">{result.classification?.intent || "-"}</p>
        <h3 className="text-sm font-semibold mt-4 mb-2">Sentiment</h3>
        <p className="text-gray-800">{result.sentiment || "-"}</p>
      </Card>
      <Card>
        <h3 className="text-sm font-semibold mb-2">RAG Chunks</h3>
        <pre className="text-xs bg-gray-50 p-3 rounded-lg overflow-auto max-h-64 whitespace-pre-wrap">
{(result.chunks || result.rag_chunks || []).map((c) => (typeof c === "string" ? c : c.content)).join("\n\n") || "-"}
        </pre>
      </Card>
      <Card>
        <h3 className="text-sm font-semibold mb-2">Function Planner</h3>
        <pre className="text-xs bg-gray-50 p-3 rounded-lg overflow-auto max-h-64 whitespace-pre-wrap">
{JSON.stringify(result.action || {}, null, 2)}
        </pre>
        <h3 className="text-sm font-semibold mt-4 mb-2">Safety</h3>
        <pre className="text-xs bg-gray-50 p-3 rounded-lg overflow-auto whitespace-pre-wrap">
{JSON.stringify(result.safety || {}, null, 2)}
        </pre>
      </Card>
    </div>
  );
}
