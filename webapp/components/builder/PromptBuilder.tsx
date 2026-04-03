"use client";

import { useBuilderStore } from "@/lib/store/builder";
import { CHARACTERS } from "@/lib/engine/characters";
import { HOOK_TEMPLATES } from "@/lib/engine/hooks";
import { OUTCOME_PROFILES, LENS_PROFILES, ANGLE_PROFILES } from "@/lib/engine/knowledge";
import { SHOT_PRESETS } from "@/lib/engine/modifiers";
import { PLATFORM_META } from "@/lib/engine/platforms";
import type { Platform, ShotType, HookType, OutcomeScenario, CameraAngle, LensType } from "@/lib/engine/types";

const PLATFORMS = Object.keys(PLATFORM_META) as Platform[];

export function PromptBuilder() {
  const store = useBuilderStore();

  const toggle = (platform: Platform) => {
    store.set({
      selectedPlatforms: store.selectedPlatforms.includes(platform)
        ? store.selectedPlatforms.filter((p) => p !== platform)
        : [...store.selectedPlatforms, platform],
    });
  };

  return (
    <div className="space-y-6">
      {/* Subject */}
      <section className="space-y-2">
        <label className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
          Subject / Concept
        </label>
        <textarea
          value={store.subject}
          onChange={(e) => store.set({ subject: e.target.value })}
          placeholder='e.g. "standing in the rain on empty cobblestone street" or "why I switched to techwear"'
          rows={3}
          className="w-full rounded-lg bg-card border border-border px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring resize-none"
        />
      </section>

      {/* Outcome scenario — smart mode */}
      <section className="space-y-2">
        <label className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
          Outcome Scenario
          <span className="ml-2 text-[10px] font-normal text-muted-foreground normal-case">
            (auto-selects best shot, lens, angle, hook)
          </span>
        </label>
        <select
          value={store.outcomeScenario}
          onChange={(e) => store.set({ outcomeScenario: e.target.value as OutcomeScenario | "" })}
          className="w-full rounded-lg bg-card border border-border px-4 py-2.5 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
        >
          <option value="">— Manual mode —</option>
          {Object.values(OUTCOME_PROFILES).map((o) => (
            <option key={o.key} value={o.key}>
              {o.label} — {o.description}
            </option>
          ))}
        </select>
      </section>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Character */}
        <section className="space-y-2">
          <label className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">Character</label>
          <select
            value={store.characterKey}
            onChange={(e) => store.set({ characterKey: e.target.value as any })}
            className="w-full rounded-lg bg-card border border-border px-4 py-2.5 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
          >
            <option value="">— No character —</option>
            {Object.values(CHARACTERS).map((c) => (
              <option key={c.key} value={c.key}>
                {c.name}
              </option>
            ))}
          </select>
        </section>

        {/* Hook */}
        <section className="space-y-2">
          <label className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">Visual Hook</label>
          <select
            value={store.hookKey}
            onChange={(e) => store.set({ hookKey: e.target.value as HookType | "" })}
            className="w-full rounded-lg bg-card border border-border px-4 py-2.5 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
          >
            <option value="">— No hook —</option>
            {Object.values(HOOK_TEMPLATES).map((h) => (
              <option key={h.key} value={h.key}>
                {h.name} — {h.durationHint}
              </option>
            ))}
          </select>
        </section>

        {/* Shot type */}
        <section className="space-y-2">
          <label className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">Shot Type</label>
          <select
            value={store.shotType}
            onChange={(e) => store.set({ shotType: e.target.value as ShotType })}
            className="w-full rounded-lg bg-card border border-border px-4 py-2.5 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
          >
            {Object.entries(SHOT_PRESETS).map(([key, preset]) => (
              <option key={key} value={key}>
                {preset.description ?? key.replace(/_/g, " ")}
              </option>
            ))}
          </select>
        </section>

        {/* Camera angle */}
        <section className="space-y-2">
          <label className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">Camera Angle</label>
          <select
            value={store.cameraAngle}
            onChange={(e) => store.set({ cameraAngle: e.target.value as CameraAngle | "" })}
            className="w-full rounded-lg bg-card border border-border px-4 py-2.5 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
          >
            <option value="">— Preset default —</option>
            {Object.values(ANGLE_PROFILES).map((a) => (
              <option key={a.key} value={a.key}>
                {a.label} — {a.emotionalEffect}
              </option>
            ))}
          </select>
        </section>

        {/* Lens */}
        <section className="space-y-2">
          <label className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">Lens Override</label>
          <select
            value={store.lensOverride}
            onChange={(e) => store.set({ lensOverride: e.target.value as LensType | "" })}
            className="w-full rounded-lg bg-card border border-border px-4 py-2.5 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
          >
            <option value="">— Shot preset lens —</option>
            {Object.values(LENS_PROFILES).map((l) => (
              <option key={l.key} value={l.key}>
                {l.label} — {l.character}
              </option>
            ))}
          </select>
        </section>

        {/* Duration */}
        <section className="space-y-2">
          <label className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">Duration</label>
          <div className="flex gap-2">
            {([5, 10] as const).map((d) => (
              <button
                key={d}
                onClick={() => store.set({ durationSeconds: d })}
                className={`flex-1 rounded-lg border px-4 py-2.5 text-sm font-medium transition-colors ${
                  store.durationSeconds === d
                    ? "bg-primary text-primary-foreground border-primary"
                    : "bg-card border-border text-muted-foreground hover:text-foreground"
                }`}
              >
                {d}s {d === 10 ? "(Pro)" : "(Standard)"}
              </button>
            ))}
          </div>
        </section>
      </div>

      {/* Advanced overrides */}
      <details className="group">
        <summary className="cursor-pointer text-xs font-semibold uppercase tracking-widest text-muted-foreground hover:text-foreground transition-colors list-none flex items-center gap-2">
          <span className="group-open:rotate-90 transition-transform inline-block">›</span>
          Advanced Overrides
        </summary>
        <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Lighting override..."
            value={store.lightingOverride}
            onChange={(e) => store.set({ lightingOverride: e.target.value })}
            className="rounded-lg bg-card border border-border px-4 py-2.5 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring"
          />
          <input
            type="text"
            placeholder="Camera motion override..."
            value={store.motionOverride}
            onChange={(e) => store.set({ motionOverride: e.target.value })}
            className="rounded-lg bg-card border border-border px-4 py-2.5 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring"
          />
          <input
            type="text"
            placeholder="Style rider (extra tokens)..."
            value={store.extraStyle}
            onChange={(e) => store.set({ extraStyle: e.target.value })}
            className="rounded-lg bg-card border border-border px-4 py-2.5 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring"
          />
          <input
            type="text"
            placeholder="Reference image URL (Kling Omni)..."
            value={store.referenceImageUrl}
            onChange={(e) => store.set({ referenceImageUrl: e.target.value })}
            className="rounded-lg bg-card border border-border px-4 py-2.5 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>
      </details>

      {/* Platform selector */}
      <section className="space-y-2">
        <label className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">Output Platforms</label>
        <div className="flex flex-wrap gap-2">
          {PLATFORMS.map((p) => {
            const meta = PLATFORM_META[p];
            const selected = store.selectedPlatforms.includes(p);
            return (
              <button
                key={p}
                onClick={() => toggle(p)}
                className={`flex items-center gap-1.5 rounded-lg border px-3 py-2 text-xs font-medium transition-colors ${
                  selected
                    ? "bg-primary text-primary-foreground border-primary"
                    : "bg-card border-border text-muted-foreground hover:text-foreground"
                }`}
              >
                <span>{meta.emoji}</span>
                {meta.label}
              </button>
            );
          })}
        </div>
      </section>

      {/* Error */}
      {store.error && (
        <p className="text-sm text-red-400 bg-red-400/10 rounded-lg px-4 py-3">{store.error}</p>
      )}

      {/* Generate button */}
      <button
        onClick={store.generate}
        disabled={store.isGenerating || !store.subject.trim()}
        className="w-full rounded-lg bg-primary text-primary-foreground px-6 py-3.5 text-sm font-semibold tracking-wide hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {store.isGenerating ? "Generating..." : "Generate Prompts →"}
      </button>
    </div>
  );
}
