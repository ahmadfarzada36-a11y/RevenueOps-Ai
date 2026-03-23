import api from "../api/axios";

export const getDashboardStats = () => api.get("/dashboard/stats");
export const getAIInsight = () => api.get("/ai/insight");
