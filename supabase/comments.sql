-- Comments table for the portfolio. Paste all of this into Supabase → SQL Editor → Run.
-- Visitors can only ADD comments (always unapproved) and only SEE approved ones.
-- To approve: Table Editor → comments → tick "approved". To remove: delete the row.

create table if not exists public.comments (
  id          uuid primary key default gen_random_uuid(),
  created_at  timestamptz not null default now(),
  page        text not null check (char_length(page) <= 200),
  path        text check (char_length(path) <= 2000),
  fx real, fy real, x real, y real,
  name        text check (char_length(name) <= 40),
  body        text not null check (char_length(body) between 1 and 500),
  approved    boolean not null default false
);

alter table public.comments enable row level security;

-- visitors (anon) may add a comment, but never an approved one
drop policy if exists "visitors can post" on public.comments;
create policy "visitors can post" on public.comments
  for insert to anon with check (approved = false);

-- visitors only ever see approved comments
drop policy if exists "visitors see approved" on public.comments;
create policy "visitors see approved" on public.comments
  for select to anon using (approved = true);

-- visitors can't edit or delete anything, and can only fill in these columns
revoke all on public.comments from anon, authenticated;
grant select on public.comments to anon;
grant insert (page, path, fx, fy, x, y, name, body) on public.comments to anon;
