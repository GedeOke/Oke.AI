import http from "./axios";

export const aiRun = async ({ organization_id, message, model_provider, model }) => {
  const { data } = await http.post("/ai/run", { organization_id, message, model_provider, model });
  return data;
};

export const getConversations = async () => {
  const { data } = await http.get("/conversations");
  return data;
};

export const getMessages = async (conversationId) => {
  const { data } = await http.get(`/messages/conversations/${conversationId}`);
  return data;
};

export const sendMessage = async (conversationId, content) => {
  const { data } = await http.post("/messages/send", {
    conversation_id: conversationId,
    content,
  });
  return data;
};
