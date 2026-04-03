"use client";

import { useState } from "react";
import { useBuilderStore } from "@/lib/store/builder";
import { PLATFORM_META } from "@/lib/engine/platforms";
import type { PlatformOutput } from "@/lib/engine/types";

export function PlatformOutputs() {
  const outputs = useBuilderStore((s) => s.outputs);

  if (outputs.length === 0) return null;

  return (
    <div className="space-y-4">
      <h3 className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
        Generated Prompts — {outputs.length} platform{outputs.length > 1 ? "s" : ""}
      </h3>
      {outputs.map((output) => (
        <PlatformCard key={output.platform} output={output} />
      ))}
    </div>
  );
}

function PlatformCard({ output }: { output: PlatformOutput }) {
  const [tab, setTab] = useState<"positive" | "negative" | "settings" | "copy">("positive");
  const meta = PLATFORM_META[output.platform];

  return (
    <div className="rounded-xl border border-border bg-card overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-border">
        <div className="flex items-center gap-2.5">
          <span className="text-lg">{meta.emoji}</span>
          <div>
            <p className="text-sm font-semibold">{meta.label}</p>
            <p className="text-[11px] text-muted-foreground">{meta.description}</p>
          </div>
        </div>
        {output.referenceImageRequired && (
          <span className="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded px-2 py-1 font-medium">
            Reference image required
          </span>
        )}
      </div>

      {/* Tabs */}
      <div className="flex border-b border-border">
        {(["positive", "negative", "settings", "copy"] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`flex-1 py-2 text-xs font-medium capitalize transition-colors ${
              tab === t
                ? "text-foreground border-b-2 border-primary"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            {t === "copy" ? "Copy-Paste" : t}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="p-5">
        {tab === "positive" && (
          <CopyableText label="Positive Prompt" text={output.positive} />
        )}
        {tab === "negative" && (
          <CopyableText label="Negative Prompt" text={output.negative} />
        )}
        {tab === "settings" && (
          <div className="space-y-1.5">
            {Object.entries(output.parameters).map(([k, v]) => (
              <div key={k} className="flex items-start gap-4">
                <span className="text-[11px] text-muted-foreground font-mono w-32 shrink-0">{k}</span>
                <span className="text-[11px] text-foreground">{String(v)}</span>
              </div>
            ))}
          </div>
        )}
        {tab === "copy" && (
          <CopyableText label="Copy-Paste Ready" text={output.copyPaste} mono />
        )}
      </div>
    </div>
  );
}

function CopyableText({
  label,
  text,
  mono = false,
}: {
  label: string;
  text: string;
  mono?: boolean;
}) {
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-[10px] text-muted-foreground uppercase tracking-widest">{label}</span>
        <button
          onClick={copy}
          className="text-[11px] text-muted-foreground hover:text-foreground transition-colors px-2 py-1 rounded border border-border hover:border-ring"
        >
          {copied ? "Copied!" : "Copy"}
        </button>
      </div>
      <pre
        className={`text-xs leading-relaxed text-foreground/90 whitespace-pre-wrap bg-background rounded-lg p-3 border border-border ${
          mono ? "font-mono" : "font-sans"
        }`}
      >
        {text}
      </pre>
    </div>
  );
}
