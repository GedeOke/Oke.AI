import { useState } from "react";
import Button from "../ui/Button.jsx";
import Textarea from "../ui/Textarea.jsx";

export default function MessageInput({ onSend, loading }) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  return (
    <div className="flex flex-col gap-2">
      <Textarea
        rows={3}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type a message..."
      />
      <div className="flex justify-end">
        <Button onClick={handleSend} disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </Button>
      </div>
    </div>
  );
}
