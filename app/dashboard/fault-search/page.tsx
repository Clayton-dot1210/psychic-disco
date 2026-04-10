import { Metadata } from 'next'
import { Zap } from 'lucide-react'

export const metadata: Metadata = { title: 'Fault Search' }

export default function FaultSearchPage() {
  return (
    <div className="h-full flex flex-col">
      <div className="flex-shrink-0 border-b border-border px-8 py-5">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-lg bg-amber-400/10 flex items-center justify-center">
            <Zap className="h-4 w-4 text-amber-400" />
          </div>
          <div>
            <h1 className="text-lg font-semibold tracking-tight">Fault Search</h1>
            <p className="text-sm text-muted-foreground">AI-powered fault diagnosis</p>
          </div>
        </div>
      </div>
      <div className="flex-1 flex items-center justify-center text-muted-foreground text-sm">
        Fault Search — coming soon
      </div>
    </div>
  )
}
