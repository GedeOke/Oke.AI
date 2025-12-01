import http from "./axios";

export const fetchAiSettings = async (organizationId) => {
  const { data } = await http.get(`/ai/settings/${organizationId}`);
  return data;
};

export const updateAiSettings = async (organizationId, payload) => {
  const { data } = await http.post(`/ai/settings/update`, { organization_id: organizationId, ...payload });
  return data;
};
