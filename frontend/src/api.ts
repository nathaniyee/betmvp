export async function fetchBets() {
    const res = await fetch("https://betmvp-backend.onrender.com/bets");
  
    if (!res.ok) {
      throw new Error("Failed to fetch bets");
    }
  
    return res.json();
}

export async function refreshBets() {
    await fetch("https://betmvp-backend.onrender.com/refresh", {
      method: "POST",
    });
  }