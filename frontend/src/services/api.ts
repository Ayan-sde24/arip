// Base API client for ARIP backend

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(error || `Request failed: ${res.status}`);
  }

  return res.json() as Promise<T>;
}

export async function uploadResume(file: File): Promise<{ document_id: string }> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}/api/resume/upload`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
  return res.json();
}

export async function uploadJob(file: File): Promise<{ document_id: string }> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}/api/job/upload`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
  return res.json();
}

export async function runAnalysis(payload: {
  resume_id: string;
  job_id: string;
}): Promise<{ analysis_id: string }> {
  return request("/api/analyze", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getAnalysis(id: string): Promise<AnalysisResponse> {
  return request(`/api/analysis/${id}`);
}

export async function getReport(id: string): Promise<ReportResponse> {
  return request(`/api/report/${id}`);
}

// ── Response Types ────────────────────────────────────────────────────────────

export interface ScoreBreakdown {
  ats_score: number;
  recruiter_score: number;
  semantic_score: number;
  overall_score: number;
}

export interface AgentResult {
  agent: string;
  status: "pending" | "running" | "completed" | "failed";
  score?: number;
  summary?: string;
}

export interface Recommendation {
  priority: "high" | "medium" | "low";
  category: string;
  title: string;
  detail: string;
}

export interface AnalysisResponse {
  analysis_id: string;
  status: "pending" | "running" | "completed" | "failed";
  scores: ScoreBreakdown;
  agents: AgentResult[];
  candidate_name?: string;
  job_title?: string;
}

export interface ReportResponse {
  analysis_id: string;
  scores: ScoreBreakdown;
  recommendations: Recommendation[];
  optimized_resume?: string;
  ats_keywords_matched: string[];
  ats_keywords_missing: string[];
  radar_data: { subject: string; score: number }[];
}
