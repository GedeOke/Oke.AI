export default function ConversationList({ conversations, activeId, onSelect }) {
  return (
    <div className="space-y-2">
      {(conversations || []).map((conv) => (
        <button
          key={conv.id}
          onClick={() => onSelect(conv.id)}
          className={`w-full text-left rounded-lg border px-3 py-2 text-sm ${
            activeId === conv.id ? "border-indigo-500 bg-indigo-50" : "border-gray-200 hover:bg-gray-50"
          }`}
        >
          <div className="font-semibold text-gray-800">{conv.customer_id || "Conversation"}</div>
          <div className="text-xs text-gray-500">Status: {conv.status || "open"}</div>
        </button>
      ))}
      {(!conversations || conversations.length === 0) && (
        <p className="text-sm text-gray-500">No conversations yet.</p>
      )}
    </div>
  );
}
