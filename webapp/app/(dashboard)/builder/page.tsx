import { PromptBuilder } from "@/components/builder/PromptBuilder";
import { PlatformOutputs } from "@/components/builder/PlatformOutput";
import { KnowledgePanel } from "@/components/builder/KnowledgePanel";

export default function BuilderPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Top bar */}
      <header className="border-b border-border px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-7 h-7 rounded-md bg-primary flex items-center justify-center">
            <span className="text-primary-foreground text-xs font-bold">RE</span>
          </div>
          <span className="font-semibold text-sm tracking-tight">Reel Engine</span>
          <span className="text-muted-foreground text-xs border border-border rounded px-1.5 py-0.5">
            Builder
          </span>
        </div>
        <nav className="flex items-center gap-6 text-xs text-muted-foreground">
          <a href="/builder" className="text-foreground font-medium">Builder</a>
          <a href="/characters" className="hover:text-foreground transition-colors">Characters</a>
          <a href="/sequences" className="hover:text-foreground transition-colors">Sequences</a>
          <a href="/library" className="hover:text-foreground transition-colors">Library</a>
        </nav>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold tracking-tight">Prompt Builder</h1>
          <p className="text-muted-foreground text-sm mt-1">
            Generate highest-quality AI video prompts for Kling 3.0, Kling Omni, Seedance 2.0 and more.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left: Builder form */}
          <div className="lg:col-span-2 space-y-6">
            <div className="rounded-xl border border-border bg-card p-6">
              <PromptBuilder />
            </div>
            <PlatformOutputs />
          </div>

          {/* Right: Knowledge panel + quick tips */}
          <div className="space-y-6">
            <KnowledgePanel />

            {/* Quick shot reference */}
            <div className="rounded-xl border border-border bg-card p-5 space-y-4">
              <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">
                Character 28 Quick Shots
              </p>
              {[
                { label: "Signature Street", shot: "techwear_street", hook: "silent_stare" },
                { label: "Intense Close-Up", shot: "techwear_closeup", hook: "bold_claim" },
                { label: "Cinematic Wide", shot: "techwear_wide", hook: "urban_reveal" },
                { label: "Neon Atmosphere", shot: "techwear_neon", hook: "neon_emergence" },
              ].map((q) => (
                <QuickShot key={q.shot} {...q} />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function QuickShot({
  label,
  shot,
  hook,
}: {
  label: string;
  shot: string;
  hook: string;
}) {
  // These are server-rendered links that pre-fill the builder
  return (
    <a
      href={`/builder?shot=${shot}&hook=${hook}&character=character_28`}
      className="block rounded-lg border border-border px-4 py-3 text-xs hover:border-ring hover:bg-accent/30 transition-colors cursor-pointer"
    >
      <p className="font-medium text-foreground">{label}</p>
      <p className="text-muted-foreground mt-0.5">
        {shot.replace(/_/g, " ")} · {hook.replace(/_/g, " ")}
      </p>
    </a>
  );
}
