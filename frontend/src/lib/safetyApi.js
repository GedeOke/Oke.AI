import http from "./axios";

export const fetchSafety = async () => {
  try {
    const { data } = await http.get("/ai/safety");
    return data;
  } catch (err) {
    return null;
  }
};

export const updateSafety = async (payload) => {
  try {
    const { data } = await http.post("/ai/safety/update", payload);
    return data;
  } catch (err) {
    return null;
  }
};

export const testSafety = async (payload) => {
  try {
    const { data } = await http.post("/ai/safety/test", payload);
    return data;
  } catch (err) {
    return null;
  }
};
