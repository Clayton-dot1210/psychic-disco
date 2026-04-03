/**
 * Platform-specific prompt formatters.
 *
 * Kling 3.0         — Latest Kling, best motion quality, 5s standard / 10s pro
 * Kling 3.0 Omni    — Image-to-video, accepts reference image for character consistency
 * Kling IO          — API-based Kling access, same models via endpoint
 * Seedance 2.0      — ByteDance model, narrative prompts, strong human motion
 * Higgsfield        — Cinematic video, motion cues in prompt
 * Runway Gen-3      — Subject/style/motion separation
 * Pika              — Short-form, motion strength 1-4
 * OpenArt           — Stable Diffusion image generation
 */

import type { BuiltPrompt, PlatformOutput, Platform, ShotType } from "./types";

// ─── Kling 3.0 ────────────────────────────────────────────────────────────────

const KLING3_CAMERA_CONTROLS: Record<string, { type: string; speed: number }> = {
  portrait:          { type: "push_in",         speed: 2 },
  street:            { type: "handheld",         speed: 3 },
  cinematic:         { type: "dolly_zoom",       speed: 2 },
  talking_head:      { type: "push_in",          speed: 2 },
  reaction:          { type: "push_in",          speed: 3 },
  lifestyle:         { type: "tracking_follow",  speed: 2 },
  unboxing:          { type: "push_in",          speed: 2 },
  transformation:    { type: "crane_up",         speed: 2 },
  techwear_street:   { type: "push_in",          speed: 1 },
  techwear_closeup:  { type: "push_in",          speed: 1 },
  techwear_wide:     { type: "crane_up",         speed: 2 },
  techwear_neon:     { type: "push_in",          speed: 2 },
  landscape:         { type: "pan_right",        speed: 2 },
  product:           { type: "orbit",            speed: 2 },
  architecture:      { type: "tilt_up",          speed: 2 },
  wildlife:          { type: "tracking_follow",  speed: 3 },
  pov:               { type: "handheld",         speed: 2 },
};

const KLING3_ASPECT: Record<string, string> = {
  portrait: "9:16", street: "9:16", talking_head: "9:16",
  reaction: "9:16", lifestyle: "9:16", unboxing: "9:16",
  transformation: "9:16", pov: "9:16",
  techwear_street: "9:16", techwear_closeup: "9:16",
  techwear_wide: "9:16", techwear_neon: "9:16",
  landscape: "16:9", architecture: "16:9", wildlife: "16:9",
  product: "1:1", cinematic: "21:9",
};

export function formatKling3(
  prompt: BuiltPrompt,
  motionOverride?: string,
  durationSeconds: 5 | 10 = 5,
): PlatformOutput {
  const shot = prompt.config.shotType;
  const ctrl = KLING3_CAMERA_CONTROLS[shot] ?? { type: "push_in", speed: 2 };
  const aspect = KLING3_ASPECT[shot] ?? "9:16";
  const mode = durationSeconds === 10 ? "pro" : "standard";

  // Kling 3.0 responds well to quality anchors + motion description
  const positive = [
    "Photorealistic, hyper-realistic cinematic video, 8K quality, film grain.",
    prompt.positive,
    motionOverride
      ? `Camera: ${motionOverride}.`
      : `Camera: ${ctrl.type.replace(/_/g, " ")}, speed ${ctrl.speed}/5.`,
    "No artifacts, no distortion, true-to-life skin texture, natural movement.",
  ].join(" ");

  const parameters = {
    mode,
    duration: `${durationSeconds}s`,
    camera_type: ctrl.type,
    camera_speed: ctrl.speed,
    aspect_ratio: aspect,
    cfg_scale: 0.5,
    quality: "high",
  };

  return {
    platform: "kling_3",
    platformLabel: "Kling 3.0",
    positive,
    negative: prompt.negative,
    parameters,
    copyPaste: buildCopyPaste("Kling 3.0", positive, prompt.negative, parameters),
  };
}

