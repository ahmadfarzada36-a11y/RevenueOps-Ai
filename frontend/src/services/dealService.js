import api from "../api/axios";

// گرفتن لیست معاملات
export const getDeals = async () => {
  const res = await api.get("/deals");
  return res.data;
};

// آپدیت وضعیت معامله
export const updateDealStatus = async (dealId, status) => {
  const res = await api.put(`/deals/${dealId}`, {
    status: status,
  });
  return res.data;
};

// ساخت Follow-up
export const createFollowUp = async (dealId, note) => {
  const res = await api.post(`/deals/${dealId}/follow-up`, {
    note: note,
  });
  return res.data;
};
