import http from "./axios";

export const fetchTools = async () => {
  try {
    const { data } = await http.get("/ai/tools");
    return data;
  } catch {
    return [];
  }
};

export const updateTools = async (payload) => {
  try {
    const { data } = await http.post("/ai/tools/update", payload);
    return data;
  } catch {
    return null;
  }
};

export const testTools = async (payload) => {
  try {
    const { data } = await http.post("/ai/tools/test", payload);
    return data;
  } catch {
    return null;
  }
};
