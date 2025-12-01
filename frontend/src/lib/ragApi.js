import http from "./axios";

export const uploadDocument = async (formData, embed_provider) => {
  if (embed_provider) formData.append("embed_provider", embed_provider);
  const { data } = await http.post("/rag/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
};

export const uploadText = async (payload, embed_provider) => {
  const { data } = await http.post("/rag/text", { ...payload, embed_provider });
  return data;
};

export const listDocuments = async () => {
  const { data } = await http.get("/rag/documents");
  return data;
};

export const searchRag = async (query, top_k = 6, embed_provider) => {
  const { data } = await http.get("/rag/search", { params: { query, top_k, embed_provider } });
  return data;
};
