const tones = ["friendly", "formal", "simple", "professional"];

export default function ToneSelector({ value, onChange }) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-slate-700">Tone</label>
      <div className="flex flex-wrap gap-2">
        {tones.map((tone) => (
          <button
            key={tone}
            type="button"
            onClick={() => onChange(tone)}
            className={`px-3 py-1 rounded-full text-sm border transition ${
              value === tone
                ? "bg-indigo-100 border-indigo-200 text-indigo-700"
                : "bg-white border-slate-200 text-slate-700 hover:bg-slate-50"
            }`}
          >
            {tone}
          </button>
        ))}
      </div>
    </div>
  );
}
