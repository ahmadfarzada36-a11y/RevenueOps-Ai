export default function StatCard({ title, value }) {
  return (
    <div className="bg-white p-4 rounded shadow">
      <p>{title}</p>
      <h2 className="text-xl font-bold">{value}</h2>
    </div>
  );
}
