export default function AutopilotRules({ rules, onChange }) {
  const updateRule = (index, field, value) => {
    const updated = [...rules];
    updated[index] = { ...updated[index], [field]: value };
    onChange(updated);
  };

  const addRule = () => {
    onChange([...(rules || []), { intent: "", action: "auto_reply" }]);
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-800">Intent-based Rules</h3>
        <button
          type="button"
          onClick={addRule}
          className="text-xs text-indigo-600 font-semibold"
        >
          + Add Rule
        </button>
      </div>
      {(rules || []).map((rule, idx) => (
        <div key={idx} className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-xs text-slate-600">Intent</label>
            <input
              value={rule.intent}
              onChange={(e) => updateRule(idx, "intent", e.target.value)}
              className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
              placeholder="e.g. faq"
            />
          </div>
          <div>
            <label className="text-xs text-slate-600">Action</label>
            <select
              value={rule.action}
              onChange={(e) => updateRule(idx, "action", e.target.value)}
              className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm"
            >
              <option value="auto_reply">Auto Reply</option>
              <option value="route_agent">Route to Agent</option>
              <option value="escalate">Escalate</option>
            </select>
          </div>
        </div>
      ))}
      {(!rules || rules.length === 0) && <p className="text-sm text-slate-500">Belum ada rules.</p>}
    </div>
  );
}
