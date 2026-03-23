export default function DealCard({ deal }) {
  return (
    <div className="deal-card">
      <b>{deal.name}</b>
      <p>${deal.value}</p>
    </div>
  );
}