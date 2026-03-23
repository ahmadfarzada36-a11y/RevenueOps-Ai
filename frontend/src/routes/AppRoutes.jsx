import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "../pages/dashboard";
import Deals from "../pages/deals";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/deals" element={<Deals />} />
      </Routes>
    </BrowserRouter>
  );
}
