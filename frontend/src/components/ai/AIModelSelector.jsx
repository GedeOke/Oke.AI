import Input from "../ui/Input";

const PROVIDERS = [
  { value: "openai", label: "OpenAI" },
  { value: "groq", label: "Groq" },
  { value: "gemini", label: "Gemini" },
];

export default function AIModelSelector({ provider, model, onProviderChange, onModelChange }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
      <div>
        <label className="text-sm font-medium text-gray-700">Provider</label>
        <select
          value={provider}
          onChange={(e) => onProviderChange(e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
        >
          {PROVIDERS.map((p) => (
            <option key={p.value} value={p.value}>
              {p.label}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label className="text-sm font-medium text-gray-700">Model</label>
        <Input
          className="mt-1"
          value={model}
          onChange={(e) => onModelChange(e.target.value)}
          placeholder="e.g. gpt-4o-mini"
        />
      </div>
    </div>
  );
}
