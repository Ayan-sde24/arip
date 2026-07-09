import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useCommandPaletteStore } from "../store";

export function useKeyboardShortcuts() {
  const navigate = useNavigate();
  const { open: openPalette, close: closePalette, isOpen } = useCommandPaletteStore();

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      const ctrl = e.ctrlKey || e.metaKey;

      // Ctrl+K — Command Palette
      if (ctrl && e.key === "k") {
        e.preventDefault();
        isOpen ? closePalette() : openPalette();
        return;
      }

      // Ctrl+U — Upload Resume
      if (ctrl && e.key === "u") {
        e.preventDefault();
        navigate("/upload");
        return;
      }

      // Ctrl+J — Start Analysis (same as upload)
      if (ctrl && e.key === "j") {
        e.preventDefault();
        navigate("/upload");
        return;
      }

      // Ctrl+D — Dashboard
      if (ctrl && e.key === "d") {
        e.preventDefault();
        navigate("/dashboard");
        return;
      }

      // Escape — close overlays (handled by components; this is a fallback)
      if (e.key === "Escape" && isOpen) {
        closePalette();
      }
    }

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [navigate, openPalette, closePalette, isOpen]);
}
