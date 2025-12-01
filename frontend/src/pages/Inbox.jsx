import { useEffect } from "react";
import ConversationList from "../components/inbox/ConversationList.jsx";
import MessageList from "../components/inbox/MessageList.jsx";
import MessageInput from "../components/inbox/MessageInput.jsx";
import Card from "../components/ui/Card.jsx";
import { useConversations } from "../hooks/useConversations.js";

export default function Inbox() {
  const { conversations, messages, activeId, selectConversation, send, loading } = useConversations();

  useEffect(() => {
    if (conversations?.length && !activeId) {
      selectConversation(conversations[0].id);
    }
  }, [conversations]);

  return (
    <div className="space-y-3">
      <div>
        <p className="text-xs font-semibold text-indigo-600 uppercase tracking-wide">Inbox</p>
        <h1 className="text-2xl font-semibold text-slate-900">Percakapan</h1>
        <p className="text-sm text-slate-500">Pantau dan kirim pesan, lihat balasan AI jika ada.</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-[280px_1fr] gap-4 h-full">
        <Card className="h-full">
          <h2 className="text-sm font-semibold mb-3">Conversations</h2>
          <ConversationList conversations={conversations} activeId={activeId} onSelect={selectConversation} />
        </Card>
        <div className="space-y-3">
          <MessageList messages={messages} />
          <Card>
            <MessageInput onSend={send} loading={loading} />
          </Card>
        </div>
      </div>
    </div>
  );
}
