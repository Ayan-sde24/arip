import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { Lock, Mail, ArrowRight, BrainCircuit } from "lucide-react";
import { useAuthStore } from "../store/authStore";
import { AuthLayout } from "../layouts/AuthLayout";
import { Button } from "../components/ui/Button";

const loginSchema = z.object({
  email: z.string().email({ message: "Invalid email address" }),
  password: z.string().min(6, { message: "Password must be at least 6 characters" }),
  rememberMe: z.boolean().optional(),
});

type LoginSchemaInput = z.infer<typeof loginSchema>;

export function LoginPage() {
  const navigate = useNavigate();
  const setAuth = useAuthStore((s) => s.setAuth);
  const setRememberMe = useAuthStore((s) => s.setRememberMe);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginSchemaInput>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
      rememberMe: false,
    },
  });

  async function onSubmit(data: LoginSchemaInput) {
    // Simulate JWT authentication API endpoints integration
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Save tokens and mock user credentials
    setAuth("mock-access-token", "mock-refresh-token", {
      id: "usr-9281",
      email: data.email,
      name: "ARIP Candidate",
    });

    if (data.rememberMe) {
      setRememberMe(true);
    }

    navigate("/dashboard");
  }

  return (
    <AuthLayout>
      <div className="flex flex-col gap-6 w-full max-w-md bg-card/65 backdrop-blur-xl border border-border/40 p-8 rounded-2xl shadow-glass relative overflow-hidden">
        {/* Header */}
        <div className="flex flex-col items-center gap-3 text-center">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-primary to-indigo-500 flex items-center justify-center shadow-lg shadow-primary/20 shrink-0">
            <BrainCircuit className="h-5 w-5 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-foreground">Sign In to ARIP</h2>
            <p className="text-xs text-muted-foreground mt-1">Multi-agent resume analysis workspace.</p>
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 mt-2">
          {/* Email input */}
          <div className="flex flex-col gap-1.5">
            <label className="text-[10px] uppercase tracking-wider font-bold text-muted-foreground pl-1">
              Email Address
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type="email"
                placeholder="you@example.com"
                {...register("email")}
                className="w-full bg-accent/20 border border-border/60 rounded-xl pl-10 pr-4 py-2.5 text-xs text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-primary/40"
              />
            </div>
            {errors.email && (
              <span className="text-[10px] font-semibold text-destructive pl-1">
                {errors.email.message}
              </span>
            )}
          </div>

          {/* Password input */}
          <div className="flex flex-col gap-1.5">
            <label className="text-[10px] uppercase tracking-wider font-bold text-muted-foreground pl-1">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type="password"
                placeholder="••••••••"
                {...register("password")}
                className="w-full bg-accent/20 border border-border/60 rounded-xl pl-10 pr-4 py-2.5 text-xs text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-primary/40"
              />
            </div>
            {errors.password && (
              <span className="text-[10px] font-semibold text-destructive pl-1">
                {errors.password.message}
              </span>
            )}
          </div>

          {/* Remember me trigger */}
          <div className="flex items-center justify-between text-xs mt-1">
            <label className="flex items-center gap-2 cursor-pointer select-none">
              <input
                type="checkbox"
                {...register("rememberMe")}
                className="h-4 w-4 rounded border-border/60 text-primary focus:ring-primary accent-primary"
              />
              <span className="text-muted-foreground">Remember me</span>
            </label>
          </div>

          <Button
            variant="gradient"
            size="lg"
            isLoading={isSubmitting}
            type="submit"
            className="w-full mt-2 flex items-center justify-center gap-2"
          >
            Sign In
            <ArrowRight className="h-4 w-4" />
          </Button>
        </form>
      </div>
    </AuthLayout>
  );
}
export default LoginPage;
