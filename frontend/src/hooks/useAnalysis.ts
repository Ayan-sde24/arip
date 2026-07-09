import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { analysisService } from "../services/analysis.service";

export function useAnalysis(id?: string) {
  const queryClient = useQueryClient();

  // Run analysis mutation
  const runMutation = useMutation({
    mutationFn: (payload: { resume_id: string; job_id: string }) =>
      analysisService.runAnalysis(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["analysis-history"] });
    },
  });

  // Fetch active analysis query (with polling support if status is running/processing)
  const analysisQuery = useQuery({
    queryKey: ["analysis", id],
    queryFn: () => analysisService.getAnalysis(id!),
    enabled: !!id,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (!data) return 2000;
      return data.status === "running" || data.status === "processing" ? 2000 : false;
    },
  });

  // History query
  const historyQuery = useQuery({
    queryKey: ["analysis-history"],
    queryFn: () => analysisService.getHistory(),
  });

  // Delete analysis mutation
  const deleteMutation = useMutation({
    mutationFn: (analysisId: string) => analysisService.deleteAnalysis(analysisId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["analysis-history"] });
    },
  });

  return {
    runAnalysis: runMutation.mutateAsync,
    isStarting: runMutation.isPending,
    analysisError: runMutation.error,

    analysis: analysisQuery.data,
    isLoadingAnalysis: analysisQuery.isLoading,
    isRefetchingAnalysis: analysisQuery.isRefetching,

    history: historyQuery.data,
    isLoadingHistory: historyQuery.isLoading,

    deleteAnalysis: deleteMutation.mutateAsync,
    isDeleting: deleteMutation.isPending,
  };
}
export default useAnalysis;
