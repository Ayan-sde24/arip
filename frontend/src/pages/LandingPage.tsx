import { useState } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  BrainCircuit,
  Sparkles,
  Target,
  ArrowRight,
  ChevronRight,
  Zap,
  Shield,
  Star,
  ChevronDown,
  Terminal,
  Cpu,
  Layers,
  Database,
} from "lucide-react";
import { Badge } from "../components/ui/Badge";
import { GlassCard } from "../components/cards/Cards";
import { staggerContainer, fadeInUp } from "../animations/variants";

const FAQS = [
  {
    question: "How does the multi-agent analysis work?",
    answer: "ARIP coordinates five dedicated AI agents. The Parser extracts section structures, the Semantic Matcher computes conceptual alignment, the ATS Agent checks formatting filters, the Recruiter Agent screens impact indicators, and the Coach compiles actionable optimization rewrites. All agents process your document concurrently in parallel.",
  },
  {
    question: "Is my personal resume data stored?",
    answer: "No. Security is central to our architecture. All PDF/DOCX parses are computed in-memory, analyzed temporarily, and flushed. We do not store resumes or jobs on persistent disks unless you explicitly click save on your account dashboard.",
  },
  {
    question: "Can I use ARIP for multiple different job target roles?",
    answer: "Yes, you can target completely different job descriptions. The analysis runs dynamically based on the exact job requirements text you paste, allowing custom keyword matches and personalized recommendations for each individual position.",
  },
  {
    question: "What is the accuracy rate of the ATS simulator?",
    answer: "Our ATS Agent simulates over 50 mainstream Application Tracking System parsing parameters. It evaluates exact keyword density, tab/column tables, header parsing accuracy, and date formatting styles to ensure a 97%+ parse rate in enterprise portals.",
  },
];

