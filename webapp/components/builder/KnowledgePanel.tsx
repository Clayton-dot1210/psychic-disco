"use client";

import { useState } from "react";
import { LENS_PROFILES, ANGLE_PROFILES, APERTURE_GUIDE, LIGHTING_KNOWLEDGE } from "@/lib/engine/knowledge";

type KnowledgeTab = "lenses" | "angles" | "aperture" | "lighting";

export function KnowledgePanel() {
  const [tab, setTab] = useState<KnowledgeTab>("lenses");

  return (
    <div className="rounded-xl border border-border bg-card overflow-hidden">
      <div className="px-5 py-3.5 border-b border-border">
        <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
          Photography Knowledge Base
        </p>
      </div>

      <div className="flex border-b border-border">
        {(["lenses", "angles", "aperture", "lighting"] as KnowledgeTab[]).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`flex-1 py-2 text-xs font-medium capitalize transition-colors ${
              tab === t
                ? "text-foreground border-b-2 border-primary"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      <div className="p-4 max-h-80 overflow-y-auto space-y-3">
        {tab === "lenses" &&
          Object.values(LENS_PROFILES).map((l) => (
            <div key={l.key} className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold">{l.label}</span>
                <span className="text-[10px] text-muted-foreground">{l.fov} FOV</span>
              </div>
              <p className="text-[11px] text-muted-foreground">{l.character}</p>
              <p className="text-[11px] text-muted-foreground">Best for: {l.bestFor.join(", ")}</p>
            </div>
          ))}

        {tab === "angles" &&
          Object.values(ANGLE_PROFILES).map((a) => (
            <div key={a.key} className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold">{a.label}</span>
              </div>
              <p className="text-[11px] text-muted-foreground">{a.description}</p>
              <p className="text-[11px] text-amber-400/80">Effect: {a.emotionalEffect}</p>
            </div>
          ))}

        {tab === "aperture" &&
          Object.entries(APERTURE_GUIDE).map(([key, a]) => (
            <div key={key} className="space-y-1">
              <span className="text-xs font-semibold">{a.label}</span>
              <p className="text-[11px] text-muted-foreground">{a.effect}</p>
              <p className="text-[11px] text-amber-400/80">Best for: {a.bestFor}</p>
            </div>
          ))}

        {tab === "lighting" &&
          Object.entries(LIGHTING_KNOWLEDGE).map(([key, l]) => (
            <div key={key} className="space-y-1">
              <span className="text-xs font-semibold">{l.label}</span>
              <p className="text-[11px] text-muted-foreground">{l.description}</p>
              <p className="text-[11px] text-amber-400/80">Mood: {l.mood}</p>
            </div>
          ))}
      </div>
    </div>
  );
}
