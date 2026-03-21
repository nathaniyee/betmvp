const API_URL = import.meta.env.VITE_API_URL;

export async function fetchBets() {
    const res = await fetch(`${API_URL}/bets`);
  
    if (!res.ok) {
      throw new Error("Failed to fetch bets");
    }
  
    return res.json();
}

export async function refreshBets() {
    await fetch(`${API_URL}/refresh`, {
      method: "POST",
    });
  }