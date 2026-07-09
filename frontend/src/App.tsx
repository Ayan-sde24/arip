import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider } from "./components/theme-provider";
import { AppShell } from "./components/layout/AppShell";
import { LandingPage } from "./pages/LandingPage";
import { UploadPage } from "./pages/UploadPage";
import { AnalysisPage } from "./pages/AnalysisPage";
import { ReportPage } from "./pages/ReportPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, refetchOnWindowFocus: false },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider defaultTheme="dark">
        <BrowserRouter>
          <AppShell>
            <Routes>
              <Route path="/"               element={<LandingPage />} />
              <Route path="/upload"         element={<UploadPage />} />
              <Route path="/analysis/:id"   element={<AnalysisPage />} />
              <Route path="/report/:id"     element={<ReportPage />} />
              <Route path="*"               element={<Navigate to="/" replace />} />
            </Routes>
          </AppShell>
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  );
}
