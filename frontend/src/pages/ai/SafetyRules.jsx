import { useEffect, useState } from "react";
import Card from "../../components/ui/Card.jsx";
import ForbiddenTopicsEditor from "../../components/ai/safety/ForbiddenTopicsEditor.jsx";
import AllowedTopicsEditor from "../../components/ai/safety/AllowedTopicsEditor.jsx";
import SafetyTester from "../../components/ai/safety/SafetyTester.jsx";
import Button from "../../components/ui/Button.jsx";
import { fetchSafety, updateSafety, testSafety } from "../../lib/safetyApi";

export default function SafetyRules() {
  const [config, setConfig] = useState({ forbidden: [], allowed: [] });
  const [testResult, setTestResult] = useState(null);

  useEffect(() => {
    const load = async () => {
      const data = await fetchSafety();
      setConfig({ forbidden: data?.forbidden || [], allowed: data?.allowed || [] });
    };
    load();
  }, []);

  const handleSave = async () => {
    await updateSafety(config);
  };

  const handleTest = async (text) => {
    const res = await testSafety({ text });
    setTestResult(res);
  };

  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs font-semibold text-indigo-600 uppercase tracking-[0.3em]">Safety & Rules</p>
        <h1 className="text-2xl font-semibold text-slate-900">Safety & Rules Engine</h1>
        <p className="text-sm text-slate-500">Atur topik terlarang/diperbolehkan dan test output AI.</p>
      </div>
      <Card className="space-y-4">
        <ForbiddenTopicsEditor topics={config.forbidden} onChange={(forbidden) => setConfig({ ...config, forbidden })} />
        <AllowedTopicsEditor topics={config.allowed} onChange={(allowed) => setConfig({ ...config, allowed })} />
        <Button onClick={handleSave}>Save Safety Rules</Button>
      </Card>
      <Card>
        <h3 className="text-sm font-semibold text-slate-800 mb-2">Safety Test</h3>
        <SafetyTester onTest={handleTest} result={testResult} />
      </Card>
    </div>
  );
}
