import * as React from "react";
import { Upload, X } from "lucide-react";
import { cn } from "../../lib/utils";

// ── 1. Input ─────────────────────────────────────────────────────────────────
export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = "text", label, error, ...props }, ref) => {
    return (
      <div className="flex flex-col gap-1.5 w-full">
        {label && (
          <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            {label}
          </label>
        )}
        <input
          type={type}
          ref={ref}
          className={cn(
            "flex h-10 w-full rounded-lg border border-border bg-card/40 px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground/60 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring focus-visible:border-primary disabled:cursor-not-allowed disabled:opacity-50 transition-all",
            error && "border-destructive focus-visible:ring-destructive",
            className
          )}
          {...props}
        />
        {error && <span className="text-xs text-destructive">{error}</span>}
      </div>
    );
  }
);
Input.displayName = "Input";

// ── 2. Textarea ──────────────────────────────────────────────────────────────
export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
}

export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, label, error, ...props }, ref) => {
    return (
      <div className="flex flex-col gap-1.5 w-full">
        {label && (
          <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          className={cn(
            "flex min-h-[80px] w-full rounded-lg border border-border bg-card/40 px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground/60 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 transition-all",
            error && "border-destructive focus-visible:ring-destructive",
            className
          )}
          {...props}
        />
        {error && <span className="text-xs text-destructive">{error}</span>}
      </div>
    );
  }
);
Textarea.displayName = "Textarea";

// ── 3. Select ────────────────────────────────────────────────────────────────
export interface SelectProps
  extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  options: { label: string; value: string }[];
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, label, error, options, ...props }, ref) => {
    return (
      <div className="flex flex-col gap-1.5 w-full">
        {label && (
          <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            {label}
          </label>
        )}
        <select
          ref={ref}
          className={cn(
            "flex h-10 w-full rounded-lg border border-border bg-card/40 px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 transition-all cursor-pointer",
            error && "border-destructive focus-visible:ring-destructive",
            className
          )}
          {...props}
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value} className="bg-card text-foreground">
              {opt.label}
            </option>
          ))}
        </select>
        {error && <span className="text-xs text-destructive">{error}</span>}
      </div>
    );
  }
);
Select.displayName = "Select";

// ── 4. Switch ────────────────────────────────────────────────────────────────
export const Switch = React.forwardRef<
  HTMLInputElement,
  React.InputHTMLAttributes<HTMLInputElement> & { label?: string }
>(({ className, label, ...props }, ref) => {
  return (
    <label className="flex items-center gap-3 cursor-pointer select-none">
      <div className="relative">
        <input
          type="checkbox"
          ref={ref}
          className="sr-only peer"
          {...props}
        />
        <div className="w-11 h-6 bg-muted peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-border after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
      </div>
      {label && <span className="text-sm text-foreground">{label}</span>}
    </label>
  );
});
Switch.displayName = "Switch";

// ── 5. File Upload Placeholder ───────────────────────────────────────────────
export function FileUploadPlaceholder({
  onFileDrop,
  acceptLabel = "PDF, DOCX up to 10MB",
}: {
  onFileDrop?: (file: File) => void;
  acceptLabel?: string;
}) {
  const [dragActive, setDragActive] = React.useState(false);
  const [selectedFile, setSelectedFile] = React.useState<File | null>(null);
  const inputRef = React.useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setSelectedFile(file);
      onFileDrop?.(file);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      onFileDrop?.(file);
    }
  };

  return (
    <div
      onDragEnter={handleDrag}
      onDragOver={handleDrag}
      onDragLeave={handleDrag}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
      className={cn(
        "border border-dashed border-border/80 hover:border-primary/50 bg-card/25 backdrop-blur-sm rounded-xl p-8 flex flex-col items-center justify-center gap-3 cursor-pointer transition-all duration-300 min-h-[180px] group",
        dragActive && "border-primary bg-primary/5",
        selectedFile && "border-success/50 bg-success/5 hover:border-success/70"
      )}
    >
      <input
        ref={inputRef}
        type="file"
        className="hidden"
        onChange={handleChange}
        accept=".pdf,.docx"
      />
      {selectedFile ? (
        <div className="flex flex-col items-center gap-2">
          <div className="h-10 w-10 rounded-lg bg-success/20 flex items-center justify-center">
            <Upload className="h-5 w-5 text-success animate-bounce" />
          </div>
          <span className="text-sm font-medium text-foreground max-w-[240px] truncate">
            {selectedFile.name}
          </span>
          <button
            onClick={(e) => {
              e.stopPropagation();
              setSelectedFile(null);
            }}
            className="text-xs text-muted-foreground hover:text-destructive flex items-center gap-1 mt-1 px-2 py-1 rounded hover:bg-accent/40 transition-all"
          >
            <X className="h-3 w-3" /> Remove file
          </button>
        </div>
      ) : (
        <>
          <div className="h-12 w-12 rounded-xl bg-accent/40 flex items-center justify-center group-hover:scale-105 transition-transform">
            <Upload className="h-5 w-5 text-muted-foreground group-hover:text-primary transition-colors" />
          </div>
          <div className="flex flex-col items-center text-center gap-1">
            <span className="text-sm font-semibold text-foreground">
              Drag & drop document or <span className="text-primary underline">browse</span>
            </span>
            <span className="text-xs text-muted-foreground/80">{acceptLabel}</span>
          </div>
        </>
      )}
    </div>
  );
}
