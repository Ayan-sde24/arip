import { useMutation } from "@tanstack/react-query";
import { resumeService } from "../services/resume.service";
import { useUploadStore } from "../store/uploadStore";

export function useResume() {
  const updateResumeUpload = useUploadStore((s) => s.updateResumeUpload);

  const uploadMutation = useMutation({
    mutationFn: async ({ file, signal }: { file: File; signal?: AbortSignal }) => {
      updateResumeUpload({ progress: 0, error: null, uploaded: false });
      return resumeService.uploadResume(
        file,
        (progress) => {
          updateResumeUpload({ progress });
        },
        signal
      );
    },
    onSuccess: () => {
      updateResumeUpload({ uploaded: true });
    },
    onError: (err: any) => {
      updateResumeUpload({ error: err.message || "Resume upload failed" });
    },
  });

  return {
    uploadResume: uploadMutation.mutateAsync,
    isUploading: uploadMutation.isPending,
    uploadError: uploadMutation.error,
  };
}
export default useResume;
