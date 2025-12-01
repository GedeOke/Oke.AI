import Button from "../../ui/Button.jsx";

export default function ChunkPreviewModal({ open, onClose, chunks = [] }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[80vh] overflow-hidden border border-slate-200">
        <div className="p-4 flex items-center justify-between border-b border-slate-200">
          <h3 className="text-sm font-semibold text-slate-800">Preview Chunks</h3>
          <Button variant="ghost" onClick={onClose}>
            Close
          </Button>
        </div>
        <div className="p-4 space-y-3 overflow-y-auto max-h-[70vh]">
          {(chunks || []).map((c, idx) => (
            <div key={idx} className="rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm text-slate-700">
              {c.content || c}
            </div>
          ))}
          {(!chunks || chunks.length === 0) && <p className="text-sm text-slate-500">No chunks found.</p>}
        </div>
      </div>
    </div>
  );
}
