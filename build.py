"""
Build orchestration for the Workplace EQ course.

Generates, for all lessons + tests, a source HTML file (uses
shared/theme.css + shared/course-engine.js + shared/supabase-config.js
via <link>/<script src> tags) and a self-contained standalone HTML
file (everything inlined via gen_common.rebuild_standalone()).

Also builds the three "infra" pages — index, glossary, teacher
dashboard — as source + standalone pairs, using a lighter custom page
wrapper (light_page_shell) instead of gen_common.page_shell(), since
those three pages need extra structure (welcome form, search box,
lesson-picker dropdown, ?group= handling) that page_shell()'s fixed
lesson-header skeleton doesn't accommodate.

Run: python3 build.py
"""
import os
import sys
import re

import gen_common
from gen_common import ROOT, FONT_LINK, SUPABASE_CDN, j, rebuild_standalone, page_shell, top_nav

import gen_lesson_template
import gen_test_template

import lessons_section1 as s1
import lessons_section2 as s2
import lessons_section3 as s3
import tests_data

ATTRIBUTION = "Workplace EQ · English Voiced with Kris"

SECTION_MODULES = [s1, s2, s3]
ALL_LESSONS = [l for mod in SECTION_MODULES for l in mod.LESSONS]
ALL_TESTS = tests_data.TESTS

SECTION_META = [
    {"name": "Professional Presence", "theme": "theme-presence", "color": "#1F4543", "accent": "#2E6461",
     "desc": "First impressions, introductions and small talk, then the core skill behind everything else in the course: choosing the right level of politeness and directness for the person in front of you.",
     "expect": "You'll compare three versions of the same line (too blunt, too stiff, just right) and learn why British listeners hear them so differently. Expect situational choices, rewriting blunt lines politely, and short speaking tasks where you introduce yourself and keep a conversation going."},
    {"name": "Communication That Lands", "theme": "theme-communication", "color": "#33375F", "accent": "#4A4F86",
     "desc": "Emails and chat messages, meetings and video calls, and the conversations most people avoid: saying no, apologising, giving feedback and delivering bad news.",
     "expect": "Most of the work here is rewriting: turning a clumsy email into one that gets a reply, softening a disagreement without losing the point, and spotting the faux pas in a message before it's sent. Speaking tasks are short role-plays."},
    {"name": "Career Velocity", "theme": "theme-velocity", "color": "#733B21", "accent": "#9A5230",
     "desc": "Being visible without bragging, managing up, asking for what you want, and networking that actually leads somewhere, then a capstone week-at-work simulation that pulls the whole course together.",
     "expect": "You'll practise the language of self-advocacy (taking credit gracefully, asking for a raise or a stretch project) and then work through a full scenario, from a client dinner to a tricky follow-up email. The final test mixes all seven lessons."},
]


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def lesson_source_filename(lesson):
    # id like "b2c1-lesson-04-academic-hedging" -> "lesson-04-academic-hedging.html"
    m = re.match(r"^weq-(lesson-\d+)-(.+)$", lesson["id"])
    assert m, f"unexpected lesson id shape: {lesson['id']}"
    return f"{m.group(1)}-{m.group(2)}.html"


def lesson_short_prefix(lesson_id):
    m = re.match(r"^weq-(lesson-\d+|test-\d+)", lesson_id)
    assert m, f"unexpected id shape: {lesson_id}"
    return m.group(1)


def lesson_standalone_filename(lesson_id):
    return f"{lesson_short_prefix(lesson_id)}-preview-standalone.html"


def test_source_filename(test):
    slug = slugify(test["title"].split(":", 1)[-1].strip()) if ":" in test["title"] else slugify(test["title"])
    return f"test-{test['num']:02d}-{slug}.html"


# ----------------------------------------------------------------
# Light-weight wrapper for the 3 infra pages (index / glossary /
# teacher-dashboard). These need custom head content (extra inline
# <style> blocks matching the original's per-page tweaks) and don't
# use the fixed lesson-header/course-attribution-inside-shell layout
# that page_shell() bakes in for lesson/test pages -- but they still
# need to end up with the exact same three shared-asset tags so
# rebuild_standalone()'s string replacement works identically.
# ----------------------------------------------------------------
def light_page_shell(*, title, body_html, extra_head="", page_script="", raw=False, nav_html=None):
    """Wrapper for the infra pages (index / glossary / teacher dashboard).
    raw=True: body_html supplies its own nav + layout (the course home).
    Otherwise the page gets the standard bottle-green nav bar and a
    padded content column."""
    if not raw:
        body_html = (nav_html if nav_html is not None else top_nav()) + \
            '\n<main class="shell"><div class="eq-wrap" style="padding-top:40px">\n' + body_html + '\n</div></main>'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<script defer src="/analytics.js"></script>
<title>{title} | Workplace EQ</title>
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
{FONT_LINK}
<link rel="stylesheet" href="shared/theme.css">
{extra_head}
{SUPABASE_CDN}
<script src="shared/supabase-config.js"></script>
</head>
<body>
{body_html}

