import { useEffect, useState } from "react";
import { fetchBets } from "./api";
import BetSection from "./components/BetSection";
import RefreshButton from "./components/RefreshButton";

function App() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBets()
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading bets...</div>;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>
        BetMVP | Helping NBA Fans Make Wiser and Safer Bets
      </h1>

      <RefreshButton setData={setData} setLoading={setLoading} />

      <BetSection title="🔥 Top Overs" bets={data.overs} />
      <BetSection title="🧊 Top Unders" bets={data.unders} />
      <BetSection title="👺 Goblins" bets={data.goblins} />
      <BetSection title="😈 Demons" bets={data.demons} />
    </div>
  );
}

export default App;

const styles = {
  container: {
    maxWidth: "800px",
    margin: "0 auto",
    padding: "20px",
    fontFamily: "system-ui",
  },
  title: {
    fontSize: "28px",
    fontWeight: 700,
    marginBottom: "20px",
  },
};
