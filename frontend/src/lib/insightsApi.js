import http from "./axios";

export const fetchLogs = async (params = {}) => {
  const { data } = await http.get("/ai/logs", { params });
  return data;
};

export const fetchLogDetail = async (id) => {
  const { data } = await http.get(`/ai/logs/${id}`);
  return data;
};

export const fetchMetrics = async () => {
  const { data } = await http.get("/ai/metrics");
  return data;
};
