import { api } from "../api/client";

export const resumeService = {
  async uploadResume(
    file: File,
    onProgress?: (progress: number) => void,
    signal?: AbortSignal
  ) {
    const formData = new FormData();
    formData.append("file", file);

    const res = await api.post("/api/resume/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      signal,
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(percent);
        }
      },
    });

    return res.data; // expects: { document_id }
  },
};
export default resumeService;
