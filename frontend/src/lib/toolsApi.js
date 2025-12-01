import http from "./axios";

export const fetchTools = async () => {
  const { data } = await http.get("/ai/tools");
  return data;
};

export const updateTools = async (payload) => {
  const { data } = await http.post("/ai/tools/update", payload);
  return data;
};

export const testTools = async (payload) => {
  const { data } = await http.post("/ai/tools/test", payload);
  return data;
};