// ─── Kling 3.0 Omni (image-to-video) ─────────────────────────────────────────

export function formatKling3Omni(
  prompt: BuiltPrompt,
  referenceImageUrl?: string,
  motionOverride?: string,
  durationSeconds: 5 | 10 = 5,
): PlatformOutput {
  const shot = prompt.config.shotType;
  const ctrl = KLING3_CAMERA_CONTROLS[shot] ?? { type: "push_in", speed: 1 };
  const aspect = KLING3_ASPECT[shot] ?? "9:16";

  // Omni accepts a reference image for character consistency — this is the killer feature
  // for Character 28: paste his actual photo as the reference image
  const positive = [
    "Animate this reference image to life, photorealistic video, preserve exact likeness.",
    prompt.positive,
    motionOverride
      ? `Camera: ${motionOverride}.`
      : `Camera: ${ctrl.type.replace(/_/g, " ")}, slow and deliberate.`,
    "Maintain 100% character consistency with reference, natural facial animation, micro-expressions.",
    "No identity drift, no likeness shift.",
  ].join(" ");

  const parameters = {
    mode: durationSeconds === 10 ? "pro" : "standard",
    duration: `${durationSeconds}s`,
    camera_type: ctrl.type,
    camera_speed: ctrl.speed,
    aspect_ratio: aspect,
    reference_image: referenceImageUrl ?? "UPLOAD_CHARACTER_REFERENCE_IMAGE",
    character_fidelity: "high",
  };

  return {
    platform: "kling_3_omni",
    platformLabel: "Kling 3.0 Omni (Img→Video)",
    positive,
    negative: prompt.negative,
    parameters,
    copyPaste: buildCopyPaste("Kling 3.0 Omni", positive, prompt.negative, parameters),
    referenceImageRequired: true,
  };
}

// ─── Kling IO (API) ───────────────────────────────────────────────────────────

export function formatKlingIO(
  prompt: BuiltPrompt,
  motionOverride?: string,
  durationSeconds: 5 | 10 = 5,
): PlatformOutput {
  const shot = prompt.config.shotType;
  const ctrl = KLING3_CAMERA_CONTROLS[shot] ?? { type: "push_in", speed: 2 };
  const aspect = KLING3_ASPECT[shot] ?? "9:16";

  const positive = [
    "Photorealistic cinematic video.",
    prompt.positive,
    motionOverride ?? `Camera movement: ${ctrl.type.replace(/_/g, " ")}.`,
    "Ultra-realistic, film quality, natural motion.",
  ].join(" ");

  const parameters = {
    model: "kling-v3",
    mode: durationSeconds === 10 ? "pro" : "std",
    duration: durationSeconds,
    aspect_ratio: aspect,
    camera_control: { type: ctrl.type, config: { speed: ctrl.speed } },
    cfg_scale: 0.5,
  };

  return {
    platform: "kling_io",
    platformLabel: "Kling IO (API)",
    positive,
    negative: prompt.negative,
    parameters: flattenForDisplay(parameters),
    copyPaste: [
      "// Kling IO API payload",
      JSON.stringify(
        {
          prompt: positive,
          negative_prompt: prompt.negative,
          ...parameters,
        },
        null,
        2,
      ),
    ].join("\n"),
  };
}

// ─── Seedance 2.0 ─────────────────────────────────────────────────────────────

// Seedance responds to natural-language narrative prompts, not token chains
const SEEDANCE_MOTION: Record<string, string> = {
  portrait:         "camera slowly and smoothly approaches the subject",
  talking_head:     "camera very gently drifts closer, subtle handheld warmth",
  techwear_street:  "camera slowly and deliberately pushes in toward the subject, rain-slicked reflections shimmering",
  techwear_closeup: "camera imperceptibly creeps closer, razor focus on face",
  techwear_wide:    "camera rises slowly from ground level to reveal the full figure",
  techwear_neon:    "camera drifts through steam and neon light toward the subject",
  lifestyle:        "camera gently follows the subject through their environment",
  unboxing:         "camera slowly reveals the product with a smooth push-in",
  reaction:         "camera stays intimate, slight handheld energy",
  transformation:   "camera dramatically cranes upward to reveal the result",
  landscape:        "camera slowly pans from left to right across the landscape",
  street:           "camera moves through the street with subtle handheld realism",
  cinematic:        "camera glides with a cinematic dolly movement",
};

