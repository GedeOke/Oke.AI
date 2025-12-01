import { useState } from "react";
import Button from "../../ui/Button.jsx";

export default function DocumentUploader({ onUpload, embedProvider, setEmbedProvider }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    await onUpload(formData, embedProvider);
    setLoading(false);
    setFile(null);
  };

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-slate-700">Upload Document (pdf/docx/txt)</label>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div>
          <label className="text-xs text-slate-600">Embedding Provider</label>
          <select
            value={embedProvider}
            onChange={(e) => setEmbedProvider(e.target.value)}
            className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
          >
            <option value="openai">OpenAI</option>
            <option value="gemini">Gemini</option>
            <option value="local">Local</option>
          </select>
        </div>
        <div className="flex items-end">
          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="w-full text-sm"
            accept=".pdf,.docx,.txt"
          />
        </div>
      </div>
      <Button onClick={handleUpload} disabled={loading || !file}>
        {loading ? "Uploading..." : "Upload"}
      </Button>
    </div>
  );
}
