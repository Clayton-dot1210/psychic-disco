import { Metadata } from 'next'
import { Library } from 'lucide-react'

export const metadata: Metadata = { title: 'Knowledge Base' }

export default function KnowledgeBasePage() {
  return (
    <div className="h-full flex flex-col">
      <div className="flex-shrink-0 border-b border-border px-8 py-5">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-lg bg-purple-400/10 flex items-center justify-center">
            <Library className="h-4 w-4 text-purple-400" />
          </div>
          <div>
            <h1 className="text-lg font-semibold tracking-tight">Knowledge Base</h1>
            <p className="text-sm text-muted-foreground">Documents & manuals</p>
          </div>
        </div>
      </div>
      <div className="flex-1 flex items-center justify-center text-muted-foreground text-sm">
        Knowledge Base — coming soon
      </div>
    </div>
  )
}
