import { useMutation } from "@tanstack/react-query";
import { jobService } from "../services/job.service";
import { useUploadStore } from "../store/uploadStore";

export function useJob() {
  const updateJobUpload = useUploadStore((s) => s.updateJobUpload);

  const uploadMutation = useMutation({
    mutationFn: async ({ file, signal }: { file: File; signal?: AbortSignal }) => {
      updateJobUpload({ progress: 0, error: null, uploaded: false });
      return jobService.uploadJob(
        file,
        (progress) => {
          updateJobUpload({ progress });
        },
        signal
      );
    },
    onSuccess: () => {
      updateJobUpload({ uploaded: true });
    },
    onError: (err: any) => {
      updateJobUpload({ error: err.message || "Job description upload failed" });
    },
  });

  return {
    uploadJob: uploadMutation.mutateAsync,
    isUploading: uploadMutation.isPending,
    uploadError: uploadMutation.error,
  };
}
export default useJob;
