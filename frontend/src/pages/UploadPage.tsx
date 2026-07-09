import * as React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Upload, FileText, Briefcase, ArrowRight, CheckCircle, X } from "lucide-react";
import { Button } from "../components/ui/Button";
import { Alert } from "../components/feedback/Feedback";
import { GlassPanel } from "../components/layout/Containers";
import { Badge } from "../components/ui/Badge";
import { uploadResume, uploadJob, runAnalysis } from "../services/api";
import { staggerContainer, fadeInUp } from "../animations/variants";

type UploadStep = "upload" | "running";

interface UploadedFile {
  file: File;
  documentId: string;
}

export function UploadPage() {
  const navigate = useNavigate();
  const [step, setStep] = React.useState<UploadStep>("upload");
  const [resumeUploaded, setResumeUploaded] = React.useState<UploadedFile | null>(null);
  const [jobUploaded, setJobUploaded] = React.useState<UploadedFile | null>(null);
  const [error, setError] = React.useState<string | null>(null);
  const [uploading, setUploading] = React.useState<"resume" | "job" | null>(null);

  const resumeInputRef = React.useRef<HTMLInputElement>(null);
  const jobInputRef = React.useRef<HTMLInputElement>(null);

  // ── Drag & Drop state
  const [resumeDragging, setResumeDragging] = React.useState(false);
  const [jobDragging, setJobDragging] = React.useState(false);

  async function handleResumeFile(file: File) {
    if (!file) return;
    setUploading("resume");
    setError(null);
    try {
      const { document_id } = await uploadResume(file);
      setResumeUploaded({ file, documentId: document_id });
    } catch (e: any) {
      setError(`Resume upload failed: ${e.message}`);
    } finally {
      setUploading(null);
    }
  }

  async function handleJobFile(file: File) {
    if (!file) return;
    setUploading("job");
    setError(null);
    try {
      const { document_id } = await uploadJob(file);
      setJobUploaded({ file, documentId: document_id });
    } catch (e: any) {
      setError(`Job description upload failed: ${e.message}`);
    } finally {
      setUploading(null);
    }
  }

  async function handleAnalyze() {
    if (!resumeUploaded || !jobUploaded) return;
    setStep("running");
    setError(null);
    try {
      const { analysis_id } = await runAnalysis({
        resume_id: resumeUploaded.documentId,
        job_id: jobUploaded.documentId,
      });
      navigate(`/analysis/${analysis_id}`);
    } catch (e: any) {
      setError(`Analysis failed: ${e.message}`);
      setStep("upload");
    }
  }

  const canAnalyze = resumeUploaded && jobUploaded && step === "upload";

  return (
    <div className="max-w-3xl mx-auto px-6 py-16">
      <motion.div
        variants={staggerContainer}
        initial="hidden"
        animate="visible"
        className="flex flex-col gap-8"
      >
        {/* Header */}
        <motion.div variants={fadeInUp} className="text-center">
          <Badge variant="ai" className="mb-4">Step 1 of 2</Badge>
          <h1 className="text-4xl font-black tracking-tight text-foreground mb-3">
            Upload Your Documents
          </h1>
          <p className="text-muted-foreground">
            Upload your resume and the job description you are targeting.
            Supported formats: PDF, DOCX.
          </p>
        </motion.div>

        {error && (
          <motion.div variants={fadeInUp}>
            <Alert variant="error" title="Upload Error" description={error} />
          </motion.div>
        )}

        {/* Drop zones */}
        <motion.div variants={fadeInUp} className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Resume drop zone */}
          <DropZone
            label="Resume"
            icon={FileText}
            uploaded={resumeUploaded}
            dragging={resumeDragging}
            uploading={uploading === "resume"}
            onDragOver={(e) => { e.preventDefault(); setResumeDragging(true); }}
            onDragLeave={() => setResumeDragging(false)}
            onDrop={(e) => {
              e.preventDefault();
              setResumeDragging(false);
              const f = e.dataTransfer.files[0];
              if (f) handleResumeFile(f);
            }}
            onClick={() => resumeInputRef.current?.click()}
            onClear={() => setResumeUploaded(null)}
          >
            <input
              ref={resumeInputRef}
              type="file"
              accept=".pdf,.docx"
              className="hidden"
              onChange={(e) => {
                const f = e.target.files?.[0];
                if (f) handleResumeFile(f);
              }}
            />
          </DropZone>

          {/* Job Description drop zone */}
          <DropZone
            label="Job Description"
            icon={Briefcase}
            uploaded={jobUploaded}
            dragging={jobDragging}
            uploading={uploading === "job"}
            onDragOver={(e) => { e.preventDefault(); setJobDragging(true); }}
            onDragLeave={() => setJobDragging(false)}
            onDrop={(e) => {
              e.preventDefault();
              setJobDragging(false);
              const f = e.dataTransfer.files[0];
              if (f) handleJobFile(f);
            }}
            onClick={() => jobInputRef.current?.click()}
            onClear={() => setJobUploaded(null)}
          >
            <input
              ref={jobInputRef}
              type="file"
              accept=".pdf,.docx,.txt"
              className="hidden"
              onChange={(e) => {
                const f = e.target.files?.[0];
                if (f) handleJobFile(f);
              }}
            />
          </DropZone>
        </motion.div>

        {/* Analyze button */}
        <motion.div variants={fadeInUp} className="flex justify-center">
          <Button
            variant="gradient"
            size="lg"
            disabled={!canAnalyze}
            isLoading={step === "running"}
            onClick={handleAnalyze}
            className="min-w-[220px] flex items-center gap-2"
          >
            Run Multi-Agent Analysis
            <ArrowRight className="h-4 w-4" />
          </Button>
        </motion.div>

        {/* Info note */}
        <motion.div variants={fadeInUp}>
          <GlassPanel className="text-center py-4">
            <p className="text-xs text-muted-foreground">
              Files are processed in memory and never stored on disk.
              Analysis takes approximately 20–40 seconds.
            </p>
          </GlassPanel>
        </motion.div>
      </motion.div>
    </div>
  );
}

