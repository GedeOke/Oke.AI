export default function PersonaEditor({ value, onChange }) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-slate-700">Persona & Instructions</label>
      <textarea
        rows={4}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Tuliskan persona, gaya bahasa, dan rules..."
        className="w-full rounded-xl border border-slate-200 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
      />
    </div>
  );
}
