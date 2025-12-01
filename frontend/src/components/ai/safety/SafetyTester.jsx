import { useState } from "react";
import Button from "../../ui/Button.jsx";
import Textarea from "../../ui/Textarea.jsx";

export default function SafetyTester({ onTest, result }) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handle = async () => {
    setLoading(true);
    await onTest(input);
    setLoading(false);
  };

  return (
    <div className="space-y-2">
      <Textarea
        rows={3}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Coba teks untuk safety check..."
      />
      <Button onClick={handle} disabled={loading || !input.trim()}>
        {loading ? "Testing..." : "Test Safety"}
      </Button>
      {result && (
        <div className="rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm text-slate-700">
          {result.safe ? "Safe" : "Unsafe"} - {result.reason || ""}
        </div>
      )}
    </div>
  );
}
