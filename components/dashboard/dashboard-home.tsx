'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import {
  Search,
  Zap,
  BookOpen,
  Library,
  MapPin,
  Clock,
  ArrowRight,
  Sparkles,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { cn, formatRelativeTime } from '@/lib/utils'

interface RecentSearch {
  id: string
  query: string
  created_at: string
  sites?: { name: string } | null
}

interface DashboardHomeProps {
  recentSearches: RecentSearch[]
  userFirstName: string | null
}

const QUICK_ACCESS = [
  {
    href: '/dashboard/fault-search',
    label: 'Fault Search',
    description: 'AI-powered fault diagnosis',
    icon: Zap,
    color: 'text-amber-400',
    bg: 'bg-amber-400/10 hover:bg-amber-400/15',
    border: 'border-amber-400/20',
    badge: 'AI',
    badgeVariant: 'warning' as const,
  },
  {
    href: '/dashboard/procedures',
    label: 'Process Library',
    description: 'Browse maintenance procedures',
    icon: BookOpen,
    color: 'text-blue-400',
    bg: 'bg-blue-400/10 hover:bg-blue-400/15',
    border: 'border-blue-400/20',
    badge: null,
    badgeVariant: null,
  },
  {
    href: '/dashboard/knowledge-base',
    label: 'Knowledge Base',
    description: 'Documents & manuals',
    icon: Library,
    color: 'text-purple-400',
    bg: 'bg-purple-400/10 hover:bg-purple-400/15',
    border: 'border-purple-400/20',
    badge: null,
    badgeVariant: null,
  },
  {
    href: '/dashboard/sites',
    label: 'Sites',
    description: 'Manage your plant sites',
    icon: MapPin,
    color: 'text-emerald-400',
    bg: 'bg-emerald-400/10 hover:bg-emerald-400/15',
    border: 'border-emerald-400/20',
    badge: null,
    badgeVariant: null,
  },
]

export function DashboardHome({
  recentSearches,
  userFirstName,
}: DashboardHomeProps) {
  const router = useRouter()
  const [query, setQuery] = useState('')

  function handleSearch(e: React.FormEvent) {
    e.preventDefault()
    if (!query.trim()) return
    router.push(`/dashboard/fault-search?q=${encodeURIComponent(query.trim())}`)
  }

  function handleRecentClick(search: RecentSearch) {
    router.push(
      `/dashboard/fault-search?q=${encodeURIComponent(search.query)}`
    )
  }

  const greeting = getGreeting()

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex-shrink-0 border-b border-border px-8 py-5 flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold tracking-tight">
            {greeting}
            {userFirstName ? `, ${userFirstName}` : ''}
          </h1>
          <p className="text-sm text-muted-foreground">
            What do you need to diagnose today?
          </p>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 overflow-auto">
        <div className="max-w-2xl mx-auto px-8 py-12 space-y-12">

          {/* Hero search */}
          <div className="space-y-4 animate-fade-in">
            <div className="flex items-center gap-2 text-muted-foreground mb-6">
              <Sparkles className="h-4 w-4 text-amber-400" />
              <span className="text-xs font-medium tracking-wide uppercase">
                AI Fault Search
              </span>
            </div>

            <form onSubmit={handleSearch} className="relative group">
              <div className="absolute left-4 top-1/2 -translate-y-1/2 pointer-events-none">
                <Search className="h-5 w-5 text-muted-foreground group-focus-within:text-foreground transition-colors" />
              </div>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Describe a fault or symptom… e.g. 'motor overheating on site 2'"
                className={cn(
                  'w-full h-14 pl-12 pr-32 rounded-xl border border-border bg-card text-base',
                  'placeholder:text-muted-foreground/60',
                  'focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent',
                  'transition-all duration-150',
                  'shadow-sm hover:shadow-md'
                )}
              />
              <div className="absolute right-3 top-1/2 -translate-y-1/2">
                <Button
                  type="submit"
                  size="sm"
                  disabled={!query.trim()}
                  className="h-8 px-4 gap-1.5"
                >
                  Search
                  <ArrowRight className="h-3.5 w-3.5" />
                </Button>
              </div>
            </form>

            <p className="text-xs text-muted-foreground pl-1">
              Powered by Claude AI · Searches your company&apos;s procedures & documents
            </p>
          </div>

          {/* Quick access tiles */}
          <div className="space-y-3 animate-fade-in" style={{ animationDelay: '0.05s' }}>
            <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              Quick access
            </h2>
            <div className="grid grid-cols-2 gap-3">
              {QUICK_ACCESS.map((item) => (
                <button
                  key={item.href}
                  onClick={() => router.push(item.href)}
                  className={cn(
                    'group relative flex flex-col gap-3 p-4 rounded-xl border transition-all duration-150 text-left',
                    'hover:shadow-sm active:scale-[0.98]',
                    item.bg,
                    item.border
                  )}
                >
                  <div className="flex items-start justify-between">
                    <div className={cn('p-2 rounded-lg bg-background/60', item.color)}>
                      <item.icon className="h-4 w-4" />
                    </div>
                    {item.badge && item.badgeVariant && (
                      <Badge variant={item.badgeVariant} className="text-[10px] px-1.5 py-0">
                        {item.badge}
                      </Badge>
                    )}
                  </div>
                  <div>
                    <p className="text-sm font-semibold">{item.label}</p>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      {item.description}
                    </p>
                  </div>
                  <ArrowRight className="absolute bottom-4 right-4 h-3.5 w-3.5 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity translate-x-[-4px] group-hover:translate-x-0 transition-transform duration-150" />
                </button>
              ))}
            </div>
          </div>

          {/* Recent searches */}
          {recentSearches.length > 0 && (
            <div className="space-y-3 animate-fade-in" style={{ animationDelay: '0.1s' }}>
              <div className="flex items-center justify-between">
                <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Recent searches
                </h2>
                <button
                  onClick={() => router.push('/dashboard/fault-search')}
                  className="text-xs text-muted-foreground hover:text-foreground transition-colors"
                >
                  View all
                </button>
              </div>
              <div className="space-y-1">
                {recentSearches.map((search) => (
                  <button
                    key={search.id}
                    onClick={() => handleRecentClick(search)}
                    className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-accent transition-colors group text-left"
                  >
                    <Clock className="h-3.5 w-3.5 text-muted-foreground flex-shrink-0" />
                    <span className="flex-1 text-sm truncate text-foreground/80 group-hover:text-foreground transition-colors">
                      {search.query}
                    </span>
                    <div className="flex items-center gap-2 flex-shrink-0">
                      {search.sites?.name && (
                        <span className="text-xs text-muted-foreground hidden sm:block">
                          {search.sites.name}
                        </span>
                      )}
                      <span className="text-xs text-muted-foreground">
                        {formatRelativeTime(search.created_at)}
                      </span>
                      <ArrowRight className="h-3 w-3 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Empty state for new users */}
          {recentSearches.length === 0 && (
            <div className="text-center py-8 space-y-2 animate-fade-in" style={{ animationDelay: '0.1s' }}>
              <div className="mx-auto h-12 w-12 rounded-full bg-muted flex items-center justify-center">
                <Zap className="h-5 w-5 text-muted-foreground" />
              </div>
              <p className="text-sm font-medium">No searches yet</p>
              <p className="text-xs text-muted-foreground">
                Run your first fault search to get started
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function getGreeting(): string {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 18) return 'Good afternoon'
  return 'Good evening'
}
