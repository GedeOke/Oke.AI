import { useEffect, useState } from "react";
import Card from "../../components/ui/Card.jsx";
import DocumentUploader from "../../components/ai/rag/DocumentUploader.jsx";
import DocumentList from "../../components/ai/rag/DocumentList.jsx";
import ChunkPreviewModal from "../../components/ai/rag/ChunkPreviewModal.jsx";
import RagTestConsole from "../../components/ai/rag/RagTestConsole.jsx";
import { uploadDocument, listDocuments, listChunks, testRag } from "../../lib/ragApi";

export default function KnowledgeBase() {
  const [docs, setDocs] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [chunks, setChunks] = useState([]);
  const [openPreview, setOpenPreview] = useState(false);
  const [ragResult, setRagResult] = useState(null);

  const refresh = async () => {
    const data = await listDocuments();
    setDocs(data || []);
  };

  const handlePreview = async (doc) => {
    setSelectedDoc(doc);
    const data = await listChunks(doc.id);
    setChunks(data || []);
    setOpenPreview(true);
  };

  const handleTest = async (query) => {
    const data = await testRag({ query });
    setRagResult(data || {});
  };

  useEffect(() => {
    refresh();
  }, []);

  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs font-semibold text-indigo-600 uppercase tracking-[0.3em]">Knowledge Base</p>
        <h1 className="text-2xl font-semibold text-slate-900">RAG Manager</h1>
        <p className="text-sm text-slate-500">Kelola dokumen, preview chunks, dan uji query RAG.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card>
          <DocumentUploader onUpload={async (fd) => { await uploadDocument(fd); refresh(); }} />
        </Card>
        <Card>
          <RagTestConsole onTest={handleTest} result={ragResult} />
        </Card>
      </div>

      <Card>
        <DocumentList documents={docs} onSelect={handlePreview} />
      </Card>

      <ChunkPreviewModal open={openPreview} onClose={() => setOpenPreview(false)} chunks={chunks} />
    </div>
  );
}
