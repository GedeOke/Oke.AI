export default function ModelSelector({ provider, model, onProviderChange, onModelChange }) {
  const providers = [
    { value: "openai", label: "OpenAI" },
    { value: "groq", label: "Groq" },
    { value: "gemini", label: "Gemini" },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label className="text-sm font-medium text-slate-700">Provider</label>
        <select
          value={provider}
          onChange={(e) => onProviderChange(e.target.value)}
          className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
        >
          {providers.map((p) => (
            <option key={p.value} value={p.value}>
              {p.label}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label className="text-sm font-medium text-slate-700">Model</label>
        <input
          value={model}
          onChange={(e) => onModelChange(e.target.value)}
          placeholder="gpt-4o-mini"
          className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
        />
      </div>
    </div>
  );
}
