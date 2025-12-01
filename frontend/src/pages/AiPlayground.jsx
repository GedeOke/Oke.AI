import { useState } from "react";
import Card from "../components/ui/Card.jsx";
import Textarea from "../components/ui/Textarea.jsx";
import Button from "../components/ui/Button.jsx";
import AIModelSelector from "../components/ai/AIModelSelector.jsx";
import AIResultPanel from "../components/ai/AIResultPanel.jsx";
import AIPayloadViewer from "../components/ai/AIPayloadViewer.jsx";
import { useAi } from "../hooks/useAi.js";
import { useOrganization } from "../context/OrganizationContext.jsx";

export default function AiPlayground() {
  const [message, setMessage] = useState("");
  const [provider, setProvider] = useState("openai");
  const [model, setModel] = useState("gpt-4o-mini");
  const { run, loading, result, error } = useAi();
  const { organizationId } = useOrganization();

  const payload = {
    organization_id: organizationId,
    message,
    model_provider: provider,
    model,
  };

  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs font-semibold text-indigo-600 uppercase tracking-[0.25em]">AI Engine</p>
        <h1 className="text-3xl font-semibold text-slate-900">AI Playground</h1>
        <p className="text-sm text-slate-600">Uji prompt, pilih provider, lihat hasil lengkap (RAG, planner, safety).</p>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card className="space-y-4">
          <AIModelSelector
            provider={provider}
            model={model}
            onProviderChange={setProvider}
            onModelChange={setModel}
          />
          <div>
            <label className="text-sm font-medium text-slate-800">Prompt</label>
            <Textarea
              rows={5}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Tuliskan pesan untuk AI..."
              className="mt-2"
            />
          </div>
          <Button onClick={() => run({ message, model_provider: provider, model })} disabled={loading}>
            {loading ? "Running..." : "Run AI"}
          </Button>
          {error && <p className="text-sm text-red-500">Error: {JSON.stringify(error)}</p>}
        </Card>
        <AIPayloadViewer payload={payload} />
      </div>

      <AIResultPanel result={result} />
    </div>
  );
}
