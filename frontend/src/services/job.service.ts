import { api } from "../api/client";

export const jobService = {
  async uploadJob(
    file: File,
    onProgress?: (progress: number) => void,
    signal?: AbortSignal
  ) {
    const formData = new FormData();
    formData.append("file", file);

    const res = await api.post("/api/job/upload", formData, {
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
export default jobService;
