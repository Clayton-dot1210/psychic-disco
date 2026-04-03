/**
 * Zustand store for the prompt builder UI state.
 */
import { create } from "zustand";
import type {
  ShotType, HookType, CharacterKey, CameraAngle,
  LensType, OutcomeScenario, Platform, PlatformOutput,
} from "@/lib/engine/types";

export interface BuilderState {
  // Inputs
  subject: string;
  shotType: ShotType;
  characterKey: CharacterKey | "";
  hookKey: HookType | "";
  outcomeScenario: OutcomeScenario | "";
  cameraAngle: CameraAngle | "";
  lensOverride: LensType | "";
  lightingOverride: string;
  motionOverride: string;
  extraStyle: string;
  referenceImageUrl: string;
  selectedPlatforms: Platform[];
  durationSeconds: 5 | 10;

  // Outputs
  outputs: PlatformOutput[];
  isGenerating: boolean;
  error: string | null;

  // Actions
  set: (partial: Partial<BuilderState>) => void;
  generate: () => Promise<void>;
  reset: () => void;
}

const DEFAULT_PLATFORMS: Platform[] = ["kling_3", "kling_3_omni", "seedance_2", "higgsfield"];

export const useBuilderStore = create<BuilderState>((set, get) => ({
  subject: "",
  shotType: "techwear_street",
  characterKey: "character_28",
  hookKey: "",
  outcomeScenario: "",
  cameraAngle: "",
  lensOverride: "",
  lightingOverride: "",
  motionOverride: "",
  extraStyle: "",
  referenceImageUrl: "",
  selectedPlatforms: DEFAULT_PLATFORMS,
  durationSeconds: 5,
  outputs: [],
  isGenerating: false,
  error: null,

  set: (partial) => set(partial),

  generate: async () => {
    const state = get();
    if (!state.subject.trim()) {
      set({ error: "Enter a subject to generate prompts." });
      return;
    }

    set({ isGenerating: true, error: null, outputs: [] });

    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          subject: state.subject,
          shotType: state.shotType,
          characterKey: state.characterKey || undefined,
          hookKey: state.hookKey || undefined,
          outcomeScenario: state.outcomeScenario || undefined,
          cameraAngle: state.cameraAngle || undefined,
          lensOverride: state.lensOverride || undefined,
          lightingOverride: state.lightingOverride || undefined,
          motionOverride: state.motionOverride || undefined,
          extraStyle: state.extraStyle || undefined,
          referenceImageUrl: state.referenceImageUrl || undefined,
          platforms: state.selectedPlatforms,
          durationSeconds: state.durationSeconds,
        }),
      });

      if (!res.ok) {
        const { error } = await res.json();
        throw new Error(error ?? "Generation failed");
      }

      const { outputs } = await res.json();
      set({ outputs, isGenerating: false });
    } catch (err) {
      set({
        error: err instanceof Error ? err.message : "Unknown error",
        isGenerating: false,
      });
    }
  },

  reset: () =>
    set({
      outputs: [],
      error: null,
      subject: "",
    }),
}));
