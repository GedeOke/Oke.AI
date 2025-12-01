import Card from "../ui/Card.jsx";
import AITag from "../ai/AITag.jsx";
import AIInsightBar from "../ai/AIInsightBar.jsx";

export default function AIToolsPanel({ aiData }) {
  const reply = aiData?.reply || "-";
  const intent = aiData?.classification?.intent || "unknown";
  const sentiment = aiData?.sentiment || "neutral";

  return (
    <div className="space-y-3">
      <Card className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-800">AI Summary</h3>
          <AIInsightBar intent={intent} sentiment={sentiment} safety={aiData?.safety} />
        </div>
        <p className="text-sm text-slate-600 leading-relaxed">{reply}</p>
      </Card>
      <Card className="space-y-2">
        <h3 className="text-sm font-semibold text-slate-800">Badges</h3>
        <div className="flex flex-wrap gap-2">
          <AITag label={`Intent: ${intent}`} />
          <AITag label={`Sentiment: ${sentiment}`} />
          <AITag label={`Auto Reply: ${aiData?.should_auto_reply ? "Yes" : "No"}`} />
        </div>
      </Card>
    </div>
  );
}
