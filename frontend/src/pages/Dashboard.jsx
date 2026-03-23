import { useEffect, useState } from "react";
import Layout from "../layout/DashboardLayout";
import StatCard from "../components/StatCard";
import Chart from "../components/Chart";
import { getDashboardStats, getAIInsight } from "../services/dashboardService";

export default function Dashboard() {
  const [stats, setStats] = useState({});
  const [ai, setAI] = useState("");

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    const s = await getDashboardStats();
    const a = await getAIInsight();
    setStats(s.data);
    setAI(a.data.message);
  };

  return (
    <Layout>

      <div className="grid grid-cols-3 gap-4">
        <StatCard title="Leads" value={stats.total_leads} />
        <StatCard title="Won" value={stats.deals_won} />
        <StatCard title="Revenue" value={stats.revenue_forecast} />
      </div>

      <Chart />

      <div className="bg-white p-4 mt-4 rounded">
        🤖 {ai}
      </div>

    </Layout>
  );
}
