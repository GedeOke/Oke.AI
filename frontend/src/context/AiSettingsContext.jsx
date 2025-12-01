import { createContext, useContext, useEffect, useState } from "react";
import { useOrganization } from "./OrganizationContext.jsx";
import { fetchAiSettings, updateAiSettings } from "../lib/aiApi";
import { getErrorMessage } from "../lib/error";

const AiSettingsContext = createContext({
  settings: null,
  loading: false,
  error: null,
  save: async () => {},
  refresh: async () => {},
});

export const AiSettingsProvider = ({ children }) => {
  const { organizationId } = useOrganization();
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const refresh = async () => {
    if (!organizationId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await fetchAiSettings(organizationId);
      setSettings(data || {});
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  const save = async (payload) => {
    if (!organizationId) return;
    setLoading(true);
    setError(null);
    try {
      await updateAiSettings(organizationId, payload);
      setSettings(payload);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refresh();
  }, [organizationId]);

  return (
    <AiSettingsContext.Provider value={{ settings, loading, error, save, refresh, setSettings }}>
      {children}
    </AiSettingsContext.Provider>
  );
};

export const useAiSettings = () => useContext(AiSettingsContext);
