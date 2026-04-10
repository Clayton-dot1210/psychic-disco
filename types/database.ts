export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      companies: {
        Row: {
          id: string
          name: string
          slug: string
          logo_url: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          name: string
          slug: string
          logo_url?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          name?: string
          slug?: string
          logo_url?: string | null
          updated_at?: string
        }
      }
      users: {
        Row: {
          id: string
          company_id: string | null
          email: string
          full_name: string | null
          avatar_url: string | null
          role: 'admin' | 'engineer'
          created_at: string
          updated_at: string
        }
        Insert: {
          id: string
          company_id?: string | null
          email: string
          full_name?: string | null
          avatar_url?: string | null
          role?: 'admin' | 'engineer'
          created_at?: string
          updated_at?: string
        }
        Update: {
          company_id?: string | null
          email?: string
          full_name?: string | null
          avatar_url?: string | null
          role?: 'admin' | 'engineer'
          updated_at?: string
        }
      }
      sites: {
        Row: {
          id: string
          company_id: string
          name: string
          location: string | null
          description: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          company_id: string
          name: string
          location?: string | null
          description?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          name?: string
          location?: string | null
          description?: string | null
          updated_at?: string
        }
      }
      fault_searches: {
        Row: {
          id: string
          user_id: string
          company_id: string
          site_id: string | null
          query: string
          results: Json | null
          created_at: string
        }
        Insert: {
          id?: string
          user_id: string
          company_id: string
          site_id?: string | null
          query: string
          results?: Json | null
          created_at?: string
        }
        Update: {
          results?: Json | null
        }
      }
      procedures: {
        Row: {
          id: string
          company_id: string
          site_id: string | null
          title: string
          content: string | null
          category: string | null
          tags: string[]
          created_by: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          company_id: string
          site_id?: string | null
          title: string
          content?: string | null
          category?: string | null
          tags?: string[]
          created_by?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          title?: string
          content?: string | null
          category?: string | null
          tags?: string[]
          updated_at?: string
        }
      }
      documents: {
        Row: {
          id: string
          company_id: string
          site_id: string | null
          title: string
          file_url: string | null
          file_type: string | null
          file_size: number | null
          status: 'processing' | 'ready' | 'error'
          uploaded_by: string | null
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          company_id: string
          site_id?: string | null
          title: string
          file_url?: string | null
          file_type?: string | null
          file_size?: number | null
          status?: 'processing' | 'ready' | 'error'
          uploaded_by?: string | null
          created_at?: string
          updated_at?: string
        }
        Update: {
          title?: string
          file_url?: string | null
          status?: 'processing' | 'ready' | 'error'
          updated_at?: string
        }
      }
      document_chunks: {
        Row: {
          id: string
          document_id: string
          company_id: string
          content: string
          chunk_index: number
          metadata: Json
          created_at: string
        }
        Insert: {
          id?: string
          document_id: string
          company_id: string
          content: string
          chunk_index: number
          metadata?: Json
          created_at?: string
        }
        Update: {
          content?: string
          metadata?: Json
        }
      }
      feedback: {
        Row: {
          id: string
          user_id: string
          company_id: string
          fault_search_id: string | null
          rating: number | null
          comment: string | null
          created_at: string
        }
        Insert: {
          id?: string
          user_id: string
          company_id: string
          fault_search_id?: string | null
          rating?: number | null
          comment?: string | null
          created_at?: string
        }
        Update: {
          rating?: number | null
          comment?: string | null
        }
      }
    }
    Views: Record<string, never>
    Functions: {
      current_user_company_id: {
        Args: Record<string, never>
        Returns: string
      }
      current_user_role: {
        Args: Record<string, never>
        Returns: string
      }
    }
    Enums: Record<string, never>
  }
}
