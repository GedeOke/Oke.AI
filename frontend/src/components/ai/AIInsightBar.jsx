import AITag from "./AITag.jsx";

export default function AIInsightBar({ intent, sentiment, safety }) {
  return (
    <div className="flex items-center gap-2 flex-wrap">
      <AITag label={intent || "unknown"} color="indigo" />
      <AITag label={sentiment || "neutral"} color="emerald" />
      <AITag label={safety?.safe === false ? "Unsafe" : "Safe"} color={safety?.safe === false ? "amber" : "slate"} />
    </div>
  );
}
