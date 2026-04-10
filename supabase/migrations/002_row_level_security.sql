-- ============================================================
-- ROW LEVEL SECURITY — all tables scoped to company
-- ============================================================

-- Helper: get the caller's company_id from their user profile
CREATE OR REPLACE FUNCTION public.current_user_company_id()
RETURNS UUID AS $$
  SELECT company_id FROM public.users WHERE id = auth.uid()
$$ LANGUAGE sql STABLE SECURITY DEFINER;

-- Helper: get the caller's role
CREATE OR REPLACE FUNCTION public.current_user_role()
RETURNS TEXT AS $$
  SELECT role FROM public.users WHERE id = auth.uid()
$$ LANGUAGE sql STABLE SECURITY DEFINER;

-- ============================================================
-- COMPANIES
-- ============================================================
ALTER TABLE public.companies ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own company"
  ON public.companies FOR SELECT
  USING (id = public.current_user_company_id());

CREATE POLICY "Admins can update their own company"
  ON public.companies FOR UPDATE
  USING (id = public.current_user_company_id() AND public.current_user_role() = 'admin');

-- ============================================================
-- USERS
-- ============================================================
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Users can always read/update their own row
CREATE POLICY "Users can view own profile"
  ON public.users FOR SELECT
  USING (id = auth.uid() OR company_id = public.current_user_company_id());

CREATE POLICY "Users can update own profile"
  ON public.users FOR UPDATE
  USING (id = auth.uid());

CREATE POLICY "Admins can update any user in their company"
  ON public.users FOR UPDATE
  USING (company_id = public.current_user_company_id() AND public.current_user_role() = 'admin');

-- Allow service role to insert on signup (trigger runs as SECURITY DEFINER)
CREATE POLICY "Service role can insert users"
  ON public.users FOR INSERT
  WITH CHECK (true);

-- ============================================================
-- SITES
-- ============================================================
ALTER TABLE public.sites ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Company members can view sites"
  ON public.sites FOR SELECT
  USING (company_id = public.current_user_company_id());

CREATE POLICY "Admins can insert sites"
  ON public.sites FOR INSERT
  WITH CHECK (company_id = public.current_user_company_id() AND public.current_user_role() = 'admin');

CREATE POLICY "Admins can update sites"
  ON public.sites FOR UPDATE
  USING (company_id = public.current_user_company_id() AND public.current_user_role() = 'admin');

CREATE POLICY "Admins can delete sites"
  ON public.sites FOR DELETE
  USING (company_id = public.current_user_company_id() AND public.current_user_role() = 'admin');

-- ============================================================
-- FAULT SEARCHES
-- ============================================================
ALTER TABLE public.fault_searches ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own fault searches"
  ON public.fault_searches FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "Admins can view all company fault searches"
  ON public.fault_searches FOR SELECT
  USING (company_id = public.current_user_company_id() AND public.current_user_role() = 'admin');

CREATE POLICY "Users can insert their own fault searches"
  ON public.fault_searches FOR INSERT
  WITH CHECK (user_id = auth.uid() AND company_id = public.current_user_company_id());

-- ============================================================
-- PROCEDURES
-- ============================================================
ALTER TABLE public.procedures ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Company members can view procedures"
  ON public.procedures FOR SELECT
  USING (company_id = public.current_user_company_id());

CREATE POLICY "Admins can manage procedures"
  ON public.procedures FOR ALL
  USING (company_id = public.current_user_company_id() AND public.current_user_role() = 'admin');

-- ============================================================
-- DOCUMENTS
-- ============================================================
ALTER TABLE public.documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Company members can view documents"
  ON public.documents FOR SELECT
  USING (company_id = public.current_user_company_id());

CREATE POLICY "Admins can manage documents"
  ON public.documents FOR ALL
  USING (company_id = public.current_user_company_id() AND public.current_user_role() = 'admin');

-- ============================================================
-- DOCUMENT CHUNKS
-- ============================================================
ALTER TABLE public.document_chunks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Company members can view document chunks"
  ON public.document_chunks FOR SELECT
  USING (company_id = public.current_user_company_id());

CREATE POLICY "Admins can manage document chunks"
  ON public.document_chunks FOR ALL
  USING (company_id = public.current_user_company_id() AND public.current_user_role() = 'admin');

-- ============================================================
-- FEEDBACK
-- ============================================================
ALTER TABLE public.feedback ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own feedback"
  ON public.feedback FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "Admins can view all company feedback"
  ON public.feedback FOR SELECT
  USING (company_id = public.current_user_company_id() AND public.current_user_role() = 'admin');

CREATE POLICY "Users can insert their own feedback"
  ON public.feedback FOR INSERT
  WITH CHECK (user_id = auth.uid() AND company_id = public.current_user_company_id());
