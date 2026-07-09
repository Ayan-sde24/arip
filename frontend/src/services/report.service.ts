import { api } from "../api/client";

export const reportService = {
  async getReport(id: string) {
    const res = await api.get(`/api/report/${id}`);
    return res.data; // expects overall score, keyword coverage, recommendations, etc.
  },

  async downloadPDF(id: string) {
    const res = await api.get(`/api/report/${id}/download`, {
      responseType: "blob",
    });
    return res.data; // Returns Blob directly
  },

  async saveSettings(settings: any) {
    const res = await api.post("/api/settings", settings);
    return res.data;
  },
};
export default reportService;
