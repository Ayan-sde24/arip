import { Link } from "react-router-dom";
import { AlertCircle, ArrowLeft } from "lucide-react";
import { PageContainer } from "../components/layout/Containers";

export function NotFound() {
  return (
    <PageContainer className="flex-1 flex flex-col items-center justify-center min-h-[70vh] text-center gap-6">
      <div className="h-16 w-16 rounded-2xl bg-destructive/10 border border-destructive/20 flex items-center justify-center text-destructive">
        <AlertCircle className="h-8 w-8" />
      </div>
      <div>
        <h1 className="text-3xl font-black tracking-tight text-foreground">404 - Page Not Found</h1>
        <p className="text-sm text-muted-foreground mt-2 max-w-sm mx-auto leading-relaxed">
          The dashboard route you requested does not exist or has been removed.
        </p>
      </div>
      <Link
        to="/"
        className="inline-flex items-center justify-center gap-2 h-9 px-4 rounded-lg text-xs font-semibold bg-gradient-to-r from-primary via-indigo-500 to-purple-600 text-white hover:brightness-105 shadow-md transition-all active:scale-[0.98] select-none"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Home
      </Link>
    </PageContainer>
  );
}
