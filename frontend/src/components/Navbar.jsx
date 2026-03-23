export default function Navbar() {
  return (
    <div className="bg-white shadow px-6 py-3 flex justify-between">
      <h1 className="font-bold">RevenueOps AI</h1>
      <button
        onClick={() =>
          document.documentElement.classList.toggle("dark")
        }
      >
        🌙
      </button>
    </div>
  );
}
