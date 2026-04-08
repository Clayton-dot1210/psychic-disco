"use client";
import { motion } from "framer-motion";

const shoots = [
  {
    num: "01",
    title: "Product Flat Lay",
    desc: "Clean, editorial-style product arrangements. AI-generated backgrounds, lighting, and styling variations let you get dozens of options from a single concept.",
    details: ["5-15 final images", "2-3 day delivery"],
    hue: 250,
  },
  {
    num: "02",
    title: "Lifestyle & Lookbook",
    desc: "AI-crafted lifestyle imagery showing your products in real-world settings. Models, environments, and moods tailored to your target audience.",
    details: ["10-25 final images", "3-5 day delivery"],
    hue: 320,
  },
  {
    num: "03",
    title: "Social Content Batch",
    desc: "A full month's worth of social media visuals in one go. Feed posts, stories, reels covers, and highlights all in your brand style.",
    details: ["20-40 assets", "5-7 day delivery"],
    hue: 180,
  },
  {
    num: "04",
    title: "Campaign Shoot",
    desc: "Full creative production for a launch or campaign. Includes hero images, supporting visuals, ad creative, and all format variations you need.",
    details: ["30-60+ assets", "7-10 day delivery"],
    hue: 30,
  },
  {
    num: "05",
    title: "Video Content Day",
    desc: "AI-powered video content creation session. Short-form videos, motion graphics, and animated content optimized for every platform.",
    details: ["5-10 videos", "5-7 day delivery"],
    hue: 130,
  },
  {
    num: "06",
    title: "Brand Identity Sprint",
    desc: "A focused session to define or refresh your entire visual identity. Logo explorations, color systems, typography, and a complete brand guide.",
    details: ["Full brand kit", "7-14 day delivery"],
    hue: 70,
  },
];

const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.08, duration: 0.5 },
  }),
};

export default function Shoots() {
  return (
    <section id="shoots" className="py-28 bg-[#111113]">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <p className="text-xs font-semibold uppercase tracking-[3px] text-violet-400 mb-3">
            Creative Sessions
          </p>
          <h2 className="font-serif text-[clamp(2rem,5vw,3.5rem)] font-bold leading-tight mb-4">
            Shoot Types
          </h2>
          <p className="text-base text-zinc-400 max-w-xl mx-auto">
            Different shoot formats to match exactly what your brand needs.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {shoots.map((s, i) => (
            <motion.div
              key={s.num}
              custom={i}
              variants={cardVariants}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-60px" }}
              className="group grid grid-cols-[160px_1fr] sm:grid-cols-[200px_1fr] bg-zinc-900 border border-white/[0.06] rounded-2xl overflow-hidden hover:border-zinc-700 hover:-translate-y-1 hover:shadow-lg transition-all duration-300"
            >
              <div
                className="flex items-center justify-center min-h-[180px]"
                style={{
                  background: `linear-gradient(135deg, hsl(${s.hue},50%,15%), hsl(${s.hue},60%,25%))`,
                }}
              >
                <span className="font-serif text-5xl font-bold text-white/[0.12]">
                  {s.num}
                </span>
              </div>
              <div className="p-7 flex flex-col justify-center">
                <h3 className="font-serif text-xl font-semibold mb-3">{s.title}</h3>
                <p className="text-sm text-zinc-400 leading-relaxed mb-4">{s.desc}</p>
                <div className="flex gap-3 flex-wrap">
                  {s.details.map((d) => (
                    <span
                      key={d}
                      className="text-xs font-medium text-violet-400 bg-violet-500/10 border border-violet-500/20 px-3.5 py-1.5 rounded-full"
                    >
                      {d}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
