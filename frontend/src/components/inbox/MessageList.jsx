import { useEffect, useRef } from "react";
import MessageItem from "./MessageItem.jsx";

export default function MessageList({ messages }) {
  const ref = useRef(null);

  useEffect(() => {
    if (ref.current) {
      ref.current.scrollTop = ref.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div ref={ref} className="h-[520px] overflow-y-auto space-y-3 p-3 bg-white border border-gray-200 rounded-xl">
      {(messages || []).map((msg) => (
        <MessageItem key={msg.id} message={msg} />
      ))}
      {(!messages || messages.length === 0) && (
        <p className="text-sm text-gray-500">No messages yet.</p>
      )}
    </div>
  );
}
