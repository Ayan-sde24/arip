import { create } from "zustand";
import { persist } from "zustand/middleware";

interface UserProfile {
  id: string;
  email: string;
  name?: string;
}

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  user: UserProfile | null;
  rememberMe: boolean;
  setAuth: (access: string, refresh: string, user: UserProfile) => void;
  setAccessToken: (access: string) => void;
  setRememberMe: (remember: boolean) => void;
  logout: () => void;
  isAuthenticated: () => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      accessToken: null,
      refreshToken: null,
      user: null,
      rememberMe: false,
      setAuth: (accessToken, refreshToken, user) =>
        set({ accessToken, refreshToken, user }),
      setAccessToken: (accessToken) => set({ accessToken }),
      setRememberMe: (rememberMe) => set({ rememberMe }),
      logout: () => set({ accessToken: null, refreshToken: null, user: null }),
      isAuthenticated: () => !!get().accessToken,
    }),
    {
      name: "arip-auth",
    }
  )
);
