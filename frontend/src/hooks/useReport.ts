import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { reportService } from "../services/report.service";

export function useReport(id?: string) {
  const queryClient = useQueryClient();

  const reportQuery = useQuery({
    queryKey: ["report", id],
    queryFn: () => reportService.getReport(id!),
    enabled: !!id && id !== "demo",
  });

  const downloadPDFMutation = useMutation({
    mutationFn: (reportId: string) => reportService.downloadPDF(reportId),
    onSuccess: (blob, reportId) => {
      // Trigger file download in browser
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `ARIP_Report_${reportId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
    },
  });

  const settingsMutation = useMutation({
    mutationFn: (settings: any) => reportService.saveSettings(settings),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["settings"] });
    },
  });

  return {
    report: reportQuery.data,
    isLoadingReport: reportQuery.isLoading,
    reportError: reportQuery.error,

    downloadPDF: downloadPDFMutation.mutateAsync,
    isDownloading: downloadPDFMutation.isPending,

    saveSettings: settingsMutation.mutateAsync,
    isSavingSettings: settingsMutation.isPending,
  };
}
export default useReport;
