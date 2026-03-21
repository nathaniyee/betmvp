export async function fetchBets() {
    const res = await fetch("http://127.0.0.1:8000/bets");
  
    if (!res.ok) {
      throw new Error("Failed to fetch bets");
    }
  
    return res.json();
}

export async function refreshBets() {
    await fetch("http://127.0.0.1:8000/refresh", {
      method: "POST",
    });
  }