<script src="shared/course-engine.js"></script>
<script>
{page_script}
</script>
</body>
</html>
'''


# ==================================================================
# LESSONS + TESTS
# ==================================================================
def _extract_total_exercises(script):
    m = re.search(r"totalExercises:\s*(\d+)", script)
    assert m, "could not find totalExercises in generated script"
    return int(m.group(1))


def build_lessons():
    written = []
    totals = {}
    for lesson in ALL_LESSONS:
        body, script = gen_lesson_template.render_lesson(lesson)
        totals[lesson["id"]] = _extract_total_exercises(script)
        html = page_shell(title=lesson["title"], theme_class=lesson["theme_class"], body_html=body, page_script=script)
        src_name = lesson_source_filename(lesson)
        src_path = os.path.join(ROOT, src_name)
        with open(src_path, "w", encoding="utf-8") as f:
            f.write(html)
        standalone_name = lesson_standalone_filename(lesson["id"])
        standalone_path = os.path.join(ROOT, standalone_name)
        rebuild_standalone(src_path, standalone_path)
        written.append((src_name, standalone_name))
    return written, totals


def build_tests():
    written = []
    totals = {}
    for test in ALL_TESTS:
        body, script = gen_test_template.render_test(test)
        totals[test["id"]] = _extract_total_exercises(script)
        # Tests aren't tied to a single lesson's theme_class; use the
        # theme of the section they close out (num N closes section N).
        theme_class = SECTION_META[test["after_section"] - 1]["theme"]
        html = page_shell(title=test["title"], theme_class=theme_class, body_html=body, page_script=script)
        src_name = test_source_filename(test)
        src_path = os.path.join(ROOT, src_name)
        with open(src_path, "w", encoding="utf-8") as f:
            f.write(html)
        standalone_name = lesson_standalone_filename(test["id"])
        standalone_path = os.path.join(ROOT, standalone_name)
        rebuild_standalone(src_path, standalone_path)
        written.append((src_name, standalone_name))
    return written, totals


# ==================================================================
# INDEX PAGE
# Bento layout designed in Claude Design (see design/README.md handoff):
# a wide intro block (hero + progress ring w/ per-section mini bars +
# stats/"Up next"), then one full-width expandable box per section with
# a description, what students will be asked to do, a progress bar, and
# (expanded) the lesson grid with a green tick at 100%. Neutral graphite
# chrome; the four section colours appear only inside the section boxes.
# ==================================================================
def build_index(lesson_totals, preview_available=None, out_path=None):
    """Course home. preview_available=N builds the public preview variant:
    only the first N items open, the rest shown locked, plus a banner and
    a link back to englishvoiced.com/courses/."""
    preview = preview_available is not None
    extra_head = '''<style>
  /* ---------- Course home (design handoff 6b) ---------- */
  .eq-hero{background:var(--green);color:var(--paper)}
  .eq-hero .grid12{padding-top:40px;padding-bottom:44px}
  .hero-t{grid-column:1 / -1;font-stretch:68%;font-weight:800;font-size:clamp(72px,17vw,168px);line-height:.82;letter-spacing:-.02em;text-transform:uppercase;margin:0}
  .hero-t span{color:var(--mint)}
  .hero-tag{grid-column:1 / span 5;margin-top:32px;font-size:22px;font-weight:600;line-height:1.25;text-wrap:pretty}
  .hero-body{grid-column:7 / span 6;margin-top:32px;font-size:16px;line-height:1.6;color:var(--hero-body);text-wrap:pretty}
  .stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-bottom:1px solid var(--ink)}
  .stat{padding:18px 20px;border-right:1px solid var(--ink)}
  .stat:first-child{padding-left:0}
  .stat:last-child{border-right:0;padding-right:0}
  .stat-n{font-stretch:68%;font-weight:800;font-size:64px;line-height:1}
  .stat-l{font-size:13px;font-weight:600}
  #overall-pct{color:var(--green)}
  .name-next{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:20px;padding:24px 0}
  .welcome{display:flex;flex-direction:column;gap:10px;justify-content:center}
  .welcome-copy{font-size:13px;font-weight:600;line-height:1.5}
  .welcome-copy b{font-weight:800}
  .name-form{display:flex}
  .name-form .btn{border-radius:0;padding:0 24px}
  .next-up{text-decoration:none;background:var(--green);color:#fff;padding:16px 20px;display:flex;flex-direction:column;justify-content:space-between;gap:10px;transition:background .15s}
  .next-up:hover{background:var(--bottle)}
  .next-k{font-size:13px;font-weight:600}
  .next-row{display:flex;justify-content:space-between;align-items:flex-end;gap:10px}
  .next-title{font-stretch:75%;font-weight:700;font-size:26px;line-height:1.05}
  .next-go{font-size:28px;line-height:1}
  .preview-banner{border:2px solid var(--ink);padding:14px 18px;font-size:15px;line-height:1.55;display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px 20px;margin:0 0 8px}
  .preview-banner a{color:var(--green);font-weight:700}
  .ltable{padding:16px 0 48px}
  .lrow{display:grid;grid-template-columns:120px minmax(0,1fr) 80px;gap:20px;padding:14px 0;border-bottom:1px solid var(--grey-rule);align-items:baseline;text-decoration:none;color:var(--ink)}
  .lrow.lhead{padding:10px 0;border-bottom:2px solid var(--ink);font-size:12px;font-weight:600;color:var(--grey-label)}
  .lrow.group-end{border-bottom:1px solid var(--ink)}
  .lrow.table-end{border-bottom:2px solid var(--ink)}
  a.lrow:hover .lr-title{color:var(--green)}
  .lr-sec{font-size:13px;font-weight:700;display:flex;flex-direction:column;gap:4px;align-items:flex-start}
  .lr-about{font-size:12px;font-weight:600;color:var(--grey-label);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline;text-underline-offset:2px}
  .lr-about:hover{color:var(--green)}
  .lr-title{font-stretch:80%;font-weight:700;font-size:24px;line-height:1.15;transition:color .15s}
  .lr-title.is-test{color:var(--green)}
  .lr-prog{text-align:right;font-size:14px;color:var(--grey-text)}
  .lr-prog.next{color:var(--green);font-weight:700}
  .lr-prog.done{color:var(--ink);font-weight:700}
  .lrow.locked{cursor:default}
  .lrow.locked .lr-title{opacity:.4}
  .lrow.locked:hover .lr-title{color:var(--ink)}
  .lr-expect{display:none;grid-template-columns:120px minmax(0,1fr) 80px;gap:20px;padding:0 0 16px;border-bottom:1px solid var(--grey-rule);font-size:15px;line-height:1.6;color:var(--text-secondary)}
  .lr-expect.open{display:grid}
  .lr-expect > div{grid-column:2 / span 1}
  .lr-expect p + p{margin-top:8px}
  .lr-sechead{display:none}
  @media (max-width:720px){
    .hero-tag,.hero-body{grid-column:1 / -1}
    .hero-body{margin-top:16px}
    .stats{grid-template-columns:repeat(2,minmax(0,1fr))}
    .stat,.stat:first-child,.stat:last-child{padding:16px 0;border-right:0;border-bottom:1px solid var(--ink)}
    .stat:nth-child(odd){border-right:1px solid var(--ink);padding-right:16px}
    .stat:nth-child(even){padding-left:16px}
    .stat:nth-child(n+3){border-bottom:0}
    .stat-n{font-size:48px}
    .name-next{grid-template-columns:minmax(0,1fr)}
    .lrow,.lr-expect{grid-template-columns:minmax(0,1fr) 64px}
    .lrow .lr-sec{display:none}
    .lrow.lhead span:first-child{display:none}
    .lr-expect > div{grid-column:1 / -1}
    .lr-sechead{display:flex;justify-content:space-between;align-items:baseline;padding:18px 0 6px;font-size:13px;font-weight:700;border-bottom:1px solid var(--grey-rule)}
    .lr-title{font-size:20px}
  }
</style>'''

    n_items = len(ALL_LESSONS) + len(ALL_TESTS)
    home_link = ('<a href="https://englishvoiced.com/courses/">&larr; All courses</a>' if preview
                 else '<a href="https://englishvoiced.com/">English Voiced with Kris</a>')
    banner = ''
    if preview:
        banner = f'''
  <div class="preview-banner">
    <span>This is a <b>free preview</b>. Lesson 1 is fully open; the rest of the course is listed so you can see where it goes.</span>
    <span>Interested in the full course? <a href="https://englishvoiced.com/contact/">Get in touch with Kris</a></span>
  </div>'''
    body_html = f'''<div class="eq-nav"><div class="eq-wrap">
  {home_link}<span>B2–C1</span><span class="eq-hl">Course home</span>
</div></div>
<header class="eq-hero"><div class="eq-wrap grid12">
  <h1 class="hero-t" id="welcome-heading">Workplace<br><span>EQ</span></h1>
  <p class="hero-tag">The unwritten rules of professional presence, communication, and career velocity.</p>
  <p class="hero-body">Your grammar can be perfect and you can still sound rude, cold or junior. This course is about the other half: what British colleagues actually mean, what they expect to hear, and how to say it (with notes on US and international norms along the way).</p>
</div></header>
<main class="eq-wrap">
  <div class="stats">
    <div class="stat"><div class="stat-n">{len(SECTION_META)}</div><div class="stat-l">Sections</div></div>
    <div class="stat"><div class="stat-n">{len(ALL_LESSONS)}</div><div class="stat-l">Lessons</div></div>
    <div class="stat"><div class="stat-n">{len(ALL_TESTS)}</div><div class="stat-l">Test{"" if len(ALL_TESTS) == 1 else "s"}</div></div>
    <div class="stat"><div class="stat-n" id="overall-pct">0%</div><div class="stat-l" id="overall-title">Nothing attempted yet</div></div>
  </div>
  <div class="name-next">
    <div class="welcome" id="welcome-card">
      <div class="welcome-copy" id="welcome-copy">Add your name, so that you can track your progress throughout the course.</div>
      <form class="name-form" id="name-form">
        <input type="text" id="name-input" class="name-input" placeholder="Name" autocomplete="off" aria-label="Your name">
        <button type="submit" class="btn btn-primary">Start</button>
      </form>
    </div>
    <a class="next-up" id="next-up" href="#">
      <span class="next-k" id="next-k">Up next</span>
      <span class="next-row"><span class="next-title" id="next-title">Lesson 1 — {ALL_LESSONS[0]["title"]}</span><span class="next-go" aria-hidden="true">&rarr;</span></span>
    </a>
  </div>{banner}
  <div class="ltable" id="lesson-index"></div>
</main>'''

    entries = []
    for mod in SECTION_MODULES:
        for l in mod.LESSONS:
            entries.append({"id": l["id"], "title": f'Lesson {l["num"]} — {l["title"]}', "isTest": False})
        section_idx = SECTION_MODULES.index(mod)
        for test in ALL_TESTS:
            if test["after_section"] == section_idx + 1:
                entries.append({"id": test["id"], "title": test["title"], "isTest": True})

    short_names = ["Presence", "Communication", "Career"]
    groups_js = [{"title": m["name"], "short": short_names[i] if i < len(short_names) else m["name"],
                  "desc": m["desc"], "expect": m["expect"]} for i, m in enumerate(SECTION_META)]
    section_sizes = [len(mod.LESSONS) + sum(1 for t in ALL_TESTS if t["after_section"] == i + 1) for i, mod in enumerate(SECTION_MODULES)]

    page_script = f'''
const LESSONS = {j(entries)};
const GROUP_META = {j(groups_js)};
const SECTION_SIZES = {j(section_sizes)};
// Public preview: only the first PREVIEW_AVAILABLE items open (null = full course).
const PREVIEW_AVAILABLE = {j(preview_available)};

/* Per-lesson exercise totals, extracted from each generated lesson/test
   file's own totalExercises at build time, so they never drift. */
const DEFAULT_TOTAL = 12;
const LESSON_TOTALS = {j(lesson_totals)};
function totalFor(id){{ return LESSON_TOTALS[id] || DEFAULT_TOTAL; }}

const GROUPS = (() => {{
  let start = 0;
  return GROUP_META.map((g, i) => {{
    const end = start + SECTION_SIZES[i];
    const range = [start, end];
    start = end;
    return {{ ...g, range }};
  }});
}})();

const STUDENT_NAME_KEY = 'workplaceeq_student_name';
const OPEN_KEY = 'workplaceeq_index_open';

const groupParam = new URLSearchParams(window.location.search).get('group');
function withGroup(href){{
  return groupParam ? `${{href}}?group=${{encodeURIComponent(groupParam)}}` : href;
}}
function standaloneFilename(id){{
  const match = id.match(/^weq-(lesson-\\d+|test-\\d+)/);
  const prefix = match ? match[1] : id;
  return `${{prefix}}-preview-standalone.html`;
}}
const isLocked = idx => PREVIEW_AVAILABLE !== null && idx >= PREVIEW_AVAILABLE;

/* ---------- Progress ----------
   Nothing is read until a name exists: the engine's getStudentName()
   would otherwise pop up its own name prompt on top of this page's
   name field (the "asked twice" problem). */
function lessonProgress(id){{
  let attempted = 0;
  if (localStorage.getItem(STUDENT_NAME_KEY)){{
    try {{
      attempted = Course.getCurrentRows(id).filter(r => r.exercise_type === 'auto_graded').length;
    }} catch (e){{ attempted = 0; }}
  }}
  const total = totalFor(id);
  const pct = total ? Math.min(100, Math.round((attempted / total) * 100)) : 0;
  return {{ attempted, total, pct, done: pct >= 100 }};
}}

function readOpen(){{
  try {{ return new Set(JSON.parse(localStorage.getItem(OPEN_KEY)) || []); }}
  catch (e){{ return new Set(); }}
}}
function writeOpen(set){{
  localStorage.setItem(OPEN_KEY, JSON.stringify([...set]));
}}

function rowTitle(l){{
  return l.isTest ? l.title : l.title.replace(/^Lesson\\s+(\\d+)\\s+[—-]\\s*/, '$1 ');
}}

function nextIndex(all){{
  let idx = all.findIndex(p => !p.done);
  if (PREVIEW_AVAILABLE !== null && (idx === -1 || idx >= PREVIEW_AVAILABLE)) idx = Math.min(PREVIEW_AVAILABLE, LESSONS.length) - 1;
  return idx;
}}

function renderLessonIndex(){{
  const root = document.getElementById('lesson-index');
  const open = readOpen();
  const all = LESSONS.map(l => lessonProgress(l.id));
  const nextIdx = nextIndex(all);
  let html = '<div class="lrow lhead"><span>Section</span><span>Lesson</span><span style="text-align:right">Progress</span></div>';

  GROUPS.forEach((g, gi) => {{
    const label = String(gi + 1).padStart(2, '0') + ' ' + g.short;
    const isOpen = open.has(gi);
    const about = `<button type="button" class="lr-about" data-gi="${{gi}}" aria-expanded="${{isOpen}}">${{isOpen ? 'Hide details' : 'What to expect'}}</button>`;
    html += `<div class="lr-sechead"><span>${{label}}</span>${{about}}</div>`;
    for (let idx = g.range[0]; idx < g.range[1]; idx++){{
      const l = LESSONS[idx], p = all[idx];
      const first = idx === g.range[0];
      const last = idx === g.range[1] - 1;
      const cls = ['lrow'];
      if (last) cls.push(gi === GROUPS.length - 1 ? 'table-end' : 'group-end');
      let prog, progCls = 'lr-prog';
      if (isLocked(idx)){{ prog = 'Locked'; cls.push('locked'); }}
      else if (p.done){{ prog = 'Done ✓'; progCls += ' done'; }}
      else if (idx === nextIdx){{ prog = p.attempted ? p.pct + '% · Next' : 'Next'; progCls += ' next'; }}
      else prog = p.pct + '%';
      const sec = first ? `<span class="lr-sec"><span>${{label}}</span>${{about}}</span>` : '<span class="lr-sec"></span>';
      const title = `<span class="lr-title${{l.isTest ? ' is-test' : ''}}">${{rowTitle(l)}}</span>`;
      const inner = `${{sec}}${{title}}<span class="${{progCls}}">${{prog}}</span>`;
      html += isLocked(idx)
        ? `<div class="${{cls.join(' ')}}" title="Not included in this preview">${{inner}}</div>`
        : `<a class="${{cls.join(' ')}}" href="${{withGroup(standaloneFilename(l.id))}}">${{inner}}</a>`;
      if (first){{
        html += `<div class="lr-expect${{isOpen ? ' open' : ''}}" id="expect-${{gi}}"><div><p>${{g.desc}}</p><p>${{g.expect}}</p></div></div>`;
      }}
    }}
  }});
  root.innerHTML = html;

  root.querySelectorAll('.lr-about').forEach(btn => btn.addEventListener('click', (e) => {{
    e.preventDefault(); e.stopPropagation();
    const gi = Number(btn.dataset.gi);
    const set = readOpen();
    if (set.has(gi)) set.delete(gi); else set.add(gi);
    writeOpen(set);
    renderLessonIndex();
  }}));

  renderOverall(all, nextIdx);
}}

function renderOverall(all, nextIdx){{
  const counted = PREVIEW_AVAILABLE === null ? all : all.slice(0, PREVIEW_AVAILABLE);
  const pct = Math.round(counted.reduce((s, p) => s + p.pct, 0) / counted.length);
  const done = counted.filter(p => p.done).length;
  document.getElementById('overall-pct').textContent = pct + '%';
  document.getElementById('overall-title').textContent = done
    ? `${{done}} of ${{counted.length}} finished`
    : (pct ? 'In progress' : 'Nothing attempted yet');

  const next = LESSONS[nextIdx];
  const nextEl = document.getElementById('next-up');
  nextEl.href = withGroup(standaloneFilename(next.id));
  document.getElementById('next-title').textContent = next.title;
  const allDone = counted.every(p => p.done);
  document.getElementById('next-k').textContent = allDone
    ? (PREVIEW_AVAILABLE === null ? 'Course complete · revisit' : 'Preview complete · revisit')
    : (all[nextIdx].attempted ? 'Continue' : 'Up next');
}}

function showWelcomeBack(name){{
  const copy = document.getElementById('welcome-copy');
  copy.innerHTML = '';
  const b = document.createElement('b'); b.textContent = name;
  copy.append('Welcome back, ', b, '. Your progress is saved as you go.');
  const form = document.getElementById('name-form');
  if (form) form.outerHTML = '<button class="change-name-link" id="change-name-btn" style="align-self:flex-start">Not you? Change name</button>';
  document.getElementById('change-name-btn').addEventListener('click', () => {{
    localStorage.removeItem(STUDENT_NAME_KEY);
    location.reload();
  }});
}}

// Pull this student's rows down from Supabase (if connected) so the
// numbers reflect work done on other devices too, then re-render.
function syncAndRender(){{
  if (!localStorage.getItem(STUDENT_NAME_KEY) || !Course.isConnected()) return;
  (async () => {{
    for (const l of LESSONS){{ await Course.syncFromSupabase(l.id); }}
    renderLessonIndex();
  }})();
}}

const existingName = localStorage.getItem(STUDENT_NAME_KEY);
if (existingName){{
  showWelcomeBack(existingName);
}} else {{
  document.getElementById('name-form').addEventListener('submit', (e) => {{
    e.preventDefault();
    const val = document.getElementById('name-input').value.trim();
    if (!val) return;
    localStorage.setItem(STUDENT_NAME_KEY, val);
    showWelcomeBack(val);
    renderLessonIndex();
    syncAndRender();
  }});
}}

renderLessonIndex();
syncAndRender();

// Coming back with the browser's Back button can show a cached copy of
// this page; refresh the numbers whenever it is shown again, and when
// another tab records progress.
window.addEventListener('pageshow', (e) => {{ if (e.persisted){{ renderLessonIndex(); syncAndRender(); }} }});
window.addEventListener('storage', () => renderLessonIndex());
'''

    html = light_page_shell(title="Course home", body_html=body_html, extra_head=extra_head, page_script=page_script, raw=True)
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        return entries
    src_path = os.path.join(ROOT, "index.html")
    with open(src_path, "w", encoding="utf-8") as f:
        f.write(html)
    rebuild_standalone(src_path, os.path.join(ROOT, "index-standalone.html"))
    return entries


# ==================================================================
# GLOSSARY PAGE
# ==================================================================
def build_glossary():
    glossary_nav = top_nav(links_html='<a href="#" id="back-link">&larr; Back to lesson</a><a id="all-lessons-link" href="index-standalone.html">All lessons</a>')
    body_html = '''  <header style="border-bottom:2px solid var(--ink);padding-bottom:18px;margin-bottom:24px">
    <div style="font-size:13px;font-weight:700;color:var(--green);margin-bottom:10px">Personal word list</div>
    <h1 style="font-stretch:68%;font-weight:800;font-size:clamp(48px,8vw,88px);line-height:.88;text-transform:uppercase">My glossary</h1>
    <p id="glossary-sub" style="font-size:17px;margin-top:14px">Loading…</p>
  </header>

  <input type="text" id="search-box" class="search-box" placeholder="Search your saved words…">
  <div id="glossary-root"></div>'''

    page_script = '''
(async function(){
  const groupParam = new URLSearchParams(window.location.search).get('group');
  const fromParam = new URLSearchParams(window.location.search).get('from');
  const backLink = document.getElementById('back-link');
  // 'from' tells us exactly which lesson sent the student here, so this works
  // correctly no matter how many lessons exist -- falls back to Lesson 1 only
  // if the glossary was opened directly, with no lesson context at all.
  let backHref = fromParam || 'lesson-01-preview-standalone.html';
  if (groupParam) backHref += `?group=${encodeURIComponent(groupParam)}`;
  backLink.href = backHref;

  document.getElementById('glossary-sub').textContent = `Syncing, ${Course.getStudentName()}…`;
  await Course.syncGlossaryFromSupabase();
  document.getElementById('glossary-sub').textContent = `${Course.getStudentName()}'s saved words, from every lesson`;

  let allWords = Object.entries(Course.getGlossary()); // [ [wordKey, data], ... ]

  function render(filter){
    const root = document.getElementById('glossary-root');
    const q = (filter || '').trim().toLowerCase();
    const shown = allWords.filter(([key, data]) => !q || data.word.toLowerCase().includes(q) || data.meaning.toLowerCase().includes(q));

    if (!allWords.length){
      root.innerHTML = `<div class="empty-state">No words saved yet.<br>Tap any highlighted word in a lesson's reading passage, then "+ Add to my glossary."</div>`;
      return;
    }
    if (!shown.length){
      root.innerHTML = `<div class="empty-state">No saved words match "${filter}".</div>`;
      return;
    }

    root.innerHTML = '';
    shown.sort((a, b) => a[1].word.localeCompare(b[1].word));
    shown.forEach(([key, data]) => {
      const card = document.createElement('div');
      card.className = 'glossary-card';
      card.innerHTML = `
        <div class="glossary-word-row">
          <div>
            <div class="glossary-word">${data.word}</div>
            <div class="glossary-ipa">${data.ipa || ''}</div>
          </div>
          <div class="glossary-actions">
            <button class="btn btn-sm audio-btn" style="margin-bottom:0" data-speak="${data.word}">Hear it</button>
            <button class="btn btn-sm btn-ghost remove-btn" data-key="${key}">Remove</button>
          </div>
        </div>
        <div class="glossary-meaning">${data.meaning}</div>
        <div class="glossary-example">"${data.example}"</div>
      `;
      card.querySelector('.audio-btn').addEventListener('click', () => Course.speak(data.word));
      card.querySelector('.remove-btn').addEventListener('click', async () => {
        await Course.removeFromGlossary(key);
        allWords = allWords.filter(([k]) => k !== key);
        render(document.getElementById('search-box').value);
      });
      root.appendChild(card);
    });
  }

  render('');
  document.getElementById('search-box').addEventListener('input', (e) => render(e.target.value));
})();
'''
    html = light_page_shell(title="My Glossary", body_html=body_html, page_script=page_script, nav_html=glossary_nav)
    src_path = os.path.join(ROOT, "glossary.html")
    with open(src_path, "w", encoding="utf-8") as f:
        f.write(html)
    rebuild_standalone(src_path, os.path.join(ROOT, "glossary-standalone.html"))


# ==================================================================
# TEACHER DASHBOARD
# ==================================================================
def build_teacher_dashboard(index_entries):
    extra_head = '''<style>
  .shell{max-width:1080px}
</style>'''

    body_html = '''  <header style="border-bottom:2px solid var(--ink);padding-bottom:18px;margin-bottom:8px">
    <div style="font-size:13px;font-weight:700;color:var(--green);margin-bottom:10px">Teacher view</div>
    <h1 id="dash-title" style="font-stretch:68%;font-weight:800;font-size:clamp(44px,7vw,72px);line-height:.9;text-transform:uppercase">Teacher Dashboard</h1>
    <p id="dash-sub" style="font-size:17px;margin-top:12px">Loading…</p>
    <select id="lesson-select" style="margin-top:10px;border:1px solid var(--border-strong);border-radius:var(--radius-pill);padding:8px 16px;font-family:inherit;font-size:13.5px;background:var(--surface);display:none"></select>
  </header>

  <div id="join-prompt" class="join-prompt" style="display:none">
    <p style="margin-bottom:14px;color:var(--text-secondary)">Which group's session do you want to open?</p>
    <input id="join-input" type="text" placeholder="e.g. tues6pm-x7k2p9" style="border:1px solid var(--border-strong);border-radius:8px;padding:9px 14px;font-family:inherit;width:240px;text-align:center">
    <br><button class="btn btn-primary" id="join-btn" style="margin-top:12px">Open dashboard</button>
  </div>

  <div id="dash-body" style="display:none">
    <section class="section">
      <div class="section-label"><span class="num">1</span> Roster &amp; live progress</div>
      <div class="roster" id="roster"></div>
    </section>

    <section class="section">
      <div class="section-label"><span class="num">2</span> Reveal panel — click any answer to override it live</div>
      <div id="reveal-root"></div>
    </section>

    <section class="section">
      <div class="section-label"><span class="num">3</span> Speaking tasks</div>
      <div id="oral-root"></div>
    </section>
  </div>'''

    # LESSONS array for the dashboard: every lesson + test id/title,
    # pulled straight from the authored data (index_entries already has
    # this exact shape) so it can never drift.
    lessons_js = j(index_entries)

    # Section labels/groups mirror the section_id naming scheme used by
    # gen_lesson_template.py / gen_test_template.py.
    section_labels = {}
    for i in range(1, 4):
        section_labels[f"warmup-{i}"] = f"Warm-up {i}"
    for i in range(1, 5):
        section_labels[f"diagnostic-{i}"] = f"Diagnostic {i}"
    for i in range(1, 5):
        section_labels[f"reading-comp-{i}"] = f"Comprehension {i}"
    for i in range(1, 6):
        section_labels[f"vocab-{i}"] = f"Vocab {i}"
    for i in range(1, 6):
        section_labels[f"vocab-gap-{i}"] = f"Vocab gap-fill {i}"
    for i in range(1, 8):
        section_labels[f"practice-gap-{i}"] = f"Gap-fill {i}"
    for i in range(1, 8):
        section_labels[f"practice-err-{i}"] = f"Sentence pair {i}"
    for i in range(1, 12):
        section_labels[f"practice-cat-{i}"] = f"Categorise {i}"
    for i in range(1, 4):
        section_labels[f"practice-builder-{i}"] = f"Sentence builder {i}"
    for i in range(1, 4):
        section_labels[f"listening-{i}"] = f"Listening {i}"
    for i in range(1, 6):
        section_labels[f"exit-{i}"] = f"Exit check {i}"
    for i in range(1, 12):
        section_labels[f"p1-{i}"] = f"Part 1, Q{i}"
        section_labels[f"p1-gap-{i}"] = f"Part 1, Q{i}"
        section_labels[f"p2-{i}"] = f"Part 2, Q{i}"
        section_labels[f"p2-gap-{i}"] = f"Part 2, Q{i}"

    section_groups = [
        {"title": "Warm-up & diagnostic", "prefixes": ["warmup-", "diagnostic-"]},
        {"title": "Reading comprehension", "prefixes": ["reading-comp-"]},
        {"title": "Vocabulary", "prefixes": ["vocab-"]},
        {"title": "Language practice", "prefixes": ["practice-"]},
        {"title": "Listening", "prefixes": ["listening-"]},
        {"title": "Exit check", "prefixes": ["exit-"]},
        {"title": "Test — Part 1", "prefixes": ["p1-"]},
        {"title": "Test — Part 2", "prefixes": ["p2-"]},
    ]

    page_script = f'''
const LESSONS = {lessons_js};
let currentLessonId = LESSONS[0].id;
function currentLessonTitle(){{
  return LESSONS.find(l => l.id === currentLessonId)?.title || currentLessonId;
}}

// Human-readable labels + display order for known sections. Anything not
// listed here still shows up (grouped under "Other"), just unordered --
// so this dashboard never silently hides a new exercise added later.
const SECTION_LABELS = {j(section_labels)};
const SECTION_GROUPS = {j(section_groups)};

function getParam(name){{ return new URLSearchParams(window.location.search).get(name); }}

let supabaseClient = null;
try {{
  if (window.supabase && window.SUPABASE_URL && window.SUPABASE_ANON_KEY){{
    supabaseClient = window.supabase.createClient(window.SUPABASE_URL, window.SUPABASE_ANON_KEY);
  }}
}} catch(e){{ console.error(e); }}

let GROUP_ID = getParam('group');
let allRows = [];       // every lesson_progress row for this group (all lessons)
let studentNames = [];
let absentStudents = new Set(); // local-only for now

function esc(s){{ return (s ?? '').toString().replace(/</g,'&lt;'); }}

/* ---------------- DATA: latest attempt per student+section ---------------- */
function currentRowsFor(lessonId){{
  const rows = allRows.filter(r => r.lesson_id === lessonId);
  const latest = {{}};
  rows.forEach(r => {{
    const key = r.student_name + '::' + r.section_id;
    const existing = latest[key];
    if (!existing || new Date(r.created_at) >= new Date(existing.created_at)) latest[key] = r;
  }});
  return Object.values(latest);
}}

/* ---------------- RENDER: roster ---------------- */
function renderRoster(){{
  const rows = currentRowsFor(currentLessonId).filter(r => r.exercise_type === 'auto_graded');
  const root = document.getElementById('roster');
  root.innerHTML = '';
  studentNames.forEach(name => {{
    const mine = rows.filter(r => r.student_name === name);
    const correct = mine.filter(r => (r.override_correct ?? r.is_correct)).length;
    const card = document.createElement('div');
    card.className = 'roster-card' + (absentStudents.has(name) ? ' absent' : '');
    card.innerHTML = `
      <div class="name">${{esc(name)}}</div>
      <div class="count">${{mine.length}} answered · ${{correct}} correct</div>
      <button class="btn absent-toggle ${{absentStudents.has(name) ? 'btn-primary' : 'btn-ghost'}}" data-name="${{esc(name)}}">
        ${{absentStudents.has(name) ? '✓ Marked absent' : 'Mark absent'}}
      </button>
      <button class="btn btn-ghost wipe-btn" data-name="${{esc(name)}}">Wipe answers</button>
    `;
    card.querySelector('.absent-toggle').addEventListener('click', () => {{
      if (absentStudents.has(name)) absentStudents.delete(name); else absentStudents.add(name);
      renderRoster();
    }});
    card.querySelector('.wipe-btn').addEventListener('click', () => wipeStudent(name));
    root.appendChild(card);
  }});
}}

/* ---------------- WIPE (real, permanent delete) ---------------- */
async function wipeStudent(name){{
  const confirmed = confirm(`Permanently delete ALL of ${{name}}'s answers for "${{currentLessonTitle()}}" from Supabase? This cannot be undone, and does not affect their own device — they'll simply start re-answering from scratch next time they open this lesson.`);
  if (!confirmed) return;
  allRows = allRows.filter(r => !(r.student_name === name && r.lesson_id === currentLessonId)); // optimistic
  renderAll();
  if (!supabaseClient) return;
  const {{ error }} = await supabaseClient.from('lesson_progress').delete()
    .eq('group_id', GROUP_ID).eq('student_name', name).eq('lesson_id', currentLessonId);
  if (error) console.warn('Wipe failed:', error.message);
}}

/* ---------------- RENDER: reveal panel ---------------- */
async function overrideAnswer(row, newValue){{
  row.override_correct = newValue; // optimistic local update
  renderReveal();
  if (!supabaseClient || !row.id) return;
  const {{ error }} = await supabaseClient.from('lesson_progress').update({{ override_correct: newValue }}).eq('id', row.id);
  if (error) console.warn('Override failed to save:', error.message);
}}

function renderReveal(){{
  const rows = currentRowsFor(currentLessonId).filter(r => r.exercise_type === 'auto_graded');
  const bySection = {{}};
  rows.forEach(r => {{ (bySection[r.section_id] = bySection[r.section_id] || []).push(r); }});

  const root = document.getElementById('reveal-root');
  root.innerHTML = '';
  const usedSections = new Set();

  SECTION_GROUPS.forEach(group => {{
    const sectionIds = Object.keys(bySection).filter(sid => group.prefixes.some(p => sid.startsWith(p)));
    if (!sectionIds.length) return;
    sectionIds.sort();
    const wrap = document.createElement('div');
    wrap.className = 'reveal-section';
    wrap.innerHTML = `<div class="reveal-section-title">${{group.title}}</div>`;
    const table = document.createElement('table');
    table.className = 'reveal-table';
    table.innerHTML = `<thead><tr><th>Question</th>${{studentNames.map(n => `<th>${{esc(n)}}</th>`).join('')}}</tr></thead><tbody></tbody>`;
    const tbody = table.querySelector('tbody');
    sectionIds.forEach(sid => {{
      usedSections.add(sid);
      const tr = document.createElement('tr');
      tr.innerHTML = `<td class="section-id">${{SECTION_LABELS[sid] || sid}}</td>`;
      studentNames.forEach(name => {{
        const row = bySection[sid].find(r => r.student_name === name);
        const td = document.createElement('td');
        if (!row){{
          td.innerHTML = `<span class="answer-cell empty">—</span>`;
        }} else {{
          const ok = row.override_correct ?? row.is_correct;
          const wasOverridden = row.override_correct !== null && row.override_correct !== undefined;
          const cell = document.createElement('span');
          cell.className = `answer-cell ${{ok ? 'correct' : 'incorrect'}}${{wasOverridden ? ' revised' : ''}}`;
          cell.innerHTML = `<span>${{ok ? '✓' : '✗'}}</span><span class="txt">${{esc(row.answer_given)}}</span>`;
          cell.title = 'Click to flip correct/incorrect';
          cell.addEventListener('click', () => overrideAnswer(row, !ok));
          td.appendChild(cell);
        }}
        tr.appendChild(td);
      }});
      tbody.appendChild(tr);
    }});
    wrap.appendChild(table);
    root.appendChild(wrap);
  }});

  // Anything not covered by a known group still shows up, so nothing is silently hidden.
  const leftover = Object.keys(bySection).filter(sid => !usedSections.has(sid));
  if (leftover.length){{
    const wrap = document.createElement('div');
    wrap.className = 'reveal-section';
    wrap.innerHTML = `<div class="reveal-section-title">Other</div>`;
    const table = document.createElement('table');
    table.className = 'reveal-table';
    table.innerHTML = `<thead><tr><th>Question</th>${{studentNames.map(n => `<th>${{esc(n)}}</th>`).join('')}}</tr></thead><tbody></tbody>`;
    const tbody = table.querySelector('tbody');
    leftover.sort().forEach(sid => {{
      const tr = document.createElement('tr');
      tr.innerHTML = `<td class="section-id">${{sid}}</td>`;
      studentNames.forEach(name => {{
        const row = bySection[sid].find(r => r.student_name === name);
        const td = document.createElement('td');
        if (!row){{ td.innerHTML = `<span class="answer-cell empty">—</span>`; }}
        else {{
          const ok = row.override_correct ?? row.is_correct;
          const cell = document.createElement('span');
          cell.className = `answer-cell ${{ok ? 'correct' : 'incorrect'}}`;
          cell.innerHTML = `<span>${{ok ? '✓' : '✗'}}</span><span class="txt">${{esc(row.answer_given)}}</span>`;
          cell.addEventListener('click', () => overrideAnswer(row, !ok));
          td.appendChild(cell);
        }}
        tr.appendChild(td);
      }});
      tbody.appendChild(tr);
    }});
    wrap.appendChild(table);
    root.appendChild(wrap);
  }}
}}

/* ---------------- RENDER: oral / discussion picks ---------------- */
async function setVerdict(row, verdict){{
  if (!row.id) return;
  row.teacher_verdict = row.teacher_verdict === verdict ? null : verdict; // click again to clear
  renderOral();
  if (!supabaseClient) return;
  const {{ error }} = await supabaseClient.from('lesson_progress').update({{ teacher_verdict: row.teacher_verdict }}).eq('id', row.id);
  if (error) console.warn('Verdict failed to save:', error.message);
}}

function renderOral(){{
  const rows = currentRowsFor(currentLessonId).filter(r => r.exercise_type === 'oral' && r.status === 'completed');
  const bySection = {{}};
  rows.forEach(r => {{ (bySection[r.section_id] = bySection[r.section_id] || []).push(r); }});

  const root = document.getElementById('oral-root');
  root.innerHTML = '';
  const sectionIds = Object.keys(bySection).sort();
  if (!sectionIds.length){{
    root.innerHTML = `<p style="font-size:13.5px;color:var(--text-tertiary)">No speaking tasks completed yet.</p>`;
    return;
  }}
  sectionIds.forEach(sid => {{
    const picks = bySection[sid];
    const card = document.createElement('div');
    card.className = 'oral-card';
    card.innerHTML = `<div class="oral-q">${{esc(picks[0].answer_given)}}</div>`;
    picks.forEach(row => {{
      const rowEl = document.createElement('div');
      rowEl.className = 'oral-student-row';
      rowEl.innerHTML = `
        <span style="font-size:13.5px;font-weight:550">${{esc(row.student_name)}}</span>
        <span class="verdict-btns">
          <button class="btn verdict-btn pass ${{row.teacher_verdict === 'pass' ? 'on' : ''}}">✓ Pass</button>
          <button class="btn verdict-btn needs ${{row.teacher_verdict === 'needs work' ? 'on' : ''}}">Needs work</button>
        </span>
      `;
      rowEl.querySelector('.pass').addEventListener('click', () => setVerdict(row, 'pass'));
      rowEl.querySelector('.needs').addEventListener('click', () => setVerdict(row, 'needs work'));
      card.appendChild(rowEl);
    }});
    root.appendChild(card);
  }});
}}

function renderAll(){{ renderRoster(); renderReveal(); renderOral(); }}

/* ---------------- LOAD + REALTIME ---------------- */
async function loadGroup(groupId){{
  GROUP_ID = groupId;
  document.getElementById('dash-title').textContent = `Teacher Dashboard — ${{groupId}}`;
  document.getElementById('join-prompt').style.display = 'none';
  document.getElementById('dash-body').style.display = 'block';
  document.getElementById('dash-sub').textContent = `Watching "${{currentLessonTitle()}}" live`;

  const select = document.getElementById('lesson-select');
  select.innerHTML = LESSONS.map(l => `<option value="${{l.id}}">${{l.title}}</option>`).join('');
  select.value = currentLessonId;
  select.style.display = 'inline-block';
  select.addEventListener('change', () => {{
    currentLessonId = select.value;
    document.getElementById('dash-sub').textContent = `Watching "${{currentLessonTitle()}}" live`;
    renderAll();
  }});

  if (!supabaseClient){{
    document.getElementById('dash-sub').textContent = 'Supabase isn\\'t connected — check shared/supabase-config.js.';
    return;
  }}

  const {{ data: groupRow, error: groupErr }} = await supabaseClient.from('groups').select('student_names').eq('group_id', groupId).maybeSingle();
  if (groupErr) console.warn(groupErr.message);
  studentNames = groupRow ? groupRow.student_names : [];

  const {{ data: rows, error: rowsErr }} = await supabaseClient.from('lesson_progress').select('*').eq('group_id', groupId);
  if (rowsErr) console.warn(rowsErr.message);
  allRows = rows || [];
  // students who've answered but aren't (yet) in groups.student_names shouldn't be invisible
  allRows.forEach(r => {{ if (!studentNames.includes(r.student_name)) studentNames.push(r.student_name); }});

  renderAll();

  supabaseClient.channel(`dash-${{groupId}}`)
    .on('postgres_changes', {{ event: '*', schema: 'public', table: 'lesson_progress', filter: `group_id=eq.${{groupId}}` }}, (payload) => {{
      if (payload.eventType === 'DELETE'){{
        // DELETE events only populate payload.old, never payload.new -- easy to
        // miss, and without this branch a wipe from another tab/device would
        // silently fail to disappear from this dashboard until manual reload.
        const oldId = payload.old?.id;
        if (oldId != null) allRows = allRows.filter(r => r.id !== oldId);
        renderAll();
        return;
      }}
      const row = payload.new;
      if (!row) return;
      if (!studentNames.includes(row.student_name)) studentNames.push(row.student_name);
      const idx = allRows.findIndex(r => r.id === row.id);
      if (idx >= 0) allRows[idx] = row; else allRows.push(row);
      renderAll();
    }})
    .on('postgres_changes', {{ event: '*', schema: 'public', table: 'groups', filter: `group_id=eq.${{groupId}}` }}, (payload) => {{
      if (payload.new?.student_names){{
        payload.new.student_names.forEach(n => {{ if (!studentNames.includes(n)) studentNames.push(n); }});
        renderAll();
      }}
    }})
    .subscribe();
}}

if (GROUP_ID){{
  loadGroup(GROUP_ID);
}} else {{
  document.getElementById('join-prompt').style.display = 'block';
  document.getElementById('join-btn').addEventListener('click', () => {{
    const val = document.getElementById('join-input').value.trim();
    if (val){{
      history.replaceState(null, '', `?group=${{encodeURIComponent(val)}}`);
      loadGroup(val);
    }}
  }});
}}
'''

    html = light_page_shell(title="Teacher Dashboard", body_html=body_html, extra_head=extra_head, page_script=page_script)
    src_path = os.path.join(ROOT, "teacher-dashboard.html")
    with open(src_path, "w", encoding="utf-8") as f:
        f.write(html)
    rebuild_standalone(src_path, os.path.join(ROOT, "teacher-dashboard-standalone.html"))



# ==================================================================
# PUBLIC PREVIEW (englishvoiced.com/courses/workplace-eq/)
# ==================================================================
PREVIEW_OPEN_LESSONS = 1


def _preview_fixups(html):
    """Turn a standalone page into its public-preview copy: no Supabase
    backend (browser storage only), links to the preview's index.html,
    and a way back to the /courses/ page from the nav bar."""
    html = re.sub(r"window\.SUPABASE_URL = '[^']*';", "window.SUPABASE_URL = ''; // preview copy: no backend", html)
    html = re.sub(r"window\.SUPABASE_ANON_KEY = '[^']*';", "window.SUPABASE_ANON_KEY = ''; // preview copy: no backend", html)
    html = html.replace("index-standalone.html", "index.html")
    html = html.replace('<span class="eq-nav-links">',
                        '<span class="eq-nav-links"><a href="https://englishvoiced.com/courses/">&larr; All courses</a>', 1)
    return html


def build_preview(out_dir, lesson_totals):
    import shutil
    os.makedirs(out_dir, exist_ok=True)
    tmp_src = os.path.join(ROOT, "_preview-index.html")
    build_index(lesson_totals, preview_available=PREVIEW_OPEN_LESSONS, out_path=tmp_src)
    rebuild_standalone(tmp_src, os.path.join(out_dir, "index.html"))
    os.remove(tmp_src)
    files = ["index.html"]
    for l in ALL_LESSONS[:PREVIEW_OPEN_LESSONS]:
        files.append(lesson_standalone_filename(l["id"]))
        shutil.copy(os.path.join(ROOT, files[-1]), os.path.join(out_dir, files[-1]))
    shutil.copy(os.path.join(ROOT, "glossary-standalone.html"), os.path.join(out_dir, "glossary-standalone.html"))
    files.append("glossary-standalone.html")
    for name in files:
        path = os.path.join(out_dir, name)
        with open(path, encoding="utf-8") as f:
            html = f.read()
        with open(path, "w", encoding="utf-8") as f:
            f.write(_preview_fixups(html))
    os.makedirs(os.path.join(out_dir, "assets"), exist_ok=True)
    for fav in ("favicon-16.png", "favicon-32.png", "favicon-180.png"):
        src = os.path.join(ROOT, "assets", fav)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(out_dir, "assets", fav))
    audio_dir = os.path.join(ROOT, "audio")
    for l in ALL_LESSONS[:PREVIEW_OPEN_LESSONS]:
        prefix = lesson_short_prefix(l["id"])
        for ext in ("mp3", "json"):
            src = os.path.join(audio_dir, f"{prefix}-listening.{ext}")
            if os.path.exists(src):
                os.makedirs(os.path.join(out_dir, "audio"), exist_ok=True)
                shutil.copy(src, os.path.join(out_dir, "audio", os.path.basename(src)))
    # vocab word audio used by the open lessons
    from extract_audio_manifest import slugify_for_audio
    for l in ALL_LESSONS[:PREVIEW_OPEN_LESSONS]:
        for entry in l["reading"]["vocab_data"].values():
            src = os.path.join(audio_dir, "vocab", slugify_for_audio(entry["word"]) + ".mp3")
            if os.path.exists(src):
                os.makedirs(os.path.join(out_dir, "audio", "vocab"), exist_ok=True)
                shutil.copy(src, os.path.join(out_dir, "audio", "vocab", os.path.basename(src)))
    print(f"Preview written to {out_dir} ({len(files)} pages).")


def main():
    lesson_files, lesson_totals = build_lessons()
    test_files, test_totals = build_tests()
    all_totals = {**lesson_totals, **test_totals}
    index_entries = build_index(all_totals)
    build_glossary()
    build_teacher_dashboard(index_entries)
    if "--preview" in sys.argv:
        build_preview(sys.argv[sys.argv.index("--preview") + 1], all_totals)

    total_lesson_test_files = len(lesson_files) * 2 + len(test_files) * 2
    infra_files = 6
    print(f"Built {len(lesson_files)} lessons + {len(test_files)} tests "
          f"({total_lesson_test_files} files) + {infra_files} infra files "
          f"= {total_lesson_test_files + infra_files} files total.")


if __name__ == "__main__":
    main()
