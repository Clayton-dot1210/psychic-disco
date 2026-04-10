import { Metadata } from 'next'
import { BookOpen } from 'lucide-react'

export const metadata: Metadata = { title: 'Process Library' }

export default function ProceduresPage() {
  return (
    <div className="h-full flex flex-col">
      <div className="flex-shrink-0 border-b border-border px-8 py-5">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-lg bg-blue-400/10 flex items-center justify-center">
            <BookOpen className="h-4 w-4 text-blue-400" />
          </div>
          <div>
            <h1 className="text-lg font-semibold tracking-tight">Process Library</h1>
            <p className="text-sm text-muted-foreground">Browse maintenance procedures</p>
          </div>
        </div>
      </div>
      <div className="flex-1 flex items-center justify-center text-muted-foreground text-sm">
        Process Library — coming soon
      </div>
    </div>
  )
}
