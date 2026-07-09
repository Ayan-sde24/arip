import { api } from "../api/client";

export const analysisService = {
  async runAnalysis(payload: { resume_id: string; job_id: string }) {
    const res = await api.post("/api/analyze", payload);
    return res.data; // expects: { analysis_id }
  },

  async getAnalysis(id: string) {
    const res = await api.get(`/api/analysis/${id}`);
    return res.data; // expects: { status, logs, progress, agent_states }
  },

  async getHistory() {
    const res = await api.get("/api/history");
    return res.data; // expects list of analyses
  },

  async deleteAnalysis(id: string) {
    const res = await api.delete(`/api/analysis/${id}`);
    return res.data;
  },
};
export default analysisService;
