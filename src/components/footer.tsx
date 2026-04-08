const links = [
  { href: "#services", label: "Services" },
  { href: "#portfolio", label: "Portfolio" },
  { href: "#packages", label: "Packages" },
  { href: "#shoots", label: "Shoots" },
  { href: "#contact", label: "Contact" },
];

export default function Footer() {
  return (
    <footer className="border-t border-white/[0.06] bg-[#0a0a0b]">
      <div className="max-w-7xl mx-auto px-6 pt-12 pb-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6 mb-8">
          <div className="text-center md:text-left">
            <a
              href="#"
              className="text-xl font-bold font-serif bg-gradient-to-r from-violet-500 to-pink-500 bg-clip-text text-transparent"
            >
              AI Content Studio
            </a>
            <p className="text-sm text-zinc-500 mt-2">
              Creating next-level brand content with AI-powered creative tools.
            </p>
          </div>
          <nav className="flex gap-6 flex-wrap justify-center">
            {links.map((l) => (
              <a
                key={l.href}
                href={l.href}
                className="text-sm text-zinc-400 hover:text-white transition-colors"
              >
                {l.label}
              </a>
            ))}
          </nav>
        </div>
        <div className="text-center border-t border-white/[0.06] pt-6">
          <p className="text-xs text-zinc-600">
            &copy; {new Date().getFullYear()} AI Content Studio. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
