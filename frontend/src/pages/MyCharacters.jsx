import { useState } from "react";
import { deleteBot } from "../services/api";
import EditCharacter from "./EditCharacter";

export default function MyCharacters({ bots, goBack, refreshBots }) {
  const token = localStorage.getItem("token");

  const [editingBot, setEditingBot] = useState(null);

  const handleDelete = async (id) => {
    if (!confirm("Delete this character?")) return;

    await deleteBot(id, token);
    refreshBots();
  };

  // 👉 If editing, show edit page
  if (editingBot) {
    return (
      <EditCharacter
        bot={editingBot}
        goBack={() => setEditingBot(null)}
        refreshBots={refreshBots}
      />
    );
  }

  // 👉 Filter ONLY user bots (private ones)
  const myBots = bots.filter((bot) => !bot.is_public);

  return (
    <div className="min-h-screen bg-[#0b0f14] text-white px-6 py-8">

      <button onClick={goBack} className="mb-6">⬅ Back</button>

      <h1 className="text-3xl font-bold mb-6">My Characters</h1>

      {myBots.length === 0 ? (
        <p className="text-gray-400">No characters created yet.</p>
      ) : (
        <div className="grid grid-cols-3 gap-6">
          {myBots.map((bot) => (
            <div
              key={bot.id}
              className="bg-[#111827] rounded-xl overflow-hidden"
            >
              <img
                src={`http://127.0.0.1:8000${bot.avatar_url}`}
                className="w-full h-48 object-cover"
              />

              <div className="p-4">
                <h2 className="text-lg font-semibold">{bot.name}</h2>

                <p className="text-gray-400 text-sm mt-1 line-clamp-2">
                  {bot.description}
                </p>

                {/* 🔥 ACTION BUTTONS */}
                <div className="flex gap-2 mt-3">
                  <button
                    onClick={() => setEditingBot(bot)}
                    className="flex-1 bg-blue-500 hover:bg-blue-600 py-2 rounded-lg"
                  >
                    Edit
                  </button>

                  <button
                    onClick={() => handleDelete(bot.id)}
                    className="flex-1 bg-red-500 hover:bg-red-600 py-2 rounded-lg"
                  >
                    Delete
                  </button>
                </div>

              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}