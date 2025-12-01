import Card from "../ui/Card";

export default function AIPayloadViewer({ payload }) {
  return (
    <Card>
      <h3 className="text-sm font-semibold mb-2">Request Payload</h3>
      <pre className="text-xs bg-gray-50 p-3 rounded-lg overflow-auto max-h-64 whitespace-pre-wrap">
{JSON.stringify(payload, null, 2)}
      </pre>
    </Card>
  );
}
