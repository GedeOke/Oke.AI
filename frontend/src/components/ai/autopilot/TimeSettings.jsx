export default function TimeSettings({ hours, onChange }) {
  const update = (field, value) => {
    onChange({ ...hours, [field]: value });
  };

  return (
    <div className="grid grid-cols-2 gap-3">
      <div>
        <label className="text-sm font-medium text-slate-700">Start Hour</label>
        <input
          type="number"
          min={0}
          max={23}
          value={hours.start || 9}
          onChange={(e) => update("start", Number(e.target.value))}
          className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
        />
      </div>
      <div>
        <label className="text-sm font-medium text-slate-700">End Hour</label>
        <input
          type="number"
          min={0}
          max={23}
          value={hours.end || 17}
          onChange={(e) => update("end", Number(e.target.value))}
          className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
        />
      </div>
    </div>
  );
}
