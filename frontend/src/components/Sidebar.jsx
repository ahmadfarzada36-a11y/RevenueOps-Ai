import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="w-60 bg-gray-900 text-white h-screen p-4">
      <h2 className="mb-6 font-bold">Menu</h2>
      <Link to="/" className="block mb-2">Dashboard</Link>
      <Link to="/deals" className="block">Deals</Link>
    </div>
  );
}