export function formatSeedance2(
  prompt: BuiltPrompt,
  motionOverride?: string,
): PlatformOutput {
  const shot = prompt.config.shotType;
  const motion = motionOverride ?? SEEDANCE_MOTION[shot] ?? "camera slowly approaches";
  const aspect = KLING3_ASPECT[shot] ?? "9:16";

  // Seedance wants narrative sentences, not comma-separated token chains
  const subjectNarrative = convertTokensToNarrative(prompt.positive);

  const positive = [
    `A photorealistic, cinematic short video clip where ${subjectNarrative}.`,
    `The ${motion}.`,
    "The footage has the quality of a high-end commercial production — perfectly exposed,",
    "natural skin texture, realistic fabric detail, authentic atmospheric depth.",
    "The motion is smooth and purposeful. No shaking, no artifacts.",
  ].join(" ");

  const parameters = {
    aspect_ratio: aspect,
    resolution: "1080p",
    fps: 24,
    style: "photorealistic",
    duration: "5-8s",
  };

  return {
    platform: "seedance_2",
    platformLabel: "Seedance 2.0",
    positive,
    negative: prompt.negative,
    parameters,
    copyPaste: buildCopyPaste("Seedance 2.0", positive, prompt.negative, parameters),
  };
}

// Converts token-chain prompts into more readable narrative for Seedance
function convertTokensToNarrative(tokenChain: string): string {
  // Seedance works best with slightly more readable language
  // but still benefits from the key descriptive tokens
  const cleaned = tokenChain
    .replace(/shot on /gi, "")
    .replace(/f\/[\d.]+/g, "")
    .replace(/ISO \d+/g, "")
    .replace(/\s+/g, " ")
    .trim();
  return cleaned.length > 200 ? cleaned.substring(0, 200) + "..." : cleaned;
}

// ─── Higgsfield ───────────────────────────────────────────────────────────────

const HIGGSFIELD_MOTION: Record<string, string> = {
  portrait: "slow push-in, subtle camera drift",
  landscape: "slow pan right, parallax depth",
  street: "handheld slight shake, tracking shot",
  product: "gentle orbit, slow rotation",
  talking_head: "slow subtle push-in",
  techwear_street: "slow deliberate push-in, wet reflection shimmer",
  techwear_closeup: "ultra-slow push-in, imperceptible",
  techwear_wide: "slow crane up, full reveal",
  techwear_neon: "slow atmospheric push-in, steam drift",
  cinematic: "dolly zoom, slow push-in",
};

export function formatHighgsfield(
  prompt: BuiltPrompt,
  motionOverride?: string,
  durationSeconds = 5,
): PlatformOutput {
  const shot = prompt.config.shotType;
  const motion = motionOverride ?? HIGGSFIELD_MOTION[shot] ?? "slow push-in";
  const aspect = KLING3_ASPECT[shot] ?? "9:16";

  const positive = [
    `Cinematic ${durationSeconds}-second video clip. Camera: ${motion}.`,
    prompt.positive,
    "cinematic motion, smooth movement",
  ].join(" ");

  const parameters = {
    aspect_ratio: aspect,
    duration: `${durationSeconds}s`,
    camera_motion: motion,
    style: "photorealistic",
    motion_amount: "subtle",
  };

  return {
    platform: "higgsfield",
    platformLabel: "Higgsfield",
    positive,
    negative: prompt.negative,
    parameters,
    copyPaste: buildCopyPaste("Higgsfield", positive, prompt.negative, parameters),
  };
}

// ─── Runway Gen-3 ─────────────────────────────────────────────────────────────

