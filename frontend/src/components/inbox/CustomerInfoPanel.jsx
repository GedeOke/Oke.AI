export default function CustomerInfoPanel({ customer }) {
  if (!customer) {
    return (
      <div className="glass-card rounded-2xl p-4">
        <h3 className="text-sm font-semibold text-slate-800">Customer Info</h3>
        <p className="text-sm text-slate-500 mt-2">Pilih percakapan untuk melihat detail.</p>
      </div>
    );
  }

  return (
    <div className="glass-card rounded-2xl p-4 space-y-3">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center font-semibold">
          {customer.name?.[0] || customer.email?.[0] || "C"}
        </div>
        <div>
          <p className="text-sm font-semibold text-slate-800">{customer.name || "Customer"}</p>
          <p className="text-xs text-slate-500">{customer.email || customer.phone || "-"}</p>
        </div>
      </div>
      <div className="text-xs text-slate-600 space-y-1">
        <div><span className="font-semibold">Phone:</span> {customer.phone || "-"}</div>
        <div><span className="font-semibold">Email:</span> {customer.email || "-"}</div>
        <div><span className="font-semibold">Source:</span> {customer.source || "whatsapp"}</div>
      </div>
    </div>
  );
}
