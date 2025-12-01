export default function ParameterSliders({ params, onChange }) {
  const sliders = [
    { key: "temperature", label: "Temperature", min: 0, max: 1, step: 0.01 },
    { key: "top_p", label: "Top P", min: 0, max: 1, step: 0.01 },
    { key: "max_tokens", label: "Max Tokens", min: 16, max: 2048, step: 16 },
    { key: "frequency_penalty", label: "Frequency Penalty", min: -2, max: 2, step: 0.1 },
    { key: "presence_penalty", label: "Presence Penalty", min: -2, max: 2, step: 0.1 },
  ];

  const handleChange = (key, value) => {
    onChange({ ...params, [key]: Number(value) });
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {sliders.map((s) => (
        <div key={s.key}>
          <label className="text-sm font-medium text-slate-700">
            {s.label}: <span className="text-slate-500">{params[s.key] ?? 0}</span>
          </label>
          <input
            type="range"
            min={s.min}
            max={s.max}
            step={s.step}
            value={params[s.key] ?? 0}
            onChange={(e) => handleChange(s.key, e.target.value)}
            className="w-full accent-indigo-500"
          />
        </div>
      ))}
    </div>
  );
}