export function LandingPage() {
  const [activeFAQ, setActiveFAQ] = useState<number | null>(null);
  const [hoveredAgent, setHoveredAgent] = useState<string | null>(null);

  const agentsList = [
    { id: "parser", name: "Doc Parser", desc: "Extracts sections & formats", color: "from-blue-500 to-cyan-400" },
    { id: "ats", name: "ATS Agent", desc: "Validates keyword density", color: "from-amber-500 to-orange-400" },
    { id: "recruiter", name: "Recruiter AI", desc: "Evaluates career metrics", color: "from-red-500 to-rose-400" },
    { id: "coach", name: "Resume Coach", desc: "Suggests inline upgrades", color: "from-emerald-500 to-green-400" },
  ];

  return (
    <div className="relative overflow-hidden w-full bg-background flex flex-col min-h-screen">
      {/* Background glow effects */}
      <div className="absolute inset-0 pointer-events-none -z-10">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/10 rounded-full blur-[140px] opacity-75" />
        <div className="absolute top-1/3 left-1/4 w-[350px] h-[350px] bg-indigo-600/5 rounded-full blur-[100px]" />
        <div className="absolute bottom-1/3 right-1/4 w-[400px] h-[400px] bg-purple-600/5 rounded-full blur-[110px]" />
      </div>

      {/* ── HERO ───────────────────────────────────────────────────────────── */}
      <section className="relative px-6 pt-20 pb-24 text-center max-w-5xl mx-auto flex flex-col items-center">
        <motion.div
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
          className="flex flex-col items-center gap-6"
        >
          <motion.div variants={fadeInUp} className="flex items-center gap-2">
            <Badge variant="ai" className="px-3 py-1 font-semibold">
              <Sparkles className="h-3 w-3 mr-1.5 animate-pulse text-primary" />
              Multi-Agent AI Platform
            </Badge>
            <Badge variant="new">v1.0</Badge>
          </motion.div>

          <motion.h1
            variants={fadeInUp}
            className="text-5xl md:text-8xl font-black tracking-tight leading-[0.9] text-foreground"
          >
            Your Resume,
            <br />
            <span className="bg-gradient-to-r from-primary via-indigo-400 to-violet-400 bg-clip-text text-transparent glow-text">
              Intelligently Optimized
            </span>
          </motion.h1>

          <motion.p
            variants={fadeInUp}
            className="text-base md:text-lg text-muted-foreground max-w-2xl leading-relaxed mt-2"
          >
            Deploy a fleet of specialized AI agents to analyze your resume against any job description. Generate ATS compatibility, recruiter scores, and conceptual optimization recommendations instantly.
          </motion.p>

          <motion.div variants={fadeInUp} className="flex flex-wrap items-center justify-center gap-4 mt-4">
            <Link
              to="/upload"
              className="inline-flex items-center gap-2 h-12 px-8 rounded-xl font-semibold bg-gradient-to-r from-primary to-indigo-500 hover:opacity-90 text-white shadow-xl shadow-primary/20 transition-all active:scale-[0.98]"
            >
              Analyze My Resume
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              to="/report/demo"
              className="inline-flex items-center gap-2 h-12 px-8 rounded-xl font-semibold border border-border/80 bg-card/50 hover:bg-accent/40 text-foreground transition-all active:scale-[0.98]"
            >
              See Sample Report
              <ChevronRight className="h-4 w-4" />
            </Link>
          </motion.div>

          <motion.div
            variants={fadeInUp}
            className="flex items-center gap-6 mt-6 text-xs text-muted-foreground/80 font-medium"
          >
            <span className="flex items-center gap-1.5">
              <Shield className="h-4 w-4 text-success" />
              In-Memory Processing
            </span>
            <span className="flex items-center gap-1.5">
              <Zap className="h-4 w-4 text-warning" />
              Response in &lt;10s
            </span>
            <span className="flex items-center gap-1.5">
              <Star className="h-4 w-4 text-primary" />
              Open Source Base
            </span>
          </motion.div>
        </motion.div>
      </section>

      {/* ── PROBLEM STATEMENT ──────────────────────────────────────────────── */}
      <section className="px-6 py-20 bg-card/25 border-y border-border/40">
        <div className="max-w-4xl mx-auto flex flex-col md:flex-row gap-10 items-center">
          <div className="flex-1 flex flex-col gap-4">
            <Badge variant="danger" className="w-fit">The Problem</Badge>
            <h2 className="text-3xl font-extrabold text-foreground">Why Traditional Resumes Fail ATS Searches</h2>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Applicant Tracking Systems (ATS) reject up to **75% of qualified candidates** due to simple formatting errors, lack of precise keyword matches, or incorrect section structures. Hiring managers spend less than **6 seconds** scanning the remaining profiles.
            </p>
          </div>
          <div className="flex-1 w-full grid grid-cols-1 gap-4">
            <GlassCard className="p-5 flex gap-4 items-start border-l-2 border-l-destructive">
              <div className="bg-destructive/15 p-2 rounded-lg text-destructive shrink-0">
                <Target className="h-5 w-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-foreground">Format Disqualification</h4>
                <p className="text-xs text-muted-foreground mt-1">Multi-column designs, text boxes, and icons cause ATS systems to parse gibberish skills data.</p>
              </div>
            </GlassCard>
            <GlassCard className="p-5 flex gap-4 items-start border-l-2 border-l-warning">
              <div className="bg-warning/15 p-2 rounded-lg text-warning shrink-0">
                <Terminal className="h-5 w-5" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-foreground">Semantic Gap</h4>
                <p className="text-xs text-muted-foreground mt-1">Candidates express requirements conceptually, but standard filters match literal job keywords.</p>
              </div>
            </GlassCard>
          </div>
        </div>
      </section>

      {/* ── MULTI-AGENT AI VISUALIZER ─────────────────────────────────────── */}
      <section className="px-6 py-24 max-w-5xl mx-auto w-full">
        <div className="text-center mb-16">
          <Badge variant="ai" className="mb-3">Orchestration Layer</Badge>
          <h2 className="text-4xl font-extrabold text-foreground">Active Multi-Agent AI Visualizer</h2>
          <p className="text-sm text-muted-foreground mt-2 max-w-lg mx-auto">
            Hover over each specialized agent block to inspect what it contributes in the analysis loop.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {agentsList.map((agent) => (
            <div
              key={agent.id}
              className="relative cursor-pointer"
              onMouseEnter={() => setHoveredAgent(agent.id)}
              onMouseLeave={() => setHoveredAgent(null)}
            >
              <GlassCard
                className={`p-6 border transition-all duration-300 relative overflow-hidden flex flex-col gap-4 items-center text-center h-48 justify-center
                  ${hoveredAgent === agent.id ? "border-primary/60 bg-card/60 shadow-lg scale-102" : "border-border/40"}
                `}
              >
                <div className={`h-12 w-12 rounded-xl bg-gradient-to-br ${agent.color} flex items-center justify-center text-white shrink-0`}>
                  <Cpu className="h-6 w-6" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-foreground">{agent.name}</h4>
                  <p className="text-xs text-muted-foreground mt-1">{agent.desc}</p>
                </div>
              </GlassCard>
            </div>
          ))}
        </div>

        <AnimatePresence>
          {hoveredAgent && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              className="mt-8 p-6 glass-panel rounded-2xl border-primary/20 text-center max-w-xl mx-auto"
            >
              {hoveredAgent === "parser" && (
                <p className="text-xs text-muted-foreground leading-relaxed">
                  <span className="font-bold text-foreground">Document Parser:</span> Utilizes structural layout models to isolate Header, Work Experience, Skills, and Projects sections. Resolves date ranges to chronological orders.
                </p>
              )}
              {hoveredAgent === "ats" && (
                <p className="text-xs text-muted-foreground leading-relaxed">
                  <span className="font-bold text-foreground">ATS Agent:</span> Checks word density, filters, and standard formatting. Validates missing/matched key skill terms needed for initial keyword scoring matrices.
                </p>
              )}
              {hoveredAgent === "recruiter" && (
                <p className="text-xs text-muted-foreground leading-relaxed">
                  <span className="font-bold text-foreground">Recruiter AI:</span> Simulates technical screens. Evaluates whether bullet achievements are quantified (%), metric-backed, or express sufficient leadership scope.
                </p>
              )}
              {hoveredAgent === "coach" && (
                <p className="text-xs text-muted-foreground leading-relaxed">
                  <span className="font-bold text-foreground">Resume Coach:</span> Highlights word discrepancies and suggests immediate inline optimizations, allowing you to accept or reject suggested rewrites.
                </p>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </section>

      {/* ── TECHNOLOGY ────────────────────────────────────────────────────── */}
      <section className="px-6 py-20 bg-card/25 border-y border-border/40">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <Badge variant="premium" className="mb-2">Under the Hood</Badge>
            <h3 className="text-2xl font-bold text-foreground">System Architecture & Tech Stack</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <GlassCard className="p-6 flex flex-col gap-4">
              <Layers className="h-6 w-6 text-primary" />
              <div>
                <h4 className="text-sm font-bold text-foreground">Vector Semantic Matching</h4>
                <p className="text-xs text-muted-foreground mt-1">Converts resumes and job specifications into high-dimensional vectors to calculate contextual relevance and semantic overlap.</p>
              </div>
            </GlassCard>
            <GlassCard className="p-6 flex flex-col gap-4">
              <Database className="h-6 w-6 text-indigo-400" />
              <div>
                <h4 className="text-sm font-bold text-foreground">In-Memory Pipeline</h4>
                <p className="text-xs text-muted-foreground mt-1">All upload extractions are routed through transient queues, safeguarding candidate data under zero-retention principles.</p>
              </div>
            </GlassCard>
            <GlassCard className="p-6 flex flex-col gap-4">
              <BrainCircuit className="h-6 w-6 text-cyan-400" />
              <div>
                <h4 className="text-sm font-bold text-foreground">Agentic Refinement</h4>
                <p className="text-xs text-muted-foreground mt-1">Multi-agent nodes critique raw parse outputs, running structural compliance algorithms before creating the final audit report.</p>
              </div>
            </GlassCard>
          </div>
        </div>
      </section>

      {/* ── FAQ ────────────────────────────────────────────────────────────── */}
      <section className="px-6 py-24 max-w-4xl mx-auto w-full">
        <h3 className="text-3xl font-extrabold text-foreground text-center mb-12">Frequently Asked Questions</h3>
        <div className="flex flex-col gap-4">
          {FAQS.map((faq, idx) => (
            <GlassCard
              key={idx}
              className="p-5 cursor-pointer transition-all duration-300 border-border/40"
              onClick={() => setActiveFAQ(activeFAQ === idx ? null : idx)}
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-bold text-foreground">{faq.question}</span>
                <ChevronDown
                  className={`h-4 w-4 text-muted-foreground transition-transform duration-200
                    ${activeFAQ === idx ? "rotate-180 text-foreground" : ""}
                  `}
                />
              </div>
              <AnimatePresence>
                {activeFAQ === idx && (
                  <motion.div
                    initial={{ height: 0, opacity: 0, marginTop: 0 }}
                    animate={{ height: "auto", opacity: 1, marginTop: 12 }}
                    exit={{ height: 0, opacity: 0, marginTop: 0 }}
                    className="overflow-hidden"
                  >
                    <p className="text-xs text-muted-foreground leading-relaxed border-t border-border/30 pt-3">
                      {faq.answer}
                    </p>
                  </motion.div>
                )}
              </AnimatePresence>
            </GlassCard>
          ))}
        </div>
      </section>

      {/* ── BOTTOM CTA ─────────────────────────────────────────────────────── */}
      <section className="px-6 py-20 text-center max-w-2xl mx-auto">
        <h3 className="text-3xl font-black text-foreground">Stop Guessing. Start Optimizing.</h3>
        <p className="text-sm text-muted-foreground mt-2 mb-8">
          Upload your resume and the target role specification to receive your agentic audit report in seconds.
        </p>
        <Link
          to="/upload"
          className="inline-flex items-center gap-2 h-12 px-8 rounded-xl font-semibold bg-gradient-to-r from-primary to-indigo-500 hover:opacity-90 text-white shadow-xl shadow-primary/20 transition-all active:scale-[0.98] mx-auto w-fit"
        >
          Analyze Resume Now
          <ArrowRight className="h-4 w-4" />
        </Link>
      </section>

      {/* ── FOOTER ─────────────────────────────────────────────────────────── */}
      <footer className="border-t border-border/40 bg-card/20 px-6 py-10 text-center text-xs text-muted-foreground">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <BrainCircuit className="h-4 w-4 text-primary" />
            <span className="font-bold text-foreground">ARIP</span>
            <span>· AI Resume Intelligence Platform</span>
          </div>
          <p>© {new Date().getFullYear()} ARIP. In-memory local processing workspace.</p>
        </div>
      </footer>
    </div>
  );
}
