import { create } from "zustand";

interface FileUploadProgress {
  progress: number;
  error: string | null;
  uploaded: boolean;
}

interface UploadStoreState {
  resumeUpload: FileUploadProgress;
  jobUpload: FileUploadProgress;
  updateResumeUpload: (update: Partial<FileUploadProgress>) => void;
  updateJobUpload: (update: Partial<FileUploadProgress>) => void;
  resetUploads: () => void;
}

const initialUploadState = {
  progress: 0,
  error: null,
  uploaded: false,
};

export const useUploadStore = create<UploadStoreState>()((set) => ({
  resumeUpload: { ...initialUploadState },
  jobUpload: { ...initialUploadState },
  updateResumeUpload: (update) =>
    set((state) => ({ resumeUpload: { ...state.resumeUpload, ...update } })),
  updateJobUpload: (update) =>
    set((state) => ({ jobUpload: { ...state.jobUpload, ...update } })),
  resetUploads: () =>
    set({
      resumeUpload: { ...initialUploadState },
      jobUpload: { ...initialUploadState },
    }),
}));
