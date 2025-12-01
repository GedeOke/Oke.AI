import Button from "../../ui/Button.jsx";

export default function AutoReplyToggle({ enabled, onChange }) {
  return (
    <div className="flex items-center justify-between rounded-xl border border-slate-200 bg-white p-4">
      <div>
        <p className="text-sm font-semibold text-slate-800">Autoreply</p>
        <p className="text-xs text-slate-500">Balas otomatis saat agent offline atau intent tertentu.</p>
      </div>
      <Button variant="secondary" onClick={() => onChange(!enabled)}>
        {enabled ? "Disable" : "Enable"}
      </Button>
    </div>
  );
}
