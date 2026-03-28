const BASE_URL = "http://127.0.0.1:8000/api";

// Get all bots
export const getBots = async (token) => {
  const res = await fetch(`${BASE_URL}/bots`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    console.error("Failed to fetch bots");
    return [];
  }

  return res.json();
};

// Send chat message
export const sendMessage = async (data, token) => {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    console.error("Chat request failed");
    return {};
  }

  return res.json();
};
export const regenerateMessage = async (data, token) => {
    const res = await fetch("http://127.0.0.1:8000/api/regenerate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });
  
    if (!res.ok) {
      console.error("Regenerate failed");
      return {};
    }
  
    return res.json();
};
// Create bot
export const createBot = async (data, token) => {
    const res = await fetch("http://127.0.0.1:8000/api/bots", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });
  
    return res.json();
  };
  
  // Upload avatar
  export const uploadAvatar = async (botId, file, token) => {
    const formData = new FormData();
    formData.append("file", file);
  
    const res = await fetch(
      `http://127.0.0.1:8000/api/bots/${botId}/avatar`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      }
    );
  
    return res.json();
  };
  export const deleteBot = async (botId, token) => {
    const res = await fetch(`http://127.0.0.1:8000/api/bots/${botId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  
    return res.json();
  };
  export const updateBot = async (botId, data, token) => {
    const res = await fetch(`http://127.0.0.1:8000/api/bots/${botId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    });
  
    return res.json();
  };