export function formatRunway(
  prompt: BuiltPrompt,
  motionOverride?: string,
  durationSeconds = 5,
): PlatformOutput {
  const shot = prompt.config.shotType;
  const aspect = KLING3_ASPECT[shot] ?? "9:16";
  const motion = motionOverride ?? "camera slowly pushes in, photorealistic, no shake";

  const positive = [
    `${motion}.`,
    prompt.positive,
    "Photorealistic, cinematic quality, natural motion, no artifacts.",
  ].join(" ");

  const parameters = {
    aspect_ratio: aspect,
    duration: `${durationSeconds}s`,
    style_preset: "photorealistic",
    seed: prompt.config.seed ?? "random",
  };

  return {
    platform: "runway",
    platformLabel: "Runway Gen-3",
    positive,
    negative: prompt.negative,
    parameters,
    copyPaste: buildCopyPaste("Runway Gen-3", positive, prompt.negative, parameters),
  };
}

// ─── Pika Labs ────────────────────────────────────────────────────────────────

export function formatPika(
  prompt: BuiltPrompt,
  motionStrength: 1 | 2 | 3 | 4 = 1,
): PlatformOutput {
  const shot = prompt.config.shotType;
  const aspect = KLING3_ASPECT[shot] ?? "9:16";

  const positive = `${prompt.positive}, photorealistic, high quality, cinematic`;

  const parameters = {
    camera_motion: "zoom in",
    motion_strength: motionStrength,
    aspect_ratio: aspect,
    fps: 24,
    quality: "1080p",
  };

  return {
    platform: "pika",
    platformLabel: "Pika Labs",
    positive,
    negative: prompt.negative,
    parameters,
    copyPaste: buildCopyPaste("Pika", positive, prompt.negative, parameters),
  };
}

// ─── OpenArt (image generation) ───────────────────────────────────────────────

const OPENART_MODELS: Record<string, { model: string; cfg: number; steps: number; sampler: string }> = {
  portrait:        { model: "Realistic Vision V6.0 B1", cfg: 7, steps: 30, sampler: "DPM++ 2M Karras" },
  talking_head:    { model: "Realistic Vision V6.0 B1", cfg: 7, steps: 30, sampler: "DPM++ 2M Karras" },
  techwear_street: { model: "CinematicKX",              cfg: 8, steps: 35, sampler: "DPM++ 2M Karras" },
  techwear_closeup:{ model: "Juggernaut XL v9",         cfg: 7, steps: 40, sampler: "DPM++ 2M Karras" },
  techwear_wide:   { model: "CinematicKX",              cfg: 8, steps: 35, sampler: "DPM++ 2M Karras" },
  techwear_neon:   { model: "CinematicKX",              cfg: 8, steps: 35, sampler: "DPM++ 2M Karras" },
  cinematic:       { model: "CinematicKX",              cfg: 8, steps: 35, sampler: "DPM++ 2M Karras" },
  product:         { model: "SDXL 1.0 base",            cfg: 7, steps: 40, sampler: "DPM++ 2S a Karras" },
};

const OPENART_RESOLUTION: Record<string, [number, number]> = {
  portrait: [832, 1216], talking_head: [832, 1216],
  techwear_street: [832, 1216], techwear_closeup: [832, 1216],
  techwear_wide: [832, 1216], techwear_neon: [832, 1216],
  landscape: [1216, 832], product: [1024, 1024], cinematic: [1280, 720],
};

export function formatOpenArt(prompt: BuiltPrompt): PlatformOutput {
  const shot = prompt.config.shotType;
  const hint = OPENART_MODELS[shot] ?? OPENART_MODELS["portrait"];
  const [w, h] = OPENART_RESOLUTION[shot] ?? [832, 1216];

  const anchor = "masterpiece, best quality, ultra-realistic, (photorealistic:1.4)";
  const positive = `${anchor}, ${prompt.positive}`;

  const parameters = {
    recommended_model: hint.model,
    cfg_scale: hint.cfg,
    sampling_steps: hint.steps,
    sampler: hint.sampler,
    width: w,
    height: h,
    hires_fix: true,
    hires_denoising: 0.45,
    hires_upscale: 2.0,
    clip_skip: 2,
  };

  return {
    platform: "openart",
    platformLabel: "OpenArt",
    positive,
    negative: prompt.negative,
    parameters: flattenForDisplay(parameters),
    copyPaste: buildCopyPaste("OpenArt", positive, prompt.negative, parameters),
  };
}

