import Button from "../../ui/Button.jsx";

export default function ResponseDetailDrawer({ open, log, onClose }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-end z-50">
      <div className="w-full max-w-lg bg-white h-full shadow-2xl border-l border-slate-200 p-4 overflow-y-auto">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-slate-800">Log Detail</h3>
          <Button variant="secondary" onClick={onClose}>
            Close
          </Button>
        </div>
        <div className="space-y-3 text-sm text-slate-700">
          <pre className="bg-slate-50 border border-slate-200 rounded-xl p-3 whitespace-pre-wrap overflow-auto">
{JSON.stringify(log || {}, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
}
