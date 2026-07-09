import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";

export function ProtectedRoute({ children }: { children?: React.ReactNode }) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated());

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children ? <>{children}</> : <Outlet />;
}
export default ProtectedRoute;
