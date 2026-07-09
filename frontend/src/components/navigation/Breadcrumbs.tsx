import { Link, useLocation } from "react-router-dom";
import { ChevronRight, Home } from "lucide-react";
import { cn } from "../../lib/utils";

const ROUTE_LABELS: Record<string, string> = {
  dashboard: "Dashboard",
  upload:    "Upload",
  analysis:  "Analysis",
  report:    "Report",
  history:   "History",
  reports:   "Reports",
  coach:     "AI Coach",
  settings:  "Settings",
  profile:   "Profile",
  demo:      "Demo",
};

export interface BreadcrumbItem {
  label: string;
  href?: string;
}

export function Breadcrumbs({ items }: { items?: BreadcrumbItem[] }) {
  const { pathname } = useLocation();

  const crumbs: BreadcrumbItem[] = items ?? buildCrumbs(pathname);

  if (crumbs.length <= 1) return null;

  return (
    <nav className="flex items-center gap-1 text-xs text-muted-foreground select-none">
      <Link
        to="/"
        className="flex items-center hover:text-foreground transition-colors"
      >
        <Home className="h-3 w-3" />
      </Link>
      {crumbs.map((crumb, i) => (
        <span key={i} className="flex items-center gap-1">
          <ChevronRight className="h-3 w-3 opacity-40" />
          {crumb.href && i < crumbs.length - 1 ? (
            <Link
              to={crumb.href}
              className="hover:text-foreground transition-colors"
            >
              {crumb.label}
            </Link>
          ) : (
            <span className={cn(i === crumbs.length - 1 && "text-foreground font-medium")}>
              {crumb.label}
            </span>
          )}
        </span>
      ))}
    </nav>
  );
}

function buildCrumbs(pathname: string): BreadcrumbItem[] {
  const segments = pathname.split("/").filter(Boolean);
  if (segments.length === 0) return [{ label: "Home" }];

  return segments.map((seg, i) => {
    const href = "/" + segments.slice(0, i + 1).join("/");
    const label = ROUTE_LABELS[seg] ?? seg.charAt(0).toUpperCase() + seg.slice(1);
    return { label, href: i < segments.length - 1 ? href : undefined };
  });
}
