export default function LogsTable({ logs = [], onSelect }) {
  return (
    <div className="overflow-auto rounded-xl border border-slate-200 bg-white shadow-sm">
      <table className="min-w-full text-sm">
        <thead className="bg-slate-50 text-slate-600">
          <tr>
            <th className="px-3 py-2 text-left">Model</th>
            <th className="px-3 py-2 text-left">Provider</th>
            <th className="px-3 py-2 text-left">Status</th>
            <th className="px-3 py-2 text-left">Created</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log) => (
            <tr
              key={log.id}
              className="border-t border-slate-100 hover:bg-slate-50 cursor-pointer"
              onClick={() => onSelect(log)}
            >
              <td className="px-3 py-2">{log.model || "-"}</td>
              <td className="px-3 py-2">{log.provider || "-"}</td>
              <td className="px-3 py-2">{log.status || "-"}</td>
              <td className="px-3 py-2">{log.created_at || "-"}</td>
            </tr>
          ))}
          {logs.length === 0 && (
            <tr>
              <td className="px-3 py-2 text-slate-500" colSpan={4}>
                Tidak ada log.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
