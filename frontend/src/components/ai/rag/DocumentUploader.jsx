import { useState } from "react";
import Button from "../../ui/Button.jsx";

export default function DocumentUploader({ onUpload }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    await onUpload(formData);
    setLoading(false);
    setFile(null);
  };

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-slate-700">Upload Document (pdf/docx/txt)</label>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="w-full text-sm"
        accept=".pdf,.docx,.txt"
      />
      <Button onClick={handleUpload} disabled={loading || !file}>
        {loading ? "Uploading..." : "Upload"}
      </Button>
    </div>
  );
}
