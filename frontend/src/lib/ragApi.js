import http from "./axios";

export const uploadDocument = async (formData) => {
  const { data } = await http.post("/rag/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
};

export const uploadText = async (payload) => {
  const { data } = await http.post("/rag/text", payload);
  return data;
};

export const listDocuments = async () => {
  const { data } = await http.get("/rag/documents");
  return data;
};

export const searchRag = async (query, top_k = 6) => {
  const { data } = await http.get("/rag/search", { params: { query, top_k } });
  return data;
};
