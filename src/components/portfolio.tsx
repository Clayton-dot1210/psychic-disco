"use client";
import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const filters = ["all", "product", "social", "campaign", "branding"] as const;
const filterLabels: Record<string, string> = {
  all: "All Work",
  product: "Product",
  social: "Social",
  campaign: "Campaigns",
  branding: "Branding",
};

const items = [
  { title: "Luxury Skincare Line", type: "AI Product Photography", category: "product", hue: 220, wide: false },
  { title: "Summer Collection Campaign", type: "Full Campaign Creative", category: "campaign", hue: 280, wide: true },
  { title: "Fitness Brand Reels", type: "Social Media Content", category: "social", hue: 340, wide: false },
  { title: "Tech Startup Identity", type: "Brand Identity & Assets", category: "branding", hue: 160, wide: false },
  { title: "Artisan Coffee Brand", type: "AI Product Photography", category: "product", hue: 40, wide: false },
  { title: "Fashion Brand Feed", type: "Social Media Content", category: "social", hue: 200, wide: true },
  { title: "Wellness App Launch", type: "Campaign Creative", category: "campaign", hue: 100, wide: false },
  { title: "Restaurant Rebrand", type: "Brand Identity & Assets", category: "branding", hue: 60, wide: false },
];

export default function Portfolio() {
  const [active, setActive] = useState<string>("all");

  const filtered = items.filter(
    (item) => active === "all" || item.category === active
  );

  return (
    <section id="portfolio" className="py-28 bg-[#111113]">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <p className="text-xs font-semibold uppercase tracking-[3px] text-violet-400 mb-3">
            My Work
          </p>
          <h2 className="font-serif text-[clamp(2rem,5vw,3.5rem)] font-bold leading-tight mb-4">
            Portfolio
          </h2>
          <p className="text-base text-zinc-400 max-w-xl mx-auto">
            A selection of AI-generated brand content across industries and styles.
          </p>
        </div>

        {/* Filters */}
        <div className="flex justify-center gap-2 mb-12 flex-wrap">
          {filters.map((f) => (
            <button
              key={f}
              onClick={() => setActive(f)}
              className={`px-6 py-2.5 text-sm font-medium rounded-full border transition-all duration-300 ${
                active === f
                  ? "bg-gradient-to-r from-violet-500 to-pink-500 text-white border-transparent"
                  : "text-zinc-400 border-zinc-800 hover:text-white hover:border-zinc-600"
              }`}
            >
              {filterLabels[f]}
            </button>
          ))}
        </div>

        {/* Grid */}
        <motion.div layout className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <AnimatePresence mode="popLayout">
            {filtered.map((item) => (
              <motion.div
                key={item.title}
                layout
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.35 }}
                className={`relative rounded-xl overflow-hidden cursor-pointer group ${
                  item.wide ? "sm:col-span-2 aspect-[2/1]" : "aspect-square"
                }`}
              >
                {/* Placeholder Gradient */}
                <div
                  className="w-full h-full flex items-center justify-center text-xs font-medium uppercase tracking-widest"
                  style={{
                    background: `linear-gradient(135deg, hsl(${item.hue},60%,15%), hsl(${item.hue},70%,25%), hsl(${item.hue + 40},60%,20%))`,
                    color: `hsl(${item.hue},50%,70%)`,
                  }}
                >
                  {item.type.split(" ")[0]}
                </div>

                {/* Overlay */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-6">
                  <h4 className="font-serif text-lg">{item.title}</h4>
                  <p className="text-sm text-violet-400">{item.type}</p>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </motion.div>
      </div>
    </section>
  );
}
