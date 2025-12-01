import { useEffect, useState } from "react";
import { getConversations, getMessages, sendMessage } from "../lib/api";

export function useConversations() {
  const [conversations, setConversations] = useState([]);
  const [messages, setMessages] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchConversations = async () => {
    const data = await getConversations();
    setConversations(data || []);
    if (data?.length && !activeId) {
      setActiveId(data[0].id);
    }
  };

  const fetchMessages = async (conversationId) => {
    setLoading(true);
    try {
      const data = await getMessages(conversationId);
      setMessages(data || []);
    } finally {
      setLoading(false);
    }
  };

  const selectConversation = (id) => {
    setActiveId(id);
    fetchMessages(id);
  };

  const send = async (text) => {
    if (!activeId) return;
    await sendMessage(activeId, text);
    await fetchMessages(activeId);
  };

  useEffect(() => {
    fetchConversations();
  }, []);

  useEffect(() => {
    if (activeId) {
      fetchMessages(activeId);
    }
  }, [activeId]);

  return {
    conversations,
    messages,
    activeId,
    selectConversation,
    send,
    loading,
  };
}
