// ─── Core engine types ────────────────────────────────────────────────────────

export type Platform =
  | "kling_3"
  | "kling_3_omni"
  | "kling_io"
  | "seedance_2"
  | "higgsfield"
  | "runway"
  | "pika"
  | "openart";

export type ShotType =
  // Standard photography shots
  | "portrait"
  | "landscape"
  | "street"
  | "product"
  | "architecture"
  | "wildlife"
  | "cinematic"
  // UGC shots
  | "talking_head"
  | "pov"
  | "reaction"
  | "lifestyle"
  | "unboxing"
  | "transformation"
  // Character 28 / Techwear shots
  | "techwear_street"
  | "techwear_closeup"
  | "techwear_wide"
  | "techwear_neon";

export type HookType =
  | "pattern_interrupt"
  | "bold_claim"
  | "curiosity_hook"
  | "pov_hook"
  | "transformation_hook"
  | "social_proof_hook"
  | "question_hook"
  | "silent_stare"
  | "urban_reveal"
  | "neon_emergence";

export type SequenceType =
  | "ugc_standard"
  | "product_demo"
  | "story_arc"
  | "techwear_promo"
  | "techwear_hook_only";

export type CharacterKey =
  | "creator"
  | "expert"
  | "everyday"
  | "influencer"
  | "entrepreneur"
  | "character_28"
  | "character_28_shades"
  | string; // allow custom characters

export type CameraAngle =
  | "eye_level"
  | "low_angle"
  | "high_angle"
  | "dutch_angle"
  | "birds_eye"
  | "worms_eye"
  | "over_shoulder"
  | "pov"
  | "hip_level"
  | "ground_level";

export type LensType =
  | "14mm_ultra_wide"
  | "24mm_wide"
  | "35mm_standard_wide"
  | "50mm_normal"
  | "85mm_portrait"
  | "135mm_short_telephoto"
  | "200mm_telephoto";

export type OutcomeScenario =
  | "ugc_testimonial"
  | "fashion_editorial"
  | "product_reveal"
  | "hook_scroll_stop"
  | "social_proof"
  | "emotional_story"
  | "brand_identity"
  | "lifestyle_content";

// ─── Config types ─────────────────────────────────────────────────────────────

export interface PromptConfig {
  subject: string;
  shotType: ShotType;
  characterKey?: CharacterKey;
  hookKey?: HookType;
  cameraAngle?: CameraAngle;
  lensOverride?: LensType;
  lightingOverride?: string;
  atmosphereOverride?: string;
  motionOverride?: string;
  outcomeScenario?: OutcomeScenario;
  extraStyle?: string;
  referenceImageUrl?: string; // for Kling Omni image-to-video
  randomize?: boolean;
  seed?: number;
}

export interface SequenceConfig {
  concept: string;
  characterKey?: CharacterKey;
  hookKey?: HookType;
  sequenceType: SequenceType;
  platformTarget: "tiktok" | "reels" | "youtube_shorts";
  productName?: string;
  seed?: number;
}

// ─── Output types ─────────────────────────────────────────────────────────────

export interface BuiltPrompt {
  positive: string;
  negative: string;
  config: PromptConfig;
}

export interface PlatformOutput {
  platform: Platform;
  platformLabel: string;
  positive: string;
  negative: string;
  parameters: Record<string, string | number | boolean>;
  copyPaste: string;
  referenceImageRequired?: boolean; // for Kling Omni
}

export interface Shot {
  shotNumber: number;
  label: string;
  prompt: BuiltPrompt;
  durationHint: string;
  motionCue: string;
  aspectRatio: string;
  notes: string;
}

export interface VideoSequence {
  title: string;
  sequenceType: SequenceType;
  totalDuration: string;
  platformTarget: string;
  shots: Shot[];
  characterName?: string;
}

// ─── Character types ──────────────────────────────────────────────────────────

export interface Character {
  key: string;
  name: string;
  archetype: string;
  ageRange: string;
  genderExpression: string;
  style: string;
  wardrobeTokens: string[];
  environmentTokens: string[];
  expressionTokens: string[];
  skinDetail: string;
  hairDetail?: string;
  extraTokens?: string[];
}

// ─── Hook types ───────────────────────────────────────────────────────────────

export interface HookTemplate {
  key: HookType;
  name: string;
  hookType: string;
  visualSetup: string;
  cameraAction: string;
  subjectAction: string;
  emotionTone: string;
  promptPrefix: string;
  motionCue: string;
  durationHint: string;
  description: string;
}

// ─── Lens / angle knowledge types ────────────────────────────────────────────

export interface LensProfile {
  key: LensType;
  label: string;
  focalLength: string;
  fov: string;
  character: string;
  bestFor: string[];
  promptToken: string;
  apertureRange: string;
}

export interface AngleProfile {
  key: CameraAngle;
  label: string;
  description: string;
  emotionalEffect: string;
  promptToken: string;
  bestFor: string[];
}

export interface OutcomeProfile {
  key: OutcomeScenario;
  label: string;
  description: string;
  recommendedShot: ShotType;
  recommendedHook?: HookType;
  recommendedLens: LensType;
  recommendedAngle: CameraAngle;
  lightingStyle: string;
  motionStyle: string;
  extraTokens: string[];
}
