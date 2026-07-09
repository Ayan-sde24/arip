import { create } from "zustand";

interface AnalysisStoreState {
  currentAnalysisId: string | null;
  pipelineLogs: string[];
  activeStepIndex: number;
  setCurrentAnalysisId: (id: string | null) => void;
  appendLog: (log: string) => void;
  clearLogs: () => void;
  setActiveStepIndex: (index: number) => void;
  resetAnalysis: () => void;
}

export const useAnalysisStore = create<AnalysisStoreState>()((set) => ({
  currentAnalysisId: null,
  pipelineLogs: [],
  activeStepIndex: 0,
  setCurrentAnalysisId: (currentAnalysisId) => set({ currentAnalysisId }),
  appendLog: (log) => set((state) => ({ pipelineLogs: [...state.pipelineLogs, log] })),
  clearLogs: () => set({ pipelineLogs: [] }),
  setActiveStepIndex: (activeStepIndex) => set({ activeStepIndex }),
  resetAnalysis: () => set({ currentAnalysisId: null, pipelineLogs: [], activeStepIndex: 0 }),
}));
