import http from "./axios";

export const fetchAutopilot = async () => {
  const { data } = await http.get("/ai/autopilot");
  return data;
};

export const updateAutopilot = async (payload) => {
  const { data } = await http.post("/ai/autopilot/update", payload);
  return data;
};
