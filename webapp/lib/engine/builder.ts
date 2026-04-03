/**
 * Core prompt assembly engine.
 *
 * Combines subject, character, hook, shot preset, lens, angle,
 * and outcome scenario into a photorealism-optimized prompt.
 */

import type { PromptConfig, BuiltPrompt, ShotType } from "./types";
import { CHARACTERS } from "./characters";
import { HOOK_TEMPLATES } from "./hooks";
import { LENS_PROFILES, ANGLE_PROFILES, OUTCOME_PROFILES } from "./knowledge";
import { SHOT_PRESETS, NEGATIVE_REALISM, NEGATIVE_TECHWEAR, NEGATIVE_UGC } from "./modifiers";

export function build(config: PromptConfig): BuiltPrompt {
  const parts: string[] = [];

  // 1. Inject character prefix for visual consistency
  if (config.characterKey) {
    const char = CHARACTERS[config.characterKey];
    if (char) {
      parts.push(toSubjectPrefix(char));
    }
  }

  // 2. Inject hook prompt prefix
  if (config.hookKey) {
    const hook = HOOK_TEMPLATES[config.hookKey];
    if (hook) {
      parts.push(hook.promptPrefix);
    }
  }

  // 3. Subject
  parts.push(config.subject);

  // 4. Outcome scenario — pulls in recommended lens, angle, extra tokens
  if (config.outcomeScenario) {
    const outcome = OUTCOME_PROFILES[config.outcomeScenario];
    if (outcome) {
      parts.push(...outcome.extraTokens);
    }
  }

  // 5. Shot preset tokens
  const preset = SHOT_PRESETS[config.shotType] ?? SHOT_PRESETS["portrait"];
  parts.push(preset.camera);
  parts.push(preset.lens);
  parts.push(preset.aperture);
  parts.push(config.lightingOverride ?? preset.lighting);
  parts.push(preset.dof);
  parts.push(...preset.quality);
  parts.push(...preset.post);

  // 6. Lens override — injects detailed lens profile knowledge
  if (config.lensOverride) {
    const lens = LENS_PROFILES[config.lensOverride];
    if (lens) parts.push(lens.promptToken);
  }

  // 7. Camera angle
  if (config.cameraAngle) {
    const angle = ANGLE_PROFILES[config.cameraAngle];
    if (angle) parts.push(angle.promptToken);
  }

  // 8. Optional overrides
  if (config.atmosphereOverride) parts.push(config.atmosphereOverride);
  if (config.extraStyle) parts.push(config.extraStyle);

  const positive = parts.filter(Boolean).join(", ");
  const negative = resolveNegative(config.shotType);

  return { positive, negative, config };
}

function resolveNegative(shotType: ShotType): string {
  if (shotType.startsWith("techwear_")) return NEGATIVE_TECHWEAR;
  const ugcTypes = ["talking_head", "pov", "reaction", "lifestyle", "unboxing", "transformation"];
  if (ugcTypes.includes(shotType)) return NEGATIVE_UGC;
  return NEGATIVE_REALISM;
}

function toSubjectPrefix(char: { style: string; wardrobeTokens: string[]; ageRange: string; genderExpression: string; skinDetail: string; hairDetail?: string; extraTokens?: string[] }): string {
  const parts = [
    `${char.ageRange} ${char.genderExpression}`,
    char.style,
    ...char.wardrobeTokens.slice(0, 2),
    char.hairDetail,
    char.skinDetail,
    ...(char.extraTokens ?? []),
  ];
  return parts.filter(Boolean).join(", ");
}

/**
 * Quick outcome-aware build — provide a scenario and the engine
 * recommends the optimal shot, lens, angle, hook automatically.
 */
export function buildFromOutcome(
  subject: string,
  scenario: PromptConfig["outcomeScenario"],
  characterKey?: string,
  overrides: Partial<PromptConfig> = {},
): BuiltPrompt {
  if (!scenario) return build({ subject, shotType: "portrait", ...overrides });

  const outcome = OUTCOME_PROFILES[scenario];
  return build({
    subject,
    shotType: outcome.recommendedShot,
    hookKey: outcome.recommendedHook,
    lensOverride: outcome.recommendedLens,
    cameraAngle: outcome.recommendedAngle,
    outcomeScenario: scenario,
    characterKey,
    lightingOverride: outcome.lightingStyle,
    ...overrides,
  });
}
