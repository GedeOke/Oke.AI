export default function AITag({ label, color = "indigo" }) {
  const colorMap = {
    indigo: "bg-indigo-100 text-indigo-700 border-indigo-200",
    emerald: "bg-emerald-100 text-emerald-700 border-emerald-200",
    amber: "bg-amber-100 text-amber-700 border-amber-200",
    slate: "bg-slate-100 text-slate-700 border-slate-200",
  };
  return (
    <span className={`text-xs font-semibold px-3 py-1 rounded-full border ${colorMap[color] || colorMap.indigo}`}>
      {label}
    </span>
  );
}
