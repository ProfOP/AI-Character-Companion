import { useEffect, useState } from "react";
import { getBots } from "../services/api";
import Chat from "./Chat";
import CreateCharacter from "./CreateCharacter";
import MyCharacters from "./MyCharacters";

export default function Home() {
  const [bots, setBots] = useState([]);
  const [selectedBot, setSelectedBot] = useState(null);
  const [page, setPage] = useState("home");

  const token = localStorage.getItem("token");

  const fetchBots = async () => {
    const data = await getBots(token);
    setBots(data);
  };

  useEffect(() => {
    fetchBots();
  }, []);

  if (selectedBot) {
    return <Chat bot={selectedBot} goBack={() => setSelectedBot(null)} />;
  }

  if (page === "create") {
    return (
      <CreateCharacter
        goBack={() => setPage("home")}
        refreshBots={fetchBots}
      />
    );
  }

  if (page === "mybots") {
    return (
      <MyCharacters
        bots={bots}
        goBack={() => setPage("home")}
        refreshBots={fetchBots}
      />
    );
  }

  return (
    <div className="flex h-screen bg-[#0b0f14] text-white">

      {/* Sidebar */}
      <div className="w-64 bg-[#0e141b] border-r border-gray-800 p-4 flex flex-col gap-4">
        <h1 className="text-xl font-bold">AI Uncensored</h1>

        <button
          onClick={() => setPage("mybots")}
          className="bg-[#1a2330] p-3 rounded-lg text-left hover:bg-[#243041]"
        >
          ✨ My Characters
        </button>

        <button
          onClick={() => setPage("create")}
          className="bg-orange-500 p-3 rounded-lg hover:bg-orange-600"
        >
          + Create Character
        </button>

        <div className="mt-auto text-sm text-gray-400">
          Account (Coming Soon)
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto px-10 py-8">

        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-5xl font-bold mb-2">AI Uncensored</h1>
          <p className="text-gray-400">Private. Liberated. Nuanced.</p>
        </div>

        {/* Search */}
        <div className="flex justify-center mb-10">
          <input
            placeholder="Search characters..."
            className="w-[500px] bg-[#1a2330] px-5 py-3 rounded-full outline-none"
          />
        </div>

        {/* Bot Grid */}
        <div className="grid grid-cols-3 gap-6 max-w-6xl mx-auto">
          {bots.map((bot) => (
            <div
              key={bot.id}
              onClick={() => setSelectedBot(bot)}
              className="bg-[#111827] rounded-2xl overflow-hidden cursor-pointer
              hover:scale-105 transition transform hover:shadow-xl"
            >
              <img
                src={`http://127.0.0.1:8000${bot.avatar_url}`}
                className="w-full h-52 object-cover"
              />

              <div className="p-4">
                <h2 className="text-lg font-semibold">{bot.name}</h2>
                <p className="text-gray-400 text-sm mt-1 line-clamp-2">
                  {bot.description}
                </p>
              </div>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}