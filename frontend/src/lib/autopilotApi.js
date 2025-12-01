import http from "./axios";

export const fetchAutopilot = async () => {
  try {
    const { data } = await http.get("/ai/autopilot");
    return data;
  } catch (err) {
    return null;
  }
};

export const updateAutopilot = async (payload) => {
  try {
    const { data } = await http.post("/ai/autopilot/update", payload);
    return data;
  } catch (err) {
    return null;
  }
};
