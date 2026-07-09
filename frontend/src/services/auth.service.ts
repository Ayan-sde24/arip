import { api } from "../api/client";

export const authService = {
  async login(payload: any) {
    const res = await api.post("/api/auth/token", payload);
    return res.data; // expects: { access_token, refresh_token, user }
  },

  async register(payload: any) {
    const res = await api.post("/api/auth/register", payload);
    return res.data;
  },

  async logout() {
    await api.post("/api/auth/logout");
  },

  async getProfile() {
    const res = await api.get("/api/auth/me");
    return res.data;
  },
};
export default authService;
