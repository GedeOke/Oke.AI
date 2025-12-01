import http from "./axios";

export const fetchSafety = async () => {
  const { data } = await http.get("/ai/safety");
  return data;
};

export const updateSafety = async (payload) => {
  const { data } = await http.post("/ai/safety/update", payload);
  return data;
};

export const testSafety = async (payload) => {
  const { data } = await http.post("/ai/safety/test", payload);
  return data;
};
