import { Metadata } from 'next'
import Link from 'next/link'
import { SignupForm } from '@/components/auth/signup-form'

export const metadata: Metadata = {
  title: 'Create Account',
}

export default function SignupPage() {
  return (
    <div className="min-h-screen flex">
      {/* Left panel — branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-zinc-950 flex-col justify-between p-12 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-zinc-900 via-zinc-950 to-black" />
        <div
          className="absolute inset-0 opacity-[0.04]"
          style={{
            backgroundImage:
              'linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)',
            backgroundSize: '40px 40px',
          }}
        />

        <div className="relative z-10">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-white flex items-center justify-center">
              <svg viewBox="0 0 24 24" className="h-4 w-4 fill-black">
                <path d="M13 3L4 14h7l-1 7 9-11h-7l1-7z" />
              </svg>
            </div>
            <span className="text-white font-semibold text-lg tracking-tight">
              FaultBase
            </span>
          </div>
        </div>

        <div className="relative z-10 space-y-8">
          <div className="space-y-3">
            <h2 className="text-3xl font-bold text-white leading-tight">
              Resolve faults faster with AI
            </h2>
            <p className="text-white/50 text-base leading-relaxed">
              Give your engineering team an AI-powered knowledge base that surfaces
              the right procedure at the right time.
            </p>
          </div>

          <ul className="space-y-3">
            {[
              'Instant fault diagnosis powered by Claude AI',
              'Company-scoped knowledge base & documents',
              'Role-based access for admins and engineers',
              'Per-site procedure management',
            ].map((feature) => (
              <li key={feature} className="flex items-start gap-3 text-sm text-white/70">
                <span className="mt-0.5 h-4 w-4 rounded-full bg-white/20 flex items-center justify-center flex-shrink-0">
                  <svg viewBox="0 0 12 12" className="h-2.5 w-2.5 fill-white">
                    <path d="M2 6l3 3 5-5" stroke="white" strokeWidth="1.5" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </span>
                {feature}
              </li>
            ))}
          </ul>
        </div>

        <div className="relative z-10 text-xs text-white/30">
          © 2025 FaultBase. All rights reserved.
        </div>
      </div>

      {/* Right panel — form */}
      <div className="flex-1 flex flex-col items-center justify-center p-8 bg-background">
        <div className="w-full max-w-sm space-y-8">
          {/* Mobile logo */}
          <div className="flex items-center gap-2 lg:hidden">
            <div className="h-8 w-8 rounded-lg bg-foreground flex items-center justify-center">
              <svg viewBox="0 0 24 24" className="h-4 w-4 fill-background">
                <path d="M13 3L4 14h7l-1 7 9-11h-7l1-7z" />
              </svg>
            </div>
            <span className="font-semibold text-lg tracking-tight">
              FaultBase
            </span>
          </div>

          <div className="space-y-2">
            <h1 className="text-2xl font-bold tracking-tight">Create an account</h1>
            <p className="text-sm text-muted-foreground">
              Set up FaultBase for your engineering team
            </p>
          </div>

          <SignupForm />

          <p className="text-center text-sm text-muted-foreground">
            Already have an account?{' '}
            <Link
              href="/auth/login"
              className="text-foreground font-medium underline underline-offset-4 hover:text-foreground/80 transition-colors"
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
