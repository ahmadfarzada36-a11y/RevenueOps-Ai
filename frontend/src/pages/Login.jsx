import { useState } from "react";
import { login, register } from "../api";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [isLogin, setIsLogin] = useState(true);
  const [form, setForm] = useState({});
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    let res;
    if (isLogin) {
      res = await login(form);
    } else {
      res = await register(form);
    }

    console.log(res);

    navigate("/dashboard"); // 👈 بعد از ورود
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-950 text-white">
      <form onSubmit={handleSubmit} className="bg-gray-900 p-8 rounded-xl w-96 space-y-4">

        <h2 className="text-2xl font-bold text-center">
          RevenueOps AI
        </h2>

        {!isLogin && (
          <input
            placeholder="Company"
            className="w-full p-2 bg-gray-800 rounded"
            onChange={(e) => setForm({ ...form, company: e.target.value })}
          />
        )}

        <input
          placeholder="Email"
          className="w-full p-2 bg-gray-800 rounded"
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />

        <input
          placeholder="Password"
          type="password"
          className="w-full p-2 bg-gray-800 rounded"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />

        <button className="w-full bg-blue-600 p-2 rounded">
          {isLogin ? "Login" : "Register"}
        </button>

        <p
          className="text-center cursor-pointer"
          onClick={() => setIsLogin(!isLogin)}
        >
          {isLogin ? "Create account" : "Login"}
        </p>
      </form>
    </div>
  );
}
