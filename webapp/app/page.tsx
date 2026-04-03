import Link from "next/link";
import { PLATFORM_META } from "@/lib/engine/platforms";

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      {/* Nav */}
      <nav className="border-b border-border px-6 py-4 flex items-center justify-between max-w-7xl mx-auto">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-md bg-primary flex items-center justify-center">
            <span className="text-primary-foreground text-xs font-bold">RE</span>
          </div>
          <span className="font-semibold text-sm tracking-tight">Reel Engine</span>
        </div>
        <div className="flex items-center gap-4">
          <Link
            href="/builder"
            className="text-xs bg-primary text-primary-foreground rounded-lg px-4 py-2 font-semibold hover:bg-primary/90 transition-colors"
          >
            Open Builder →
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-4xl mx-auto px-6 pt-24 pb-16 text-center">
        <div className="inline-flex items-center gap-2 rounded-full border border-border px-3 py-1.5 text-[11px] text-muted-foreground mb-8">
          <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
          Kling 3.0 · Kling Omni · Seedance 2.0 · Higgsfield · Runway
        </div>
        <h1 className="text-5xl font-bold tracking-tight leading-tight mb-6">
          The AI Video
          <br />
          Prompt Studio
        </h1>
        <p className="text-muted-foreground text-lg leading-relaxed max-w-2xl mx-auto mb-10">
          Generate highest-quality prompts for AI realistic videos. Built for UGC creators,
          visual hooks, and AI content characters. Every lens, angle, and lighting scenario
          encoded for maximum output quality.
        </p>
        <div className="flex items-center justify-center gap-4">
          <Link
            href="/builder"
            className="bg-primary text-primary-foreground rounded-xl px-8 py-3.5 text-sm font-semibold hover:bg-primary/90 transition-colors"
          >
            Start Building Free →
          </Link>
        </div>
      </section>

      {/* Platform grid */}
      <section className="max-w-5xl mx-auto px-6 pb-24">
        <p className="text-center text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-8">
          Supported Platforms
        </p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {Object.values(PLATFORM_META).map((p) => (
            <div
              key={p.label}
              className="rounded-xl border border-border bg-card px-5 py-4 text-center space-y-2"
            >
              <div className="text-2xl">{p.emoji}</div>
              <p className="text-sm font-semibold">{p.label}</p>
              <p className="text-[11px] text-muted-foreground leading-relaxed">{p.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="border-t border-border bg-card/30">
        <div className="max-w-5xl mx-auto px-6 py-24 grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              icon: "🎬",
              title: "Character Profiles",
              body: "Define your AI character once — visual attributes, wardrobe, environments — and inject them consistently into every prompt.",
            },
            {
              icon: "⚡",
              title: "Visual Hook Templates",
              body: "10 proven hook patterns: Silent Stare, Bold Claim, Urban Reveal, Neon Emergence and more. Stop the scroll in 1-3 seconds.",
            },
            {
              icon: "🧠",
              title: "Outcome-Aware Engine",
              body: "Tell it what you want to achieve — UGC testimonial, fashion editorial, scroll-stop hook — and it auto-selects the optimal lens, angle, lighting and motion.",
            },
            {
              icon: "📸",
              title: "Full Lens & Angle Knowledge",
              body: "Every focal length from 14mm ultra-wide to 200mm telephoto. Every angle from worm's eye to bird's eye. The emotional effect of each encoded.",
            },
            {
              icon: "🎞️",
              title: "Multi-Shot Sequences",
              body: "Build complete Hook → Body → CTA video sequences. Techwear promo, UGC standard, product demo, story arc — all structured for maximum retention.",
            },
            {
              icon: "🖼️",
              title: "Kling Omni Image→Video",
              body: "Feed your actual character photo as a reference image. Kling 3.0 Omni animates it to life with 100% character consistency.",
            },
          ].map((f) => (
            <div key={f.title} className="space-y-3">
              <div className="text-2xl">{f.icon}</div>
              <h3 className="font-semibold text-sm">{f.title}</h3>
              <p className="text-[13px] text-muted-foreground leading-relaxed">{f.body}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
