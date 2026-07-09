import { create } from "zustand";
import { persist } from "zustand/middleware";

interface UserPreferences {
  atsSensitivity: number;
  recruiterSensitivity: number;
  emailNotifications: boolean;
  pushNotifications: boolean;
}

interface UserStoreState {
  preferences: UserPreferences;
  updatePreferences: (update: Partial<UserPreferences>) => void;
  resetPreferences: () => void;
}

const defaultPreferences: UserPreferences = {
  atsSensitivity: 70,
  recruiterSensitivity: 80,
  emailNotifications: true,
  pushNotifications: false,
};

export const useUserStore = create<UserStoreState>()(
  persist(
    (set) => ({
      preferences: { ...defaultPreferences },
      updatePreferences: (update) =>
        set((state) => ({ preferences: { ...state.preferences, ...update } })),
      resetPreferences: () => set({ preferences: { ...defaultPreferences } }),
    }),
    {
      name: "arip-user-pref",
    }
  )
);
