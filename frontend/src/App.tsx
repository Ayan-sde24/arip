import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AppShell } from "./layouts";
import { LandingPage } from "./pages/LandingPage";
import { LoginPage } from "./pages/LoginPage";
import { Dashboard } from "./pages/Dashboard";
import { UploadPage } from "./pages/UploadPage";
import { AnalysisWorkspace } from "./pages/AnalysisWorkspace";
import { ResultsPage } from "./pages/ResultsPage";
import { ResumeOptimizer } from "./pages/ResumeOptimizer";
import { History } from "./pages/History";
import { Profile } from "./pages/Profile";
import { Settings } from "./pages/Settings";
import { NotFound } from "./pages/NotFound";
import { ProtectedRoute } from "./components/navigation";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, refetchOnWindowFocus: false },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppShell>
          <Routes>
            {/* Public routes */}
            <Route path="/"             element={<LandingPage />} />
            <Route path="/login"        element={<LoginPage />} />

            {/* Protected dashboard / workspaces */}
            <Route element={<ProtectedRoute />}>
              <Route path="/dashboard"    element={<Dashboard />} />
              <Route path="/upload"       element={<UploadPage />} />
              <Route path="/analysis/:id" element={<AnalysisWorkspace />} />
              <Route path="/report/:id"   element={<ResultsPage />} />
              <Route path="/coach"        element={<ResumeOptimizer />} />
              <Route path="/history"      element={<History />} />
              <Route path="/profile"      element={<Profile />} />
              <Route path="/settings"     element={<Settings />} />
            </Route>

            {/* Catch-all */}
            <Route path="*"             element={<NotFound />} />
          </Routes>
        </AppShell>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
