import { Metadata } from 'next'
import { createServerClient } from '@/lib/supabase-server'
import { DashboardHome } from '@/components/dashboard/dashboard-home'

export const metadata: Metadata = {
  title: 'Dashboard',
}

export default async function DashboardPage() {
  const supabase = await createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  // Fetch recent searches for this user
  const { data: recentSearches } = await supabase
    .from('fault_searches')
    .select('id, query, created_at, sites(name)')
    .eq('user_id', user!.id)
    .order('created_at', { ascending: false })
    .limit(8)

  const { data: profileData } = await supabase
    .from('users')
    .select('full_name, role')
    .eq('id', user!.id)
    .maybeSingle()

  const profile = profileData as { full_name: string | null; role: string } | null

  return (
    <DashboardHome
      recentSearches={recentSearches ?? []}
      userFirstName={profile?.full_name?.split(' ')[0] ?? null}
    />
  )
}
