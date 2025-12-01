import http from "./axios";

export const fetchLogs = async (params = {}) => {
  try {
    const { data } = await http.get("/ai/logs", { params });
    return data;
  } catch {
    return [];
  }
};

export const fetchLogDetail = async (id) => {
  try {
    const { data } = await http.get(`/ai/logs/${id}`);
    return data;
  } catch {
    return null;
  }
};

export const fetchMetrics = async () => {
  try {
    const { data } = await http.get("/ai/metrics");
    return data;
  } catch {
    return {};
  }
};
