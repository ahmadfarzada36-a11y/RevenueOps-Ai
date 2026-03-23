import api from "../api/axios";

export const login = async (data) => {
  const res = await api.post("/auth/login", data);
  return res.data;
};

export const register = async (data) => {
  const res = await api.post(
    `/auth/register-company?company_name=${data.company}&email=${data.email}&password=${data.password}`
  );
  return res.data;
};
