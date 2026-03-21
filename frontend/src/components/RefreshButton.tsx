import { fetchBets, refreshBets } from "../api";

type Props = {
  setData: (data: any) => void;
  setLoading: (loading: boolean) => void;
};

export default function RefreshButton({ setData, setLoading }: Props) {
  return (
    <div style={styles.container}>
      <button
        onClick={async () => {
          setLoading(true);

          await refreshBets(); // hit backend refresh
          const data = await fetchBets(); // get updated bets

          setData(data);
          setLoading(false);
        }}
        style={styles.button}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = "scale(1.05)";
          e.currentTarget.style.backgroundColor = "#374151";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = "scale(1)";
          e.currentTarget.style.backgroundColor = "#1f2937";
        }}
      >
        Refresh
      </button>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    justifyContent: "flex-end",
    marginBottom: "10px",
  },
  button: {
    padding: "6px 10px",
    backgroundColor: "#1f2937",
    color: "#e5e7eb",
    border: "1px solid #374151",
    borderRadius: "6px",
    cursor: "pointer",
    fontSize: "12px",
    transition: "transform 0.15s ease, background-color 0.15s ease",
  },
};