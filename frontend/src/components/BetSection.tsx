import BetTable from "./BetTable";

export default function BetSection({
  title,
  bets,
}: {
  title: string;
  bets: any[];
}) {
  return (
    <div style={{ marginBottom: "32px" }}>
      <h2 style={{ marginBottom: "10px" }}>{title}</h2>

      <BetTable bets={bets} />
    </div>
  );
}