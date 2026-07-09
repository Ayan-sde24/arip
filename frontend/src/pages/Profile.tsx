import {
  Activity,
  Award,
  Sparkles,
  FileCheck,
  TrendingUp,
} from "lucide-react";
import { PageContainer } from "../components/layout/Containers";
import { GlassCard } from "../components/cards/Cards";
import { Badge } from "../components/ui/Badge";
import { Divider } from "../components/ui/Utilities";

export function Profile() {
  const profileStats = [
    { label: "Total Audits Run", value: "24", icon: FileCheck },
    { label: "Average Match Index", value: "85%", icon: Award },
    { label: "AI Suggestions Applied", value: "62", icon: Sparkles },
    { label: "Career Progress Rate", value: "+14%", icon: TrendingUp },
  ];

  const profileActivity = [
    { time: "Yesterday, 3:20 PM", text: "Exported Senior DevOps Engineer report as PDF" },
    { time: "2 days ago", text: "Accepted summary optimize suggestion for Senior Full Stack Engineer" },
    { time: "5 days ago", text: "Configured multi-agent weight sliders inside settings panel" },
  ];

  return (
    <PageContainer>
      <div className="flex flex-col gap-8 w-full">
        {/* Header banner */}
        <div className="relative overflow-hidden rounded-2xl border border-border/40 bg-card/25 p-6 flex flex-col md:flex-row gap-6 items-center w-full">
          <div className="absolute inset-0 pointer-events-none -z-10">
            <div className="absolute top-1/2 left-1/4 w-[200px] h-[200px] bg-primary/10 rounded-full blur-[80px]" />
          </div>

          {/* Large Avatar */}
          <div className="h-20 w-20 rounded-full bg-gradient-to-br from-primary via-indigo-500 to-purple-600 flex items-center justify-center text-white text-3xl font-black shadow-lg shadow-primary/20 shrink-0">
            A
          </div>

          <div className="flex-1 text-center md:text-left min-w-0">
            <div className="flex items-center justify-center md:justify-start gap-2 flex-wrap">
              <h2 className="text-xl font-bold text-foreground">ARIP Platform User</h2>
              <Badge variant="premium">Pro Account</Badge>
            </div>
            <p className="text-xs text-muted-foreground mt-1">user@example.com · Member since 2026</p>
          </div>
        </div>

        <Divider label="Audit Statistics" />

        {/* Stats breakdown */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full">
          {profileStats.map((stat, idx) => (
            <GlassCard key={idx} className="p-5 flex flex-col gap-2 border-border/40 relative overflow-hidden">
              <div className="h-8 w-8 rounded-lg bg-accent/20 flex items-center justify-center text-primary shrink-0 border border-border/40">
                <stat.icon className="h-4 w-4" />
              </div>
              <span className="text-[10px] uppercase tracking-wider text-muted-foreground font-bold mt-2">
                {stat.label}
              </span>
              <p className="text-2xl font-black text-foreground">{stat.value}</p>
            </GlassCard>
          ))}
        </div>

        <Divider label="Recent Platform Actions" />

        {/* Activity feed */}
        <div className="flex flex-col gap-3 w-full">
          {profileActivity.map((act, i) => (
            <GlassCard key={i} className="p-4 flex gap-4 items-center border-border/40">
              <Activity className="h-4 w-4 text-primary shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-xs text-foreground/80 font-medium leading-relaxed truncate">{act.text}</p>
                <span className="text-[9px] text-muted-foreground mt-0.5 block">{act.time}</span>
              </div>
            </GlassCard>
          ))}
        </div>
      </div>
    </PageContainer>
  );
}
