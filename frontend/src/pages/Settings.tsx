import { useState } from "react";
import { useThemeStore } from "../store";
import { PageContainer } from "../components/layout/Containers";
import { GlassCard } from "../components/cards/Cards";
import { Button } from "../components/ui/Button";
import { Divider } from "../components/ui/Utilities";
import { Sliders, Bell, Monitor, Moon, Sun } from "lucide-react";
import { cn } from "../lib/utils";

export function Settings() {
  const { theme, setTheme } = useThemeStore();
  const [atsWeight, setAtsWeight] = useState(70);
  const [recWeight, setRecWeight] = useState(80);
  const [notifEmail, setNotifEmail] = useState(true);
  const [notifDesktop, setNotifDesktop] = useState(false);

  return (
    <PageContainer>
      <div className="flex flex-col gap-8 w-full">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-black tracking-tight text-foreground">Workspace Settings</h1>
          <p className="text-sm text-muted-foreground mt-1">
            Configure agent audit parameters, theme appearance, and notification thresholds.
          </p>
        </div>

        <Divider label="Appearance & Theme" />

        {/* Theme Settings cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full">
          {[
            { id: "dark",   label: "Dark Mode",   icon: Moon },
            { id: "light",  label: "Light Mode",  icon: Sun },
            { id: "system", label: "System Auto", icon: Monitor },
          ].map((opt) => (
            <GlassCard
              key={opt.id}
              onClick={() => setTheme(opt.id as any)}
              className={cn(
                "p-5 flex flex-col items-center gap-3 text-center cursor-pointer transition-all border",
                theme === opt.id
                  ? "border-primary/50 bg-primary/5"
                  : "border-border/40 hover:border-primary/20"
              )}
            >
              <opt.icon className="h-5 w-5 text-primary" />
              <span className="text-xs font-bold text-foreground">{opt.label}</span>
            </GlassCard>
          ))}
        </div>

        <Divider label="Multi-Agent Weight Tuning" />

        {/* AI Preferences weight sliders */}
        <GlassCard className="p-6 flex flex-col gap-6 border-border/40 w-full">
          <div className="flex items-center gap-3">
            <Sliders className="h-5 w-5 text-primary shrink-0" />
            <div>
              <h4 className="text-sm font-bold text-foreground">Sensitivity Weighting</h4>
              <p className="text-xs text-muted-foreground mt-0.5">
                Adjust how aggressively each AI agent flags deviations or compliance issues.
              </p>
            </div>
          </div>

          <div className="flex flex-col gap-4">
            {/* ATS weight slider */}
            <div className="flex flex-col gap-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-foreground/80">ATS Compliance Agent</span>
                <span className="font-bold text-primary">{atsWeight}%</span>
              </div>
              <input
                type="range"
                min="10"
                max="100"
                value={atsWeight}
                onChange={(e) => setAtsWeight(Number(e.target.value))}
                className="w-full h-1 bg-accent rounded-lg appearance-none cursor-pointer accent-primary"
              />
              <span className="text-[10px] text-muted-foreground">Adjusts structural parse strictness levels.</span>
            </div>

            {/* Recruiter weight slider */}
            <div className="flex flex-col gap-2">
              <div className="flex justify-between items-center text-xs">
                <span className="font-semibold text-foreground/80">Recruiter AI Scorer</span>
                <span className="font-bold text-indigo-400">{recWeight}%</span>
              </div>
              <input
                type="range"
                min="10"
                max="100"
                value={recWeight}
                onChange={(e) => setRecWeight(Number(e.target.value))}
                className="w-full h-1 bg-accent rounded-lg appearance-none cursor-pointer accent-primary"
              />
              <span className="text-[10px] text-muted-foreground">Influences career metrics analysis triggers.</span>
            </div>
          </div>
        </GlassCard>

        <Divider label="Notification Thresholds" />

        {/* Notifications toggles */}
        <GlassCard className="p-6 flex flex-col gap-6 border-border/40 w-full">
          <div className="flex items-center gap-3">
            <Bell className="h-5 w-5 text-primary shrink-0" />
            <div>
              <h4 className="text-sm font-bold text-foreground">Alert Subscriptions</h4>
              <p className="text-xs text-muted-foreground mt-0.5">
                Select target routes for system notifications.
              </p>
            </div>
          </div>

          <div className="flex flex-col gap-3">
            <label className="flex items-center justify-between cursor-pointer">
              <span className="text-xs font-semibold text-foreground/80">Email updates on analysis complete</span>
              <input
                type="checkbox"
                checked={notifEmail}
                onChange={(e) => setNotifEmail(e.target.checked)}
                className="h-4 w-4 rounded border-border/60 text-primary focus:ring-primary accent-primary"
              />
            </label>
            <label className="flex items-center justify-between cursor-pointer">
              <span className="text-xs font-semibold text-foreground/80">Desktop push alerts</span>
              <input
                type="checkbox"
                checked={notifDesktop}
                onChange={(e) => setNotifDesktop(e.target.checked)}
                className="h-4 w-4 rounded border-border/60 text-primary focus:ring-primary accent-primary"
              />
            </label>
          </div>
        </GlassCard>

        {/* Confirm buttons */}
        <div className="flex justify-end gap-3 w-full">
          <Button variant="outline" size="sm">
            Cancel
          </Button>
          <Button variant="gradient" size="sm" onClick={() => alert("Settings saved successfully!")}>
            Save Changes
          </Button>
        </div>
      </div>
    </PageContainer>
  );
}
