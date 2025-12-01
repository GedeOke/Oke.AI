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

export const listChunks = async (docId) => {
  const { data } = await http.get(`/rag/chunks/${docId}`);
  return data;
};

export const testRag = async (payload) => {
  const { data } = await http.post("/rag/test", payload);
  return data;
};
