"use client";
import { motion } from "framer-motion";

const services = [
  {
    title: "AI Product Photography",
    desc: "Photorealistic product images generated and enhanced with AI. Perfect for e-commerce, social media, and advertising campaigns.",
    features: ["Product mockups & lifestyle shots", "Background generation & swaps", "Batch variations for A/B testing"],
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6 text-white">
        <rect x="3" y="3" width="18" height="18" rx="2" />
        <circle cx="8.5" cy="8.5" r="1.5" />
        <path d="m21 15-5-5L5 21" />
      </svg>
    ),
  },
  {
    title: "AI Video Content",
    desc: "Dynamic video content crafted with AI tools for social reels, ads, and branded storytelling that captures attention.",
    features: ["Short-form social videos & reels", "AI-generated motion graphics", "Brand story animations"],
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6 text-white">
        <polygon points="23 7 16 12 23 17 23 7" />
        <rect x="1" y="5" width="15" height="14" rx="2" />
      </svg>
    ),
  },
  {
    title: "Social Media Content",
    desc: "Scroll-stopping social content designed to grow your audience and drive engagement across all platforms.",
    features: ["Feed posts & carousel designs", "Story & reel templates", "Platform-specific optimization"],
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6 text-white">
        <path d="M12 2L2 7l10 5 10-5-10-5z" />
        <path d="M2 17l10 5 10-5" />
        <path d="M2 12l10 5 10-5" />
      </svg>
    ),
  },
  {
    title: "Brand Identity & Assets",
    desc: "Complete visual identity systems built with AI assistance. Logos, color palettes, typography, and brand guidelines.",
    features: ["AI-assisted logo concepts", "Brand style guides", "Marketing collateral design"],
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6 text-white">
        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
        <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
        <line x1="12" y1="22.08" x2="12" y2="12" />
      </svg>
    ),
  },
  {
    title: "Campaign Creative",
    desc: "Full campaign creative direction and asset production. From concept to delivery, powered by AI efficiency.",
    features: ["Ad creative & variations", "Email marketing visuals", "Landing page assets"],
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6 text-white">
        <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
      </svg>
    ),
  },
  {
    title: "UGC-Style AI Content",
    desc: "Authentic-looking user-generated content created with AI. Perfect for brands wanting relatable, organic-feeling visuals.",
    features: ['Lifestyle & "in-the-wild" shots', "Testimonial-style visuals", "Community content at scale"],
    icon: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="w-6 h-6 text-white">
        <circle cx="12" cy="12" r="10" />
        <path d="M8 14s1.5 2 4 2 4-2 4-2" />
        <line x1="9" y1="9" x2="9.01" y2="9" />
        <line x1="15" y1="9" x2="15.01" y2="9" />
      </svg>
    ),
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

export default function Services() {
  return (
    <section id="services" className="py-28 bg-[#0a0a0b]">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <p className="text-xs font-semibold uppercase tracking-[3px] text-violet-400 mb-3">
            What I Do
          </p>
          <h2 className="font-serif text-[clamp(2rem,5vw,3.5rem)] font-bold leading-tight mb-4">
            Services
          </h2>
          <p className="text-base text-zinc-400 max-w-xl mx-auto">
            End-to-end AI content creation tailored for your brand&apos;s unique voice and vision.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((s, i) => (
            <motion.div
              key={s.title}
              custom={i}
              variants={cardVariants}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-60px" }}
              className="group bg-zinc-900 border border-white/[0.06] rounded-2xl p-8 hover:bg-zinc-800/80 hover:border-zinc-700 hover:-translate-y-1 hover:shadow-lg transition-all duration-300"
            >
              <div className="w-12 h-12 flex items-center justify-center bg-gradient-to-br from-violet-500 to-pink-500 rounded-lg mb-6">
                {s.icon}
              </div>
              <h3 className="font-serif text-xl font-semibold mb-3">{s.title}</h3>
              <p className="text-sm text-zinc-400 leading-relaxed mb-5">{s.desc}</p>
              <ul className="flex flex-col gap-2">
                {s.features.map((f) => (
                  <li
                    key={f}
                    className="text-xs text-zinc-500 pl-4 relative before:absolute before:left-0 before:top-[6px] before:w-1.5 before:h-1.5 before:rounded-full before:bg-violet-500"
                  >
                    {f}
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
