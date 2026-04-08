"use client";
import { motion } from "framer-motion";

const steps = [
  { num: "01", title: "Discovery Call", desc: "We hop on a quick call to understand your brand, audience, goals, and aesthetic preferences." },
  { num: "02", title: "Creative Brief", desc: "I put together a detailed brief with mood boards, style references, and a content plan for your approval." },
  { num: "03", title: "AI Production", desc: "Using top AI tools and creative expertise, I produce all your content with precision and speed." },
  { num: "04", title: "Review & Deliver", desc: "You review everything, request revisions, and receive final files in all formats you need." },
];

const stepVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.15, duration: 0.5 },
  }),
};

export default function Process() {
  return (
    <section className="py-28 bg-[#0a0a0b]">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <p className="text-xs font-semibold uppercase tracking-[3px] text-violet-400 mb-3">How It Works</p>
          <h2 className="font-serif text-[clamp(2rem,5vw,3.5rem)] font-bold leading-tight mb-4">My Process</h2>
          <p className="text-base text-zinc-400 max-w-xl mx-auto">
            Simple, transparent, and built for speed.
          </p>
        </div>

        <div className="flex flex-wrap items-start justify-center max-w-4xl mx-auto">
          {steps.map((s, i) => (
            <div key={s.num} className="contents">
              <motion.div
                custom={i}
                variants={stepVariants}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: "-60px" }}
                className="flex-1 min-w-[200px] text-center px-4 md:px-6"
              >
                <p className="font-serif text-3xl font-bold bg-gradient-to-r from-violet-500 to-pink-500 bg-clip-text text-transparent mb-4">
                  {s.num}
                </p>
                <h3 className="font-serif text-lg font-semibold mb-2">{s.title}</h3>
                <p className="text-sm text-zinc-400 leading-relaxed">{s.desc}</p>
              </motion.div>
              {i < steps.length - 1 && (
                <div className="hidden md:block w-12 h-px bg-gradient-to-r from-zinc-800 via-violet-500 to-zinc-800 mt-6 flex-shrink-0" />
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
