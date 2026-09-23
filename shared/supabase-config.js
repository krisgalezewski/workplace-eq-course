/* ============================================================
   Supabase project config for the English+ B2+/C1 Companion Course.
   Reuses the SAME Supabase project as the original B1+/B2 course
   (per the handoff's open-decision recommendation — simplest option,
   no known downside since the schema partitions by lesson_id +
   group_id, and this course's lesson ids are all distinct strings
   like "b2c1-lesson-01-..." that can never collide with the
   original course's "lesson-01-..." ids).
   The anon key is safe to be public — access is controlled by the
   RLS policies in supabase/schema.sql, not by keeping this key secret.
   ============================================================ */
window.SUPABASE_URL = 'https://ovosqztjtnvasbaursnh.supabase.co';
window.SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im92b3NxenRqdG52YXNiYXVyc25oIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc0ODcxNzcsImV4cCI6MjEwMzA2MzE3N30.I5yzw18Jd2-AgCqLxbkS3CioeUb3kFBjby8dcKUmvoM';
