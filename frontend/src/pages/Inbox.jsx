import { useEffect } from "react";
import ConversationList from "../components/inbox/ConversationList.jsx";
import MessageList from "../components/inbox/MessageList.jsx";
import MessageInput from "../components/inbox/MessageInput.jsx";
import Card from "../components/ui/Card.jsx";
import { useConversations } from "../hooks/useConversations.js";
import CustomerInfoPanel from "../components/inbox/CustomerInfoPanel.jsx";
import AIToolsPanel from "../components/inbox/AIToolsPanel.jsx";

export default function Inbox() {
  const { conversations, messages, activeId, selectConversation, send, loading } = useConversations();

  useEffect(() => {
    if (conversations?.length && !activeId) {
      selectConversation(conversations[0].id);
    }
  }, [conversations]);

  const activeConversation = conversations.find((c) => c.id === activeId);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold text-indigo-600 uppercase tracking-[0.3em]">Inbox</p>
          <h1 className="text-2xl font-semibold text-slate-900">Percakapan</h1>
          <p className="text-sm text-slate-500">Pantau & kirim pesan, lihat balasan AI.</p>
        </div>
      </div>
      <div className="grid grid-cols-1 xl:grid-cols-[280px_1.2fr_320px] gap-4 min-h-[600px]">
        <div className="space-y-3">
          <Card className="h-full">
            <h2 className="text-sm font-semibold mb-3 text-slate-800">Conversations</h2>
            <ConversationList conversations={conversations} activeId={activeId} onSelect={selectConversation} />
          </Card>
        </div>
        <div className="space-y-3">
          <MessageList messages={messages} />
          <Card>
            <MessageInput onSend={send} loading={loading} />
          </Card>
        </div>
        <div className="space-y-3 hidden xl:block">
          <CustomerInfoPanel customer={activeConversation} />
          <AIToolsPanel aiData={null} />
        </div>
      </div>
    </div>
  );
}
