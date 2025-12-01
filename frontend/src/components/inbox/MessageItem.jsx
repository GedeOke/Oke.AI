export default function MessageItem({ message }) {
  const isUser = message.sender_type === "customer";
  return (
    <div className={`flex ${isUser ? "justify-start" : "justify-end"}`}>
      <div
        className={`max-w-xl rounded-lg px-3 py-2 text-sm shadow ${
          isUser ? "bg-white border border-gray-200" : "bg-indigo-600 text-white"
        }`}
      >
        <div className="font-medium text-xs mb-1 text-gray-500">
          {isUser ? "Customer" : "AI"}
        </div>
        <div>{message.content}</div>
      </div>
    </div>
  );
}
