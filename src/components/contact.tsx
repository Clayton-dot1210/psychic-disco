"use client";
import { useState, type FormEvent } from "react";
import { motion } from "framer-motion";

const serviceOptions = [
  { value: "product-photography", label: "AI Product Photography" },
  { value: "video-content", label: "AI Video Content" },
  { value: "social-media", label: "Social Media Content" },
  { value: "brand-identity", label: "Brand Identity & Assets" },
  { value: "campaign", label: "Campaign Creative" },
  { value: "ugc", label: "UGC-Style AI Content" },
  { value: "custom", label: "Custom Package" },
];

const budgetOptions = [
  { value: "under-500", label: "Under $500" },
  { value: "500-1500", label: "$500 - $1,500" },
  { value: "1500-3500", label: "$1,500 - $3,500" },
  { value: "3500-plus", label: "$3,500+" },
];

export default function Contact() {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    setTimeout(() => {
      setSubmitted(false);
      (e.target as HTMLFormElement).reset();
    }, 3000);
  };

  return (
    <section id="contact" className="py-28 bg-[#111113]">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
          {/* Info */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <p className="text-xs font-semibold uppercase tracking-[3px] text-violet-400 mb-3">
              Get In Touch
            </p>
            <h2 className="font-serif text-[clamp(1.8rem,4vw,2.5rem)] font-bold leading-tight mb-5">
              Let&apos;s Create Something Amazing
            </h2>
            <p className="text-zinc-400 leading-relaxed mb-8">
              Ready to elevate your brand&apos;s visual content? Fill out the form and
              I&apos;ll get back to you within 24 hours.
            </p>

            <div className="flex flex-col gap-4 mb-8">
              <div className="flex items-center gap-3 text-zinc-400">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-5 h-5 text-violet-400 flex-shrink-0">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                  <polyline points="22,6 12,13 2,6" />
                </svg>
                <span className="text-sm">hello@aicontentstudio.com</span>
              </div>
              <div className="flex items-center gap-3 text-zinc-400">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-5 h-5 text-violet-400 flex-shrink-0">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
                  <circle cx="12" cy="10" r="3" />
                </svg>
                <span className="text-sm">Available Worldwide (Remote)</span>
              </div>
            </div>

            {/* Social Links */}
            <div className="flex gap-3">
              {[
                { label: "Instagram", path: <><rect x="2" y="2" width="20" height="20" rx="5" /><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" /><line x1="17.5" y1="6.5" x2="17.51" y2="6.5" /></> },
                { label: "Twitter/X", path: <><path d="M4 4l11.733 16h4.267l-11.733-16z" /><path d="M4 20l6.768-6.768m2.46-2.46l6.772-6.772" /></> },
                { label: "LinkedIn", path: <><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z" /><rect x="2" y="9" width="4" height="12" /><circle cx="4" cy="4" r="2" /></> },
                { label: "TikTok", path: <path d="M9 12a4 4 0 1 0 4 4V4a5 5 0 0 0 5 5" /> },
              ].map((s) => (
                <a
                  key={s.label}
                  href="#"
                  aria-label={s.label}
                  className="w-11 h-11 flex items-center justify-center border border-zinc-800 rounded-lg hover:border-violet-500 hover:bg-violet-500/10 transition-all"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-5 h-5 text-zinc-400 hover:text-violet-400 transition-colors">
                    {s.path}
                  </svg>
                </a>
              ))}
            </div>
          </motion.div>

          {/* Form */}
          <motion.form
            onSubmit={handleSubmit}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.15 }}
            className="bg-zinc-900 border border-white/[0.06] rounded-2xl p-8 sm:p-10"
          >
            <div className="space-y-5">
              <div>
                <label htmlFor="name" className="block text-xs font-medium text-zinc-400 mb-2">Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  required
                  placeholder="Your name"
                  className="w-full px-4 py-3.5 text-sm text-white bg-[#0a0a0b] border border-zinc-800 rounded-lg outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30 transition-all placeholder:text-zinc-600"
                />
              </div>
              <div>
                <label htmlFor="email" className="block text-xs font-medium text-zinc-400 mb-2">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  required
                  placeholder="you@brand.com"
                  className="w-full px-4 py-3.5 text-sm text-white bg-[#0a0a0b] border border-zinc-800 rounded-lg outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30 transition-all placeholder:text-zinc-600"
                />
              </div>
              <div>
                <label htmlFor="service" className="block text-xs font-medium text-zinc-400 mb-2">What are you looking for?</label>
                <select
                  id="service"
                  name="service"
                  required
                  defaultValue=""
                  className="w-full px-4 py-3.5 text-sm text-white bg-[#0a0a0b] border border-zinc-800 rounded-lg outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30 transition-all appearance-none"
                >
                  <option value="" disabled>Select a service</option>
                  {serviceOptions.map((o) => (
                    <option key={o.value} value={o.value}>{o.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label htmlFor="budget" className="block text-xs font-medium text-zinc-400 mb-2">Budget Range</label>
                <select
                  id="budget"
                  name="budget"
                  defaultValue=""
                  className="w-full px-4 py-3.5 text-sm text-white bg-[#0a0a0b] border border-zinc-800 rounded-lg outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30 transition-all appearance-none"
                >
                  <option value="" disabled>Select budget range</option>
                  {budgetOptions.map((o) => (
                    <option key={o.value} value={o.value}>{o.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label htmlFor="message" className="block text-xs font-medium text-zinc-400 mb-2">Tell me about your project</label>
                <textarea
                  id="message"
                  name="message"
                  rows={4}
                  required
                  placeholder="Describe your brand, what you're looking for, and any deadlines..."
                  className="w-full px-4 py-3.5 text-sm text-white bg-[#0a0a0b] border border-zinc-800 rounded-lg outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30 transition-all resize-y min-h-[120px] placeholder:text-zinc-600"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={submitted}
              className={`w-full mt-6 py-3.5 text-sm font-semibold rounded-xl transition-all ${
                submitted
                  ? "bg-green-500 text-white"
                  : "bg-gradient-to-r from-violet-500 to-pink-500 text-white shadow-[0_0_40px_rgba(139,92,246,0.3)] hover:-translate-y-0.5"
              }`}
            >
              {submitted ? "Message Sent!" : "Send Message"}
            </button>
          </motion.form>
        </div>
      </div>
    </section>
  );
}
