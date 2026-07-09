import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import {
  BrainCircuit,
  Sparkles,
  FileSearch,
  BarChart3,
  Target,
  ArrowRight,
  ChevronRight,
  Zap,
  Shield,
  Star,
} from "lucide-react";
import { Button } from "../components/ui/Button";
import { Badge } from "../components/ui/Badge";
import { GlassCard, FeatureCard } from "../components/cards/Cards";
import { staggerContainer, fadeInUp } from "../animations/variants";

const features = [
  {
    icon: FileSearch,
    title: "Deep Resume Parsing",
    description:
      "Multi-layer document intelligence extracts every section, entity, and skill from your resume with surgical precision.",
  },
  {
    icon: Target,
    title: "ATS Intelligence",
    description:
      "Our ATS agent simulates 50+ real ATS systems, scoring keyword density, section structure, and format compliance.",
  },
  {
    icon: BrainCircuit,
    title: "Recruiter Simulation",
    description:
      "A recruiter agent evaluates your resume's narrative quality, impact metrics, and leadership signals in seconds.",
  },
  {
    icon: Sparkles,
    title: "AI Resume Coach",
    description:
      "Receive specific rewrites, bullet upgrades, and keyword injections tailored to the exact job description.",
  },
  {
    icon: BarChart3,
    title: "Semantic Match Engine",
    description:
      "Vector-based semantic analysis scores conceptual alignment between your experience and job requirements.",
  },
  {
    icon: Zap,
    title: "Instant Results",
    description:
      "Multi-agent pipeline runs in parallel, delivering a comprehensive analysis report in under 30 seconds.",
  },
];

const stats = [
  { value: "50+", label: "ATS Systems Simulated" },
  { value: "97%", label: "Parse Accuracy" },
  { value: "5", label: "Specialized AI Agents" },
  { value: "<30s", label: "Analysis Time" },
];

export function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* ── Hero ───────────────────────────────────────────────────────────── */}
      <section className="relative flex-1 flex flex-col items-center justify-center text-center px-6 py-24 overflow-hidden">
        {/* Background glow effects */}
        <div className="absolute inset-0 pointer-events-none -z-10">
          <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/10 rounded-full blur-[120px]" />
          <div className="absolute top-1/2 left-1/4 w-[300px] h-[300px] bg-indigo-600/8 rounded-full blur-[80px]" />
          <div className="absolute bottom-1/4 right-1/4 w-[250px] h-[250px] bg-violet-600/8 rounded-full blur-[80px]" />
        </div>

        <motion.div
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
          className="max-w-4xl mx-auto flex flex-col items-center gap-6"
        >
          {/* Eyebrow badge */}
          <motion.div variants={fadeInUp} className="flex items-center gap-2">
            <Badge variant="ai">
              <Sparkles className="h-2.5 w-2.5 mr-1" />
              Multi-Agent AI Platform
            </Badge>
            <Badge variant="new">v1.0</Badge>
          </motion.div>

          {/* Headline */}
          <motion.h1
            variants={fadeInUp}
            className="text-5xl md:text-7xl font-black tracking-tight leading-none"
          >
            <span className="text-foreground">Your Resume,</span>
            <br />
            <span className="bg-gradient-to-r from-primary via-indigo-400 to-violet-400 bg-clip-text text-transparent">
              Intelligently Optimized
            </span>
          </motion.h1>

          {/* Subheadline */}
          <motion.p
            variants={fadeInUp}
            className="text-lg text-muted-foreground max-w-2xl leading-relaxed"
          >
            ARIP deploys a fleet of specialized AI agents to analyze your resume
            against any job description — scoring ATS compatibility, recruiter
            appeal, and semantic alignment in one unified report.
          </motion.p>

          {/* CTA buttons */}
          <motion.div variants={fadeInUp} className="flex items-center gap-4 mt-2">
            <Button variant="gradient" size="lg" asChild>
              <Link to="/upload" className="flex items-center gap-2">
                Analyze My Resume
                <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <Link to="/report/demo" className="flex items-center gap-2">
                See Sample Report
                <ChevronRight className="h-4 w-4" />
              </Link>
            </Button>
          </motion.div>

          {/* Trust signals */}
          <motion.div
            variants={fadeInUp}
            className="flex items-center gap-6 mt-4 text-xs text-muted-foreground"
          >
            <span className="flex items-center gap-1">
              <Shield className="h-3.5 w-3.5 text-success" />
              No data stored
            </span>
            <span className="flex items-center gap-1">
              <Zap className="h-3.5 w-3.5 text-warning" />
              Results in 30s
            </span>
            <span className="flex items-center gap-1">
              <Star className="h-3.5 w-3.5 text-primary" />
              Free to use
            </span>
          </motion.div>
        </motion.div>
      </section>

      {/* ── Stats Bar ──────────────────────────────────────────────────────── */}
      <section className="border-y border-border/40 bg-card/30 px-6 py-10">
        <div className="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="text-center"
            >
              <div className="text-4xl font-black text-primary mb-1">{stat.value}</div>
              <div className="text-xs text-muted-foreground font-medium uppercase tracking-wider">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── Features ───────────────────────────────────────────────────────── */}
      <section className="px-6 py-24 max-w-6xl mx-auto w-full">
        <div className="text-center mb-16">
          <Badge variant="premium" className="mb-4">Platform Features</Badge>
          <h2 className="text-4xl font-bold text-foreground mb-4">
            Five Agents. One Report.
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto">
            Each agent is purpose-built and independently optimized. Together
            they produce the most comprehensive resume analysis available.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.08 }}
            >
              <FeatureCard
                title={feature.title}
                description={feature.description}
                icon={feature.icon}
              />
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── Pipeline Visual ────────────────────────────────────────────────── */}
      <section className="px-6 py-20 bg-card/20 border-y border-border/30">
        <div className="max-w-5xl mx-auto text-center mb-12">
          <h2 className="text-3xl font-bold text-foreground mb-3">
            How It Works
          </h2>
          <p className="text-muted-foreground">
            From upload to optimization report in three steps.
          </p>
        </div>
        <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              step: "01",
              title: "Upload Documents",
              desc: "Drop your resume (PDF/DOCX) and paste or upload the job description.",
            },
            {
              step: "02",
              title: "Agents Analyze",
              desc: "5 specialized agents run in parallel — ATS, Recruiter, Semantic, Coach, and Parser.",
            },
            {
              step: "03",
              title: "Get Your Report",
              desc: "Receive a scored report with specific rewrites, keyword suggestions, and an optimized resume.",
            },
          ].map((item, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.12 }}
            >
              <GlassCard className="relative text-center py-8 px-6">
                <div className="text-6xl font-black text-primary/20 mb-4 leading-none">
                  {item.step}
                </div>
                <h3 className="font-bold text-foreground mb-2">{item.title}</h3>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  {item.desc}
                </p>
              </GlassCard>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── Bottom CTA ─────────────────────────────────────────────────────── */}
      <section className="px-6 py-24 text-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.97 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="max-w-2xl mx-auto"
        >
          <h2 className="text-4xl font-black text-foreground mb-4">
            Ready to land the interview?
          </h2>
          <p className="text-muted-foreground mb-8">
            Upload your resume and job description. Get your analysis in 30 seconds.
          </p>
          <Button variant="gradient" size="lg" asChild>
            <Link to="/upload" className="flex items-center gap-2 mx-auto w-fit">
              Start Free Analysis
              <ArrowRight className="h-4 w-4" />
            </Link>
          </Button>
        </motion.div>
      </section>
    </div>
  );
}
