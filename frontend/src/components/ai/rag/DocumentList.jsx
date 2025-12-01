import Button from "../../ui/Button.jsx";

export default function DocumentList({ documents, onSelect }) {
  return (
    <div className="space-y-2">
      <h3 className="text-sm font-semibold text-slate-800">Documents</h3>
      <div className="space-y-2">
        {(documents || []).map((doc) => (
          <div
            key={doc.id}
            className="flex items-center justify-between rounded-xl border border-slate-200 bg-white px-3 py-2"
          >
            <div>
              <p className="text-sm font-medium text-slate-800">{doc.title || "Untitled"}</p>
              <p className="text-xs text-slate-500">{doc.source || "upload"}</p>
            </div>
            <Button variant="secondary" onClick={() => onSelect(doc)}>
              Preview
            </Button>
          </div>
        ))}
        {(!documents || documents.length === 0) && <p className="text-sm text-slate-500">Belum ada dokumen.</p>}
      </div>
    </div>
  );
}
