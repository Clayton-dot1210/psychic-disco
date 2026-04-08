"use client";
import { motion } from "framer-motion";

const Check = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-4 h-4 text-green-500 flex-shrink-0">
    <polyline points="20 6 9 17 4 12" />
  </svg>
);

const packages = [
  {
    badge: "Starter",
    name: "Content Spark",
    price: "$500",
    period: "/project",
    desc: "Perfect for small brands or one-off projects that need a quick creative boost.",
    features: [
      "5 AI-generated images",
      "2 revision rounds",
      "1 style direction",
      "Social-ready formats",
      "3-day turnaround",
    ],
    featured: false,
  },
  {
    badge: "Most Popular",
    name: "Brand Builder",
    price: "$1,500",
    period: "/month",
    desc: "For growing brands that need consistent, high-quality AI content every month.",
    features: [
      "20 AI-generated images",
      "3 short-form videos",
      "Unlimited revisions",
      "Content calendar planning",
      "Platform-optimized formats",
      "Priority support",
    ],
    featured: true,
  },
  {
    badge: "Premium",
    name: "Full Studio",
    price: "$3,500",
    period: "/month",
    desc: "The complete creative partner. Ideal for brands running multi-channel campaigns.",
    features: [
      "50+ AI-generated images",
      "10 short-form videos",
      "Full campaign creative",
      "Brand style guide",
      "Dedicated creative direction",
      "Same-day turnaround",
      "Monthly strategy call",
    ],
    featured: false,
  },
];

const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.12, duration: 0.5 },
  }),
};

export default function Packages() {
  const scrollTo = () => {
    const el = document.querySelector("#contact");
    if (el) el.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section id="packages" className="py-28 bg-[#0a0a0b]">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <p className="text-xs font-semibold uppercase tracking-[3px] text-violet-400 mb-3">Pricing</p>
          <h2 className="font-serif text-[clamp(2rem,5vw,3.5rem)] font-bold leading-tight mb-4">Packages</h2>
          <p className="text-base text-zinc-400 max-w-xl mx-auto">
            Flexible packages designed to fit your brand&apos;s needs and budget.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-start">
          {packages.map((pkg, i) => (
            <motion.div
              key={pkg.name}
              custom={i}
              variants={cardVariants}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-60px" }}
              className={`rounded-2xl p-8 transition-all duration-300 hover:-translate-y-1 ${
                pkg.featured
                  ? "bg-gradient-to-br from-violet-500/10 to-pink-500/10 border border-violet-500 md:scale-[1.03] hover:shadow-[0_0_40px_rgba(139,92,246,0.3)]"
                  : "bg-zinc-900 border border-white/[0.06] hover:shadow-lg"
              }`}
            >
              <p className="text-xs font-semibold uppercase tracking-[2px] text-violet-400 mb-2">
                {pkg.badge}
              </p>
              <h3 className="font-serif text-2xl font-bold mb-4">{pkg.name}</h3>
              <p className="mb-4">
                <span className="font-serif text-4xl font-bold">{pkg.price}</span>
                <span className="text-sm text-zinc-500">{pkg.period}</span>
              </p>
              <p className="text-sm text-zinc-400 leading-relaxed mb-7">{pkg.desc}</p>

              <ul className="flex flex-col gap-3.5 mb-8">
                {pkg.features.map((f) => (
                  <li key={f} className="flex items-center gap-3 text-sm text-zinc-400">
                    <Check />
                    {f}
                  </li>
                ))}
              </ul>

              <button
                onClick={scrollTo}
                className={`w-full py-3.5 text-sm font-semibold rounded-xl transition-all ${
                  pkg.featured
                    ? "bg-gradient-to-r from-violet-500 to-pink-500 text-white shadow-[0_0_40px_rgba(139,92,246,0.3)] hover:-translate-y-0.5"
                    : "border border-zinc-700 text-white hover:border-violet-500 hover:text-violet-300 hover:-translate-y-0.5"
                }`}
              >
                Get Started
              </button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
