import { useState } from "react";
import { updateBot, uploadAvatar } from "../services/api";

export default function EditCharacter({ bot, goBack, refreshBots }) {
  const token = localStorage.getItem("token");

  const [name, setName] = useState(bot.name);
  const [description, setDescription] = useState(bot.description);
  const [systemPrompt, setSystemPrompt] = useState(bot.system_prompt);
  const [initialMessage, setInitialMessage] = useState(bot.initial_message);
  const [avatar, setAvatar] = useState(null);

  const handleUpdate = async () => {
    await updateBot(
      bot.id,
      {
        name,
        description,
        system_prompt: systemPrompt,
        initial_message: initialMessage,
      },
      token
    );

    if (avatar) {
      await uploadAvatar(bot.id, avatar, token);
    }

    alert("Character updated!");
    refreshBots();
    goBack();
  };

  return (
    <div className="min-h-screen bg-[#0b0f14] text-white p-6 max-w-3xl mx-auto">

      <button onClick={goBack} className="mb-4">⬅ Back</button>

      <h1 className="text-3xl font-bold mb-6">Edit Character</h1>

      <div className="space-y-4">

        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full p-3 bg-[#1a2330] rounded"
        />

        <input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full p-3 bg-[#1a2330] rounded"
        />

        <textarea
          value={systemPrompt}
          onChange={(e) => setSystemPrompt(e.target.value)}
          className="w-full p-3 bg-[#1a2330] rounded h-32"
        />

        <textarea
          value={initialMessage}
          onChange={(e) => setInitialMessage(e.target.value)}
          className="w-full p-3 bg-[#1a2330] rounded h-24"
        />

        <input
          type="file"
          onChange={(e) => setAvatar(e.target.files[0])}
        />

        <button
          onClick={handleUpdate}
          className="bg-orange-500 px-6 py-3 rounded-xl w-full"
        >
          Save Changes
        </button>
      </div>
    </div>
  );
}