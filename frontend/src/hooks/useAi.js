import { useState } from "react";
import { aiRun } from "../lib/api";
import { useOrganization } from "../context/OrganizationContext.jsx";

export function useAi() {
  const { organizationId } = useOrganization();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const run = async ({ message, model_provider, model }) => {
    setLoading(true);
    setError(null);
    try {
      const data = await aiRun({
        organization_id: organizationId,
        message,
        model_provider,
        model,
      });
      setResult(data);
    } catch (err) {
      setError(err.response?.data || err.message);
    } finally {
      setLoading(false);
    }
  };

  return { run, loading, result, error };
}
