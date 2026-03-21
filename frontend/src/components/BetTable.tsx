type Bet = {
    Player: string;
    Stat: string;
    Line: number;
    Probability: string;
    Edge: string;
    EV: number;
    "Kelly Bet": string;
  };
  
  export default function BetTable({
    bets,
  }: {
    bets: Bet[];
  }) {
    return (
      <div style={{ marginBottom: "40px" }}>
  
        <table style={styles.table}>
          <thead>
            <tr>
              <th>Player</th>
              <th>Stat</th>
              <th>Line</th>
              <th>Prob</th>
              <th>Edge</th>
              <th>EV</th>
              <th>Kelly</th>
            </tr>
          </thead>
  
          <tbody>
            {bets.map((bet, i) => (
              <tr key={i}>
                <td>{bet.Player}</td>
                <td>{bet.Stat}</td>
                <td>{bet.Line}</td>
                <td>{bet.Probability}</td>
                <td>{bet.Edge}</td>
                <td style={{ color: bet.EV > 0 ? "#16a34a" : "#dc2626" }}>
                  {bet.EV}
                </td>
                <td>{bet["Kelly Bet"]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
  
  const styles = {
    table: {
      width: "100%",
      borderCollapse: "collapse" as const,
      backgroundColor: "#111",
      color: "#fff",
    },
  };