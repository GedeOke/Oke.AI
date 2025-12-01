import { useState } from "react";
import Button from "../../ui/Button.jsx";
import Textarea from "../../ui/Textarea.jsx";

export default function RagTestConsole({ onTest, result }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const handleTest = async () => {
    setLoading(true);
    await onTest(query);
    setLoading(false);
  };

  return (
    <div className="space-y-3">
      <Textarea
        rows={3}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Coba query RAG..."
      />
      <Button onClick={handleTest} disabled={loading || !query.trim()}>
        {loading ? "Testing..." : "Test RAG"}
      </Button>
      {result && (
        <div className="rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm text-slate-700 space-y-2">
          <div>
            <span className="font-semibold">Chunks:</span>
            <pre className="text-xs bg-white border border-slate-200 rounded-xl p-2 whitespace-pre-wrap">
{JSON.stringify(result.chunks || [], null, 2)}
            </pre>
          </div>
          <div>
            <span className="font-semibold">Answer:</span>
            <p>{result.answer || "-"}</p>
          </div>
        </div>
      )}
    </div>
  );
}
