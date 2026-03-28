import { useState } from "react";
import { createBot, uploadAvatar } from "../services/api";

export default function CreateCharacter({ goBack, refreshBots }) {
  const token = localStorage.getItem("token");

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [systemPrompt, setSystemPrompt] = useState("");
  const [initialMessage, setInitialMessage] = useState("");
  const [avatar, setAvatar] = useState(null);

  const handleSubmit = async () => {
    if (!name || !systemPrompt) {
      alert("Name and system prompt are required");
      return;
    }

    // 1️⃣ Create bot
    const bot = await createBot(
      {
        name,
        description,
        system_prompt: systemPrompt,
        initial_message: initialMessage,
        is_public: true,
      },
      token
    );

    // 2️⃣ Upload avatar
    if (avatar) {
      await uploadAvatar(bot.id, avatar, token);
    }

    alert("Character created!");

    refreshBots(); // refresh list
    goBack();
  };

  return (
    <div className="min-h-screen bg-[#0b0f14] text-white p-6 max-w-3xl mx-auto">

      <button onClick={goBack} className="mb-4">⬅ Back</button>

      <h1 className="text-3xl font-bold mb-6">Create Character</h1>

      <div className="space-y-4">

        <input
          placeholder="Name"
          className="w-full p-3 bg-[#1a2330] rounded"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <input
          placeholder="Description"
          className="w-full p-3 bg-[#1a2330] rounded"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <textarea
          placeholder="System Prompt (Personality)"
          className="w-full p-3 bg-[#1a2330] rounded h-32"
          value={systemPrompt}
          onChange={(e) => setSystemPrompt(e.target.value)}
        />

        <textarea
          placeholder="Initial Message"
          className="w-full p-3 bg-[#1a2330] rounded h-24"
          value={initialMessage}
          onChange={(e) => setInitialMessage(e.target.value)}
        />

        <input
          type="file"
          onChange={(e) => setAvatar(e.target.files[0])}
        />

        <button
          onClick={handleSubmit}
          className="bg-orange-500 px-6 py-3 rounded-xl w-full"
        >
          Create
        </button>
      </div>
    </div>
  );
}