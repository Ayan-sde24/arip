import { Navbar } from "./Navbar";
import { Sidebar } from "./Sidebar";
import { ContentArea } from "./Containers";

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <ContentArea className="flex-1 overflow-y-auto min-h-[calc(100vh-73px)]">
          {children}
        </ContentArea>
      </div>
    </div>
  );
}
