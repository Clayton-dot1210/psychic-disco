import { Metadata } from 'next'
import { MapPin } from 'lucide-react'

export const metadata: Metadata = { title: 'Sites' }

export default function SitesPage() {
  return (
    <div className="h-full flex flex-col">
      <div className="flex-shrink-0 border-b border-border px-8 py-5">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-lg bg-emerald-400/10 flex items-center justify-center">
            <MapPin className="h-4 w-4 text-emerald-400" />
          </div>
          <div>
            <h1 className="text-lg font-semibold tracking-tight">Sites</h1>
            <p className="text-sm text-muted-foreground">Manage your plant sites</p>
          </div>
        </div>
      </div>
      <div className="flex-1 flex items-center justify-center text-muted-foreground text-sm">
        Sites — coming soon
      </div>
    </div>
  )
}
