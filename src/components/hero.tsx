"use client";
import { motion } from "framer-motion";
import { SparklesCore } from "@/components/ui/sparkles";

const stats = [
  { number: "50+", label: "Brands Served" },
  { number: "500+", label: "Assets Created" },
  { number: "10x", label: "Faster Delivery" },
];

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.12, duration: 0.7 },
  }),
};

export default function Hero() {
  const scrollTo = (href: string) => {
    const el = document.querySelector(href);
    if (el) el.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <header id="hero" className="relative min-h-screen flex items-center justify-center text-center overflow-hidden">
      {/* Sparkles Background */}
      <div className="absolute inset-0 z-0">
        <SparklesCore
          id="hero-sparkles"
          background="transparent"
          minSize={0.6}
          maxSize={1.8}
          particleDensity={100}
          className="w-full h-full"
          particleColor="#a78bfa"
          speed={2}
        />
      </div>

      {/* Gradient Overlays */}
      <div className="absolute inset-0 z-[1]">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_20%_50%,rgba(139,92,246,0.15),transparent_60%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_80%_20%,rgba(236,72,153,0.1),transparent_50%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_80%,rgba(139,92,246,0.08),transparent_50%)]" />
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-4xl px-6 pt-28 pb-20">
        <motion.p
          custom={0}
          variants={fadeUp}
          initial="hidden"
          animate="visible"
          className="text-xs font-semibold uppercase tracking-[4px] text-violet-400 mb-6"
        >
          AI-Powered Brand Content
        </motion.p>

        <motion.h1
          custom={1}
          variants={fadeUp}
          initial="hidden"
          animate="visible"
          className="font-serif text-[clamp(2.5rem,7vw,4.5rem)] font-bold leading-[1.1] mb-6"
        >
          Elevating Brands Through{" "}
          <span className="bg-gradient-to-r from-violet-500 to-pink-500 bg-clip-text text-transparent">
            AI-Driven
          </span>{" "}
          Creative Content
        </motion.h1>

        <motion.p
          custom={2}
          variants={fadeUp}
          initial="hidden"
          animate="visible"
          className="text-lg text-zinc-400 max-w-2xl mx-auto mb-10 leading-relaxed"
        >
          I create stunning visual content for brands using cutting-edge AI tools
          combined with expert creative direction. From product shoots to full
          campaign rollouts.
        </motion.p>

        <motion.div
          custom={3}
          variants={fadeUp}
          initial="hidden"
          animate="visible"
          className="flex gap-4 justify-center flex-wrap mb-16"
        >
          <button
            onClick={() => scrollTo("#portfolio")}
            className="px-8 py-3.5 text-sm font-semibold text-white bg-gradient-to-r from-violet-500 to-pink-500 rounded-xl shadow-[0_0_40px_rgba(139,92,246,0.3)] hover:-translate-y-0.5 hover:shadow-[0_0_60px_rgba(139,92,246,0.3)] transition-all"
          >
            View My Work
          </button>
          <button
            onClick={() => scrollTo("#packages")}
            className="px-8 py-3.5 text-sm font-semibold text-white border border-zinc-700 rounded-xl hover:border-violet-500 hover:text-violet-300 hover:-translate-y-0.5 transition-all"
          >
            See Packages
          </button>
        </motion.div>

        <motion.div
          custom={4}
          variants={fadeUp}
          initial="hidden"
          animate="visible"
          className="flex gap-12 justify-center flex-wrap"
        >
          {stats.map((stat) => (
            <div key={stat.label} className="flex flex-col items-center">
              <span className="font-serif text-4xl font-bold bg-gradient-to-r from-violet-500 to-pink-500 bg-clip-text text-transparent">
                {stat.number}
              </span>
              <span className="text-xs text-zinc-500 mt-1">{stat.label}</span>
            </div>
          ))}
        </motion.div>
      </div>

      {/* Scroll Indicator */}
      <motion.div
        animate={{ y: [0, 8, 0] }}
        transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-zinc-500"
      >
        <span className="text-[0.65rem] uppercase tracking-[2px]">Scroll to explore</span>
        <div className="w-4 h-4 border-r-[1.5px] border-b-[1.5px] border-zinc-500 rotate-45" />
      </motion.div>
    </header>
  );
}
