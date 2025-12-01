import { useEffect, useState } from "react";
import Card from "../../components/ui/Card.jsx";
import ModelSelector from "../../components/ai/settings/ModelSelector.jsx";
import ParameterSliders from "../../components/ai/settings/ParameterSliders.jsx";
import PersonaEditor from "../../components/ai/settings/PersonaEditor.jsx";
import ToneSelector from "../../components/ai/settings/ToneSelector.jsx";
import SaveBar from "../../components/ai/settings/SaveBar.jsx";
import { useAiSettings } from "../../context/AiSettingsContext.jsx";

export default function Settings() {
  const { settings, setSettings, loading, save } = useAiSettings();
  const [local, setLocal] = useState({
    model_provider: "openai",
    model: "gpt-4o-mini",
    llm_params: { temperature: 0.3, top_p: 1, max_tokens: 512, frequency_penalty: 0, presence_penalty: 0 },
    persona: "",
    tone: "professional",
  });

  useEffect(() => {
    if (settings) {
      setLocal({
        model_provider: settings.model_provider || "openai",
        model: settings.model || "gpt-4o-mini",
        llm_params: settings.llm_params || local.llm_params,
        persona: settings.persona || "",
        tone: settings.tone || "professional",
      });
    }
  }, [settings]);

  const updateParams = (params) => setLocal({ ...local, llm_params: params });

  const handleSave = async () => {
    await save(local);
  };

  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs font-semibold text-indigo-600 uppercase tracking-[0.3em]">AI Config</p>
        <h1 className="text-2xl font-semibold text-slate-900">AI Settings</h1>
        <p className="text-sm text-slate-500">Atur provider, model, parameter generasi, persona, dan tone.</p>
      </div>

      <Card className="space-y-4">
        <ModelSelector
          provider={local.model_provider}
          model={local.model}
          onProviderChange={(p) => setLocal({ ...local, model_provider: p })}
          onModelChange={(m) => setLocal({ ...local, model: m })}
        />
        <ParameterSliders params={local.llm_params} onChange={updateParams} />
        <ToneSelector value={local.tone} onChange={(tone) => setLocal({ ...local, tone })} />
        <PersonaEditor value={local.persona} onChange={(persona) => setLocal({ ...local, persona })} />
      </Card>

      <SaveBar onSave={handleSave} saving={loading} />
    </div>
  );
}
