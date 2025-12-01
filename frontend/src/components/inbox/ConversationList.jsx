export default function ConversationList({ conversations, activeId, onSelect }) {
  return (
    <div className="space-y-2">
      {(conversations || []).map((conv) => (
        <button
          key={conv.id}
          onClick={() => onSelect(conv.id)}
          className={`w-full text-left rounded-xl border px-3 py-2 text-sm transition ${
            activeId === conv.id
              ? "border-indigo-500 bg-indigo-50"
              : "border-slate-200 hover:border-indigo-200 hover:bg-indigo-50/50"
          }`}
        >
          <div className="flex items-center justify-between">
            <div className="font-semibold text-slate-800">{conv.customer_id || "Conversation"}</div>
            <span className="text-[11px] text-slate-500">{conv.status || "open"}</span>
          </div>
          <div className="text-xs text-slate-500 truncate">{conv.last_message || "No messages"}</div>
        </button>
      ))}
      {(!conversations || conversations.length === 0) && (
        <p className="text-sm text-gray-500">No conversations yet.</p>
      )}
    </div>
  );
}
