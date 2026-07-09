import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDropzone } from "react-dropzone";
import { motion } from "framer-motion";
import {
  FileText,
  Briefcase,
  ArrowRight,
  CheckCircle,
  X,
  FileCode,
  Sparkles,
} from "lucide-react";
import { Button } from "../components/ui/Button";
import { Alert } from "../components/feedback/Feedback";
import { GlassPanel } from "../components/layout/Containers";
import { Badge } from "../components/ui/Badge";
import { staggerContainer, fadeInUp } from "../animations/variants";

interface UploadedFile {
  name: string;
  size: number;
}

export function UploadPage() {
  const navigate = useNavigate();
  const [resume, setResume] = useState<UploadedFile | null>(null);
  const [jobDescription, setJobDescription] = useState<UploadedFile | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [isUploading, setIsUploading] = useState(false);

  // Resume Dropzone configuration
  const {
    getRootProps: getResumeRootProps,
    getInputProps: getResumeInputProps,
    isDragActive: isResumeDragActive,
  } = useDropzone({
    onDrop: (files) => {
      if (files[0]) {
        setResume({ name: files[0].name, size: files[0].size });
        setError(null);
      }
    },
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
    },
    maxFiles: 1,
  });

  // Job Description Dropzone configuration
  const {
    getRootProps: getJobRootProps,
    getInputProps: getJobInputProps,
    isDragActive: isJobDragActive,
  } = useDropzone({
    onDrop: (files) => {
      if (files[0]) {
        setJobDescription({ name: files[0].name, size: files[0].size });
        setError(null);
      }
    },
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
      "text/plain": [".txt"],
    },
    maxFiles: 1,
  });

  const recentUploads = [
    { name: "Alex_Mercer_Resume_V4.pdf", type: "Resume", date: "Today, 10:14 AM" },
    { name: "Senior_Fullstack_Eng_JD.pdf", type: "JD", date: "Today, 10:12 AM" },
  ];

  function handleStartAnalysis() {
    if (!resume || !jobDescription) return;
    setIsUploading(true);
    setError(null);

    // Simulate upload progress
    let prog = 0;
    const interval = setInterval(() => {
      prog += 20;
      setUploadProgress(prog);
      if (prog >= 100) {
        clearInterval(interval);
        setTimeout(() => {
          setIsUploading(false);
          // Route to active analysis workspace with a randomly generated analysis id
          navigate(`/analysis/an-${Math.floor(1000 + Math.random() * 9000)}`);
        }, 300);
      }
    }, 150);
  }

  const canAnalyze = resume && jobDescription && !isUploading;

  return (
    <div className="max-w-4xl mx-auto px-6 py-12 flex flex-col gap-8 w-full">
      <motion.div
        variants={staggerContainer}
        initial="hidden"
        animate="visible"
        className="flex flex-col gap-8 w-full"
      >
        {/* Header */}
        <motion.div variants={fadeInUp} className="text-center">
          <Badge variant="ai" className="mb-3">Workspace Core</Badge>
          <h1 className="text-4xl font-black tracking-tight text-foreground mb-2">
            Initiate AI Resume Audit
          </h1>
          <p className="text-sm text-muted-foreground max-w-xl mx-auto leading-relaxed">
            Drag and drop your candidate resume alongside the target job specification text.
            Our agents process the files concurrently.
          </p>
        </motion.div>

        {error && (
          <motion.div variants={fadeInUp}>
            <Alert variant="error" title="Upload Error" description={error} />
          </motion.div>
        )}

        {/* Upload Panels */}
        <motion.div variants={fadeInUp} className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
          {/* Resume Upload panel */}
          <div className="flex flex-col gap-2">
            <span className="text-xs font-bold text-foreground/80 pl-1 uppercase tracking-wider">Candidate Resume</span>
            <div
              {...getResumeRootProps()}
              className={`relative min-h-[220px] rounded-2xl border-2 border-dashed flex flex-col items-center justify-center p-6 transition-all duration-200 cursor-pointer
                ${isResumeDragActive ? "border-primary bg-primary/10 scale-101" : "border-border/60 bg-card/30 hover:border-primary/40 hover:bg-card/50"}
                ${resume ? "border-success/50 bg-success/5 hover:border-success/60" : ""}
              `}
            >
              <input {...getResumeInputProps()} />
              {resume ? (
                <div className="flex flex-col items-center gap-3 text-center w-full">
                  <CheckCircle className="h-10 w-10 text-success" />
                  <div>
                    <p className="text-xs font-bold text-foreground max-w-[200px] truncate">{resume.name}</p>
                    <p className="text-[10px] text-muted-foreground mt-1">{(resume.size / 1024).toFixed(1)} KB</p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setResume(null);
                    }}
                    className="absolute top-3 right-3 p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-accent/40 transition-colors"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              ) : (
                <div className="flex flex-col items-center gap-4 text-center">
                  <div className="h-12 w-12 rounded-xl bg-primary/15 flex items-center justify-center text-primary border border-primary/20">
                    <FileText className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="text-xs font-bold text-foreground">Upload Resume PDF / DOCX</p>
                    <p className="text-[10px] text-muted-foreground mt-1">Drag file here or click to browse</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Job Specification panel */}
          <div className="flex flex-col gap-2">
            <span className="text-xs font-bold text-foreground/80 pl-1 uppercase tracking-wider">Job Specification</span>
            <div
              {...getJobRootProps()}
              className={`relative min-h-[220px] rounded-2xl border-2 border-dashed flex flex-col items-center justify-center p-6 transition-all duration-200 cursor-pointer
                ${isJobDragActive ? "border-primary bg-primary/10 scale-101" : "border-border/60 bg-card/30 hover:border-primary/40 hover:bg-card/50"}
                ${jobDescription ? "border-success/50 bg-success/5 hover:border-success/60" : ""}
              `}
            >
              <input {...getJobInputProps()} />
              {jobDescription ? (
                <div className="flex flex-col items-center gap-3 text-center w-full">
                  <CheckCircle className="h-10 w-10 text-success" />
                  <div>
                    <p className="text-xs font-bold text-foreground max-w-[200px] truncate">{jobDescription.name}</p>
                    <p className="text-[10px] text-muted-foreground mt-1">{(jobDescription.size / 1024).toFixed(1)} KB</p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setJobDescription(null);
                    }}
                    className="absolute top-3 right-3 p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-accent/40 transition-colors"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              ) : (
                <div className="flex flex-col items-center gap-4 text-center">
                  <div className="h-12 w-12 rounded-xl bg-indigo-500/15 flex items-center justify-center text-indigo-400 border border-indigo-500/20">
                    <Briefcase className="h-5 w-5" />
                  </div>
                  <div>
                    <p className="text-xs font-bold text-foreground">Upload JD PDF / TXT</p>
                    <p className="text-[10px] text-muted-foreground mt-1">Drag file here or click to browse</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </motion.div>

        {/* Start button & upload progress bar */}
        <motion.div variants={fadeInUp} className="flex flex-col items-center gap-4 w-full">
          {isUploading && (
            <div className="w-full max-w-md bg-accent/20 rounded-full h-1.5 overflow-hidden">
              <motion.div
                className="bg-primary h-full rounded-full"
                animate={{ width: `${uploadProgress}%` }}
                transition={{ duration: 0.1 }}
              />
            </div>
          )}
          <Button
            variant="gradient"
            size="lg"
            disabled={!canAnalyze}
            isLoading={isUploading}
            onClick={handleStartAnalysis}
            className="min-w-[240px] flex items-center gap-2"
          >
            <Sparkles className="h-4 w-4 mr-1 text-white" />
            Analyze Target Match
            <ArrowRight className="h-4 w-4" />
          </Button>
        </motion.div>

        {/* Recent Uploads grid */}
        <motion.div variants={fadeInUp} className="flex flex-col gap-3 w-full">
          <span className="text-xs font-bold text-foreground/80 pl-1 uppercase tracking-wider">Recent Local Uploads</span>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recentUploads.map((item, idx) => (
              <GlassPanel key={idx} className="flex items-center justify-between p-4 border-border/40">
                <div className="flex items-center gap-3">
                  <FileCode className="h-5 w-5 text-muted-foreground shrink-0" />
                  <div>
                    <p className="text-xs font-bold text-foreground">{item.name}</p>
                    <p className="text-[10px] text-muted-foreground mt-0.5">{item.type} · {item.date}</p>
                  </div>
                </div>
              </GlassPanel>
            ))}
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
}