// ── Drop Zone Sub-component ───────────────────────────────────────────────────

function DropZone({
  label,
  icon: Icon,
  uploaded,
  dragging,
  uploading,
  onDragOver,
  onDragLeave,
  onDrop,
  onClick,
  onClear,
  children,
}: {
  label: string;
  icon: React.ElementType;
  uploaded: UploadedFile | null;
  dragging: boolean;
  uploading: boolean;
  onDragOver: React.DragEventHandler;
  onDragLeave: React.DragEventHandler;
  onDrop: React.DragEventHandler;
  onClick: () => void;
  onClear: () => void;
  children: React.ReactNode;
}) {
  return (
    <div
      onDragOver={onDragOver}
      onDragLeave={onDragLeave}
      onDrop={onDrop}
      onClick={uploaded ? undefined : onClick}
      className={`relative flex flex-col items-center justify-center gap-4 rounded-xl border-2 border-dashed p-8 min-h-[200px] transition-all duration-200 cursor-pointer
        ${dragging ? "border-primary bg-primary/8 scale-[1.01]" : "border-border/60 bg-card/40 hover:border-primary/50 hover:bg-card/60"}
        ${uploaded ? "cursor-default border-success/50 bg-success/5" : ""}
        ${uploading ? "pointer-events-none opacity-70 animate-pulse" : ""}
      `}
    >
      {children}

      {uploaded ? (
        <>
          <CheckCircle className="h-10 w-10 text-success" />
          <div className="text-center">
            <p className="text-sm font-semibold text-foreground">{uploaded.file.name}</p>
            <p className="text-xs text-muted-foreground mt-1">
              {(uploaded.file.size / 1024).toFixed(0)} KB · Uploaded
            </p>
          </div>
          <button
            onClick={(e) => { e.stopPropagation(); onClear(); }}
            className="absolute top-3 right-3 p-1 rounded-full text-muted-foreground hover:text-foreground hover:bg-accent/40 transition-all"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        </>
      ) : uploading ? (
        <>
          <Icon className="h-10 w-10 text-primary animate-pulse" />
          <p className="text-sm font-medium text-foreground">Uploading…</p>
        </>
      ) : (
        <>
          <div className="h-14 w-14 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center">
            <Icon className="h-7 w-7 text-primary" />
          </div>
          <div className="text-center">
            <p className="font-semibold text-sm text-foreground">{label}</p>
            <p className="text-xs text-muted-foreground mt-1">
              Drop file here or click to browse
            </p>
            <p className="text-[10px] text-muted-foreground/60 mt-0.5">
              PDF, DOCX up to 10MB
            </p>
          </div>
          <div className="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity rounded-xl">
            <Upload className="h-5 w-5 text-primary" />
          </div>
        </>
      )}
    </div>
  );
}