// ─── Multi-platform formatter ─────────────────────────────────────────────────

export function formatForPlatforms(
  prompt: BuiltPrompt,
  platforms: Platform[],
  options: {
    motionOverride?: string;
    durationSeconds?: 5 | 10;
    referenceImageUrl?: string;
    pikaMotionStrength?: 1 | 2 | 3 | 4;
  } = {},
): PlatformOutput[] {
  const { motionOverride, durationSeconds = 5, referenceImageUrl, pikaMotionStrength = 1 } = options;
  const results: PlatformOutput[] = [];

  for (const p of platforms) {
    switch (p) {
      case "kling_3":      results.push(formatKling3(prompt, motionOverride, durationSeconds)); break;
      case "kling_3_omni": results.push(formatKling3Omni(prompt, referenceImageUrl, motionOverride, durationSeconds)); break;
      case "kling_io":     results.push(formatKlingIO(prompt, motionOverride, durationSeconds)); break;
      case "seedance_2":   results.push(formatSeedance2(prompt, motionOverride)); break;
      case "higgsfield":   results.push(formatHighgsfield(prompt, motionOverride, durationSeconds)); break;
      case "runway":       results.push(formatRunway(prompt, motionOverride, durationSeconds)); break;
      case "pika":         results.push(formatPika(prompt, pikaMotionStrength)); break;
      case "openart":      results.push(formatOpenArt(prompt)); break;
    }
  }

  return results;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function buildCopyPaste(
  platformName: string,
  positive: string,
  negative: string,
  parameters: Record<string, unknown>,
): string {
  const settingsLines = Object.entries(parameters)
    .map(([k, v]) => `  ${k}: ${JSON.stringify(v)}`)
    .join("\n");
  return `[${platformName} — POSITIVE]\n${positive}\n\n[NEGATIVE]\n${negative}\n\n[SETTINGS]\n${settingsLines}`;
}

function flattenForDisplay(obj: Record<string, unknown>): Record<string, string | number | boolean> {
  const out: Record<string, string | number | boolean> = {};
  for (const [k, v] of Object.entries(obj)) {
    if (typeof v === "object" && v !== null) {
      out[k] = JSON.stringify(v);
    } else {
      out[k] = v as string | number | boolean;
    }
  }
  return out;
}

export const PLATFORM_META: Record<Platform, { label: string; emoji: string; description: string; isVideo: boolean }> = {
  kling_3:      { label: "Kling 3.0",            emoji: "🎬", description: "Best motion quality, 5s or 10s pro mode", isVideo: true },
  kling_3_omni: { label: "Kling 3.0 Omni",       emoji: "📸→🎬", description: "Image-to-video, perfect character consistency with reference photo", isVideo: true },
  kling_io:     { label: "Kling IO (API)",        emoji: "⚡", description: "API access to Kling 3.0 for bulk generation", isVideo: true },
  seedance_2:   { label: "Seedance 2.0",          emoji: "🌱", description: "ByteDance model, strong human motion and expression", isVideo: true },
  higgsfield:   { label: "Higgsfield",            emoji: "🎥", description: "Cinematic video generation, motion cues in prompt", isVideo: true },
  runway:       { label: "Runway Gen-3",          emoji: "🚀", description: "Subject/style/motion separation, reliable realism", isVideo: true },
  pika:         { label: "Pika Labs",             emoji: "⚡", description: "Fast short-form video, motion strength control", isVideo: true },
  openart:      { label: "OpenArt",               emoji: "🖼️", description: "Stable Diffusion image generation, reference frames", isVideo: false },
};
