import { useMutation, useQuery } from "@tanstack/react-query";
import { authService } from "../services/auth.service";
import { useAuthStore } from "../store/authStore";

export function useAuth() {
  const { setAuth, logout, user } = useAuthStore();

  const loginMutation = useMutation({
    mutationFn: async (credentials: any) => {
      const data = await authService.login(credentials);
      return data;
    },
    onSuccess: (data) => {
      setAuth(data.access_token, data.refresh_token, data.user);
    },
  });

  const logoutMutation = useMutation({
    mutationFn: async () => {
      try {
        await authService.logout();
      } catch (e) {
        // Continue logout locally even if server call fails
      }
    },
    onSuccess: () => {
      logout();
    },
  });

  const profileQuery = useQuery({
    queryKey: ["auth-profile"],
    queryFn: () => authService.getProfile(),
    enabled: useAuthStore((s) => s.isAuthenticated()),
  });

  return {
    login: loginMutation.mutateAsync,
    isLoggingIn: loginMutation.isPending,
    loginError: loginMutation.error,
    logout: logoutMutation.mutate,
    user,
    profile: profileQuery.data,
    isLoadingProfile: profileQuery.isLoading,
  };
}
