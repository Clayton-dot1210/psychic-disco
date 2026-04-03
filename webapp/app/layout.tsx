import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Reel Engine — AI Video Prompt Studio",
  description:
    "Generate highest-quality AI video prompts for Kling 3.0, Seedance 2.0, Higgsfield, Runway and more. Built for UGC, visual hooks, and AI content characters.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-background antialiased">{children}</body>
    </html>
  );
}
