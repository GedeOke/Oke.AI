export default function ForbiddenTopicsEditor({ topics, onChange }) {
  const update = (value) => onChange(value.split("\n").map((t) => t.trim()).filter(Boolean));

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-slate-700">Forbidden Topics</label>
      <textarea
        rows={4}
        defaultValue={(topics || []).join("\n")}
        onBlur={(e) => update(e.target.value)}
        className="w-full rounded-xl border border-slate-200 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
        placeholder="Kekerasan\nUjaran kebencian\nData sensitif"
      />
    </div>
  );
}
