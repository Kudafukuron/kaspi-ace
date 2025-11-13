import React, { useState, useEffect } from "react";
import { getChatHistory, sendMessage } from "../api/chat";

function ChatWindow({ token, consumer }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    if (consumer) loadHistory();
  }, [consumer]);

  const loadHistory = async () => {
    const res = await getChatHistory(token, consumer.id);
    setMessages(res.data);
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    await sendMessage(token, consumer.id, input);
    setInput("");
    await loadHistory();
  };

  return (
    <div className="chat-window">
      <h3>Chat with {consumer.username}</h3>

      <div className="messages">
        {messages.map((m) => (
          <div
            key={m.id}
            className={m.sender === consumer.id ? "msg consumer" : "msg me"}
          >
            {m.content}
          </div>
        ))}
      </div>

      <div className="input-row">
        <input value={input} onChange={(e) => setInput(e.target.value)} />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default ChatWindow;
