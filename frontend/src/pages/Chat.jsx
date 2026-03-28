import { useState, useRef, useEffect } from "react";
import { sendMessage, regenerateMessage } from "../services/api";
import MessageRenderer from "../components/MessageRenderer";
import TypingMessage from "../components/TypingMessage";

export default function Chat({ bot, goBack }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState(null);

  const [tone, setTone] = useState("default");
  const [style, setStyle] = useState("balanced");
  const [intensity, setIntensity] = useState(5);

  const [typingIndex, setTypingIndex] = useState(null);

  const token = localStorage.getItem("token");

  const bottomRef = useRef(null);

  // 🔽 Auto scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // SEND
  const handleSend = async () => {
    if (!input) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);

    const res = await sendMessage(
      {
        bot_id: bot.id,
        message: input,
        conversation_id: conversationId,
        style_config: { tone, style, intensity },
      },
      token
    );

    setConversationId(res.conversation_id);

    const newList = [
      ...newMessages,
      { role: "assistant", content: res.reply },
    ];

    setMessages(newList);
    setTypingIndex(newList.length - 1);
    setInput("");
  };

  // REGENERATE
  const handleRegenerate = async () => {
    if (!conversationId) return;

    const updated = [...messages];

    if (updated[updated.length - 1]?.role === "assistant") {
      updated.pop();
    }

    setMessages(updated);

    const res = await regenerateMessage(
      {
        conversation_id: conversationId,
        style_config: { tone, style, intensity },
      },
      token
    );

    const newList = [
      ...updated,
      { role: "assistant", content: res.reply },
    ];

    setMessages(newList);
    setTypingIndex(newList.length - 1);
  };

  return (
    <div className="h-screen bg-[#0b0f14] text-white flex flex-col">

      {/* Header */}
      <div className="flex items-center gap-3 p-4 border-b border-gray-800 bg-[#0e141b]">
        <button onClick={goBack} className="text-lg">⬅</button>

        <img
          src={`http://127.0.0.1:8000${bot.avatar_url}`}
          className="w-10 h-10 rounded-full object-cover"
        />

        <div>
          <h2 className="text-lg font-semibold">{bot.name}</h2>
          <p className="text-xs text-gray-400">Online</p>
        </div>
      </div>

      {/* Style Controls */}
      <div className="px-6 py-3 border-b border-gray-800 flex gap-4 flex-wrap bg-[#0e141b]">
        <select
          value={tone}
          onChange={(e) => setTone(e.target.value)}
          className="bg-[#1a2330] px-3 py-2 rounded-lg"
        >
          <option value="default">Default</option>
          <option value="playful">Playful</option>
          <option value="romantic">Romantic</option>
          <option value="aggressive">Aggressive</option>
          <option value="serious">Serious</option>
          <option value="dark">Dark</option>
        </select>

        <select
          value={style}
          onChange={(e) => setStyle(e.target.value)}
          className="bg-[#1a2330] px-3 py-2 rounded-lg"
        >
          <option value="short">Short</option>
          <option value="balanced">Balanced</option>
          <option value="descriptive">Descriptive</option>
        </select>

        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-400">Intensity</span>
          <input
            type="range"
            min="1"
            max="10"
            value={intensity}
            onChange={(e) => setIntensity(e.target.value)}
          />
          <span>{intensity}</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto space-y-6">

          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[75%] px-4 py-3 rounded-2xl ${
                  msg.role === "user"
                    ? "bg-orange-500 text-white"
                    : "bg-[#141c26]"
                }`}
              >
                {msg.role === "assistant" && i === typingIndex ? (
                  <TypingMessage
                    text={msg.content}
                    onDone={() => setTypingIndex(null)}
                  />
                ) : (
                  <MessageRenderer text={msg.content} />
                )}
              </div>
            </div>
          ))}

          <div ref={bottomRef} />
        </div>
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-800 bg-[#0e141b] flex gap-3 items-center">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          placeholder="Type a message..."
          className="flex-1 bg-[#1a2330] px-4 py-3 rounded-xl outline-none"
        />

        <button
          onClick={handleRegenerate}
          className="bg-gray-700 hover:bg-gray-600 px-4 py-3 rounded-xl"
        >
          🔁
        </button>

        <button
          onClick={handleSend}
          className="bg-orange-500 hover:bg-orange-600 px-5 py-3 rounded-xl"
        >
          ➤
        </button>
      </div>
    </div>
  );
}