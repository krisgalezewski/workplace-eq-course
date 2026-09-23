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
import re

import gen_common
from gen_common import ROOT, FONT_LINK, SUPABASE_CDN, j, rebuild_standalone, page_shell

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
def light_page_shell(*, title, body_html, extra_head="", page_script=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Workplace EQ</title>
{FONT_LINK}
<link rel="stylesheet" href="shared/theme.css">
{extra_head}
{SUPABASE_CDN}
<script src="shared/supabase-config.js"></script>
</head>
<body>

<div class="course-attribution">{ATTRIBUTION}</div>
<div class="shell">
{body_html}
</div>

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
def build_index(lesson_totals):
    extra_head = '''<style>

  /* ---------- Index bento layout ---------- */
  /* The index isn't inside any one section, so it stays clear of the
     four section colours; it uses a neutral graphite accent instead, so
     the coloured boxes below are the only colour signal on the page. */
  body{--accent:#2F343C;--accent-dark:#1B2430;--accent-soft:#EDEFF2;--accent-soft-border:#C2C8D0;--bg:#F5F6F7}
  .shell{max-width:1060px}

  .intro-grid{
    display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);gap:12px;margin-bottom:12px;
  }
  .bx{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-lg)}

  .intro-hero{padding:34px 34px 30px;display:flex;flex-direction:column;gap:16px}
  .intro-eyebrow{
    font-size:11.5px;font-weight:650;letter-spacing:.12em;text-transform:uppercase;color:var(--text-tertiary);
  }
  .intro-hero h1{
    font-family:var(--font-serif);font-weight:600;font-size:40px;line-height:1.08;
    letter-spacing:-0.02em;color:#1B2430;text-wrap:pretty;
  }
  .intro-hero p{font-size:14.5px;line-height:1.65;color:var(--text-secondary);max-width:52ch}
  .intro-hero .name-form{justify-content:flex-start;margin:0;max-width:420px}
  .intro-side{display:grid;grid-template-columns:minmax(0,1fr);gap:12px;align-content:stretch}

  .ring-cell{min-width:0;padding:22px 24px;display:flex;flex-direction:column;justify-content:center;gap:18px}
  .ring-top{display:flex;align-items:center;gap:18px}
  .mini-list{display:flex;flex-direction:column;gap:9px}
  .mini{display:flex;align-items:center;gap:10px;font-size:11.5px;font-weight:600;min-width:0}
  .mini-idx{font-family:var(--font-mono);font-size:10.5px;opacity:.7;flex-shrink:0}
  .mini-name{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .mini-bar{width:74px;height:4px;border-radius:999px;background:rgba(27,36,48,.10);overflow:hidden;flex-shrink:0}
  .mini-bar > i{display:block;height:100%;border-radius:999px}
  .mini-pct{font-family:var(--font-mono);font-size:10.5px;color:var(--text-tertiary);width:30px;text-align:right;flex-shrink:0}
  .ring{
    width:88px;height:88px;border-radius:50%;flex-shrink:0;
    display:flex;align-items:center;justify-content:center;
    background:conic-gradient(var(--accent) var(--pct,0%), var(--surface-alt) 0);
  }
  .ring > span{
    width:66px;height:66px;border-radius:50%;background:var(--surface);
    display:flex;align-items:center;justify-content:center;
    font-size:17px;font-weight:650;letter-spacing:-0.02em;
  }
  .ring-label{font-size:13px;line-height:1.5;color:var(--text-secondary)}
  .ring-label b{display:block;font-size:14.5px;color:var(--text);margin-bottom:2px}

  .stat-cell{min-width:0;padding:20px 24px;display:flex;flex-direction:column;justify-content:center;gap:18px}
  .stat-row{display:flex;gap:26px;flex-wrap:wrap}
  .stat-row > div{min-width:0}
  .next-up{
    display:flex;flex-direction:column;gap:5px;text-decoration:none;
    border-top:1px solid var(--border);padding-top:15px;
  }
  .next-title{font-size:14px;font-weight:600;line-height:1.4;color:var(--text);text-wrap:pretty}
  .next-go{font-size:12px;font-weight:650;color:var(--accent)}
  .next-up:hover .next-go{text-decoration:underline}
  .stat-n{font-family:var(--font-serif);font-size:26px;font-weight:600;line-height:1;letter-spacing:-0.02em;color:var(--text)}
  .stat-l{font-size:11px;font-weight:650;letter-spacing:.08em;text-transform:uppercase;color:var(--text-tertiary);margin-top:5px}

  /* ---------- Section boxes ---------- */
  .bento-sections{display:flex;flex-direction:column;gap:12px}
  .sec-box{
    border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden;
    display:flex;flex-direction:column;transition:box-shadow .18s;
  }
  .sec-head{
    width:100%;text-align:left;font-family:inherit;border:none;cursor:pointer;background:none;
    padding:24px 26px;display:flex;flex-direction:column;gap:12px;color:inherit;
  }
  .sec-top{display:flex;align-items:flex-start;gap:14px}
  .sec-idx{
    font-family:var(--font-mono);font-size:11.5px;letter-spacing:.06em;padding-top:5px;opacity:.65;flex-shrink:0;
  }
  .sec-title{font-size:20px;font-weight:650;letter-spacing:-0.015em;line-height:1.25;flex:1;min-width:0}
  .sec-chev{font-size:20px;line-height:1;flex-shrink:0;padding-top:2px;transition:transform .2s}
  .sec-toggle{
    display:inline-flex;align-items:center;padding:3px 10px;border-radius:999px;
    border:1px solid;font-size:11.5px;font-weight:650;letter-spacing:.02em;white-space:nowrap;
  }
  .sec-box.open .sec-chev{transform:rotate(180deg)}
  .sec-desc{font-size:14.5px;line-height:1.6;color:var(--text-secondary);text-wrap:pretty;max-width:88ch}
  .sec-expect{font-size:13px;line-height:1.65;color:var(--text-secondary);text-wrap:pretty;max-width:88ch}
  .sec-foot{display:flex;align-items:center;gap:12px;font-size:12px;font-weight:600;letter-spacing:.02em}
  .sec-bar{flex:1;height:5px;border-radius:999px;background:rgba(27,36,48,.10);overflow:hidden;min-width:60px}
  .sec-bar > i{display:block;height:100%;border-radius:999px;transition:width .4s}
  .sec-done{
    display:inline-flex;align-items:center;gap:5px;padding:3px 9px;border-radius:999px;
    background:var(--ok-bg);border:1px solid var(--ok-border);color:var(--ok);font-size:11.5px;font-weight:650;
  }

  .sec-body{display:none;padding:0 14px 14px}
  .sec-box.open .sec-body{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:6px}
  .lx{
    display:flex;align-items:center;gap:11px;padding:11px 13px;border-radius:var(--radius-md);
    text-decoration:none;font-size:14px;background:var(--surface);border:1px solid var(--border);transition:all .12s;
  }
  .lx:hover{transform:translateY(-1px)}
  .lx-num{
    flex-shrink:0;width:25px;height:25px;border-radius:50%;display:flex;align-items:center;justify-content:center;
    font-size:11.5px;font-weight:650;
  }
  .lx-title{flex:1;min-width:0;font-weight:550;line-height:1.35}
  .lx-state{flex-shrink:0;font-family:var(--font-mono);font-size:11px;color:var(--text-tertiary)}
  .lx-tick{
    flex-shrink:0;width:19px;height:19px;border-radius:50%;background:var(--ok);color:#fff;
    display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;
  }

  @media (max-width:820px){
    .intro-grid{grid-template-columns:minmax(0,1fr)}
    .intro-hero h1{font-size:31px}
  }

</style>'''

    body_html = '''  <div class="intro-grid">
    <div class="bx intro-hero" id="welcome-card">
      <div class="intro-eyebrow">English Voiced with Kris &middot; B2&ndash;C1</div>
      <h1 id="welcome-heading">Workplace EQ</h1>
      <p id="welcome-copy"><b>The unwritten rules of professional presence, communication, and career velocity.</b> Your grammar can be perfect and you can still sound rude, cold or junior. This course is about the other half: what British colleagues actually mean, what they expect to hear, and how to say it (with notes on US and international norms along the way).<br>Add your name, so that you can track your progress throughout the course.</p>
      <form class="name-form" id="name-form">
        <input type="text" id="name-input" class="name-input" placeholder="Your name" autocomplete="off">
        <button type="submit" class="btn btn-primary">Start</button>
      </form>
    </div>

    <div class="intro-side">
      <div class="bx ring-cell">
        <div class="ring-top">
          <div class="ring" id="overall-ring"><span id="overall-pct">0%</span></div>
          <div class="ring-label"><b id="overall-title">Nothing attempted yet</b><span id="overall-sub">Your progress across all {N_ITEMS} items.</span></div>
        </div>
        <div class="mini-list" id="mini-progress"></div>
      </div>
      <div class="bx stat-cell">
        <div class="stat-row">
          <div><div class="stat-n">{N_SECTIONS}</div><div class="stat-l">Sections</div></div>
          <div><div class="stat-n">{N_LESSONS}</div><div class="stat-l">Lessons</div></div>
          <div><div class="stat-n">{N_TESTS}</div><div class="stat-l">Test{TEST_PLURAL}</div></div>
        </div>
        <a class="next-up" id="next-up" href="#">
          <span class="stat-l" style="margin:0">Up next</span>
          <span class="next-title" id="next-title">{FIRST_TITLE}</span>
          <span class="next-go">Open lesson &rarr;</span>
        </a>
      </div>
    </div>
  </div>

  <div id="lesson-index" class="bento-sections"></div>'''
    body_html = (body_html.replace("{N_ITEMS}", str(len(ALL_LESSONS) + len(ALL_TESTS)))
        .replace("{N_SECTIONS}", str(len(SECTION_META))).replace("{N_LESSONS}", str(len(ALL_LESSONS)))
        .replace("{N_TESTS}", str(len(ALL_TESTS))).replace("{TEST_PLURAL}", "" if len(ALL_TESTS) == 1 else "s")
        .replace("{FIRST_TITLE}", f'Lesson 1 — {ALL_LESSONS[0]["title"]}'))

    # Build the LESSONS array (id + title + isTest) directly from the
    # authored data so the index page can never drift from the actual
    # lessons_section*.py / tests_data.py content.
    entries = []
    for mod in SECTION_MODULES:
        for l in mod.LESSONS:
            entries.append({"id": l["id"], "title": f'Lesson {l["num"]} — {l["title"]}', "isTest": False})
        # the test that closes this section comes right after its lessons
        section_idx = SECTION_MODULES.index(mod)
        for test in ALL_TESTS:
            if test["after_section"] == section_idx + 1:
                entries.append({"id": test["id"], "title": test["title"], "isTest": True})

    groups_js = [{"title": m["name"], "color": m["color"], "accent": m["accent"], "desc": m["desc"], "expect": m["expect"]} for m in SECTION_META]
    section_sizes = [len(mod.LESSONS) + sum(1 for t in ALL_TESTS if t["after_section"] == i + 1) for i, mod in enumerate(SECTION_MODULES)]

    # Real per-item exercise totals, extracted from each generated
    # lesson/test's own `totalExercises` value — never hand-maintained,
    # so it can't drift out of sync with the actual content.
    lessons_js = j(entries)
    groups_meta_js = j(groups_js)
    lesson_totals_js = j(lesson_totals)

    page_script = f'''
const LESSONS = {lessons_js};
const GROUP_META = {groups_meta_js};
const SECTION_SIZES = {j(section_sizes)};

/* ------------------------------------------------------------------
   Per-lesson exercise totals — the same number each lesson/test file
   passes as `totalExercises` to Course.initSummary(). A lesson counts
   as 100% complete (and gets its green tick) once this many auto-graded
   exercises have been attempted. Extracted directly from the generated
   lesson/test files at build time (see build.py), so it's always in
   sync with the actual content.
   ------------------------------------------------------------------ */
const DEFAULT_TOTAL = 12;
const LESSON_TOTALS = {lesson_totals_js};
function totalFor(id){{ return LESSON_TOTALS[id] || DEFAULT_TOTAL; }}

// Build the [start, end) ranges from SECTION_SIZES so this never has to
// be hand-kept in sync with LESSONS.length.
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
  // Standalone files are named with just the short prefix (lesson-01,
  // test-01), never the full descriptive id.
  const match = id.match(/^weq-(lesson-\\d+|test-\\d+)/);
  const prefix = match ? match[1] : id;
  return `${{prefix}}-preview-standalone.html`;
}}

/* ---------- Progress ---------- */
function lessonProgress(id){{
  let attempted = 0;
  try {{
    attempted = Course.getCurrentRows(id).filter(r => r.exercise_type === 'auto_graded').length;
  }} catch (e){{ attempted = 0; }}
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

function shortTitle(l){{
  // "Lesson 4 — Academic Hedging: ..." → "Academic Hedging: ..." (the
  // number already lives in the numbered badge beside it). Tests keep
  // their full label.
  return l.isTest ? l.title : l.title.replace(/^Lesson\\s+\\d+\\s+[—-]\\s*/, '');
}}

function renderLessonIndex(){{
  const root = document.getElementById('lesson-index');
  const open = readOpen();
  root.innerHTML = '';

  GROUPS.forEach((g, gi) => {{
    const items = LESSONS.slice(g.range[0], g.range[1]);
    const progress = items.map(l => lessonProgress(l.id));
    const doneCount = progress.filter(p => p.done).length;
    const pct = Math.round(progress.reduce((s, p) => s + p.pct, 0) / items.length);
    const lessonCount = items.filter(l => !l.isTest).length;
    const testCount = items.length - lessonCount;
    const isOpen = open.has(gi);

    const rows = items.map((l, i) => {{
      const p = progress[i];
      const testNo = LESSONS.slice(0, g.range[0] + i + 1).filter(x => x.isTest).length;
      const num = l.isTest ? 'T' + testNo : (g.range[0] + i + 1 - LESSONS.slice(0, g.range[0] + i).filter(x => x.isTest).length);
      const state = p.done
        ? '<span class="lx-tick" title="Completed">✓</span>'
        : `<span class="lx-state">${{p.attempted ? p.pct + '%' : ''}}</span>`;
      return `
        <a class="lx" href="${{withGroup(standaloneFilename(l.id))}}"
           style="border-color:${{g.color}}26;background:${{l.isTest ? g.color + '0F' : 'var(--surface)'}}"
           onmouseover="this.style.background='${{g.color}}1A'"
           onmouseout="this.style.background='${{l.isTest ? g.color + '0F' : '#fff'}}'">
          <span class="lx-num" style="${{l.isTest ? 'background:' + g.color + ';color:#fff' : 'background:' + g.color + '1F;color:' + g.color}}">${{num}}</span>
          <span class="lx-title" style="color:${{g.color}}">${{shortTitle(l)}}</span>
          ${{state}}
        </a>`;
    }}).join('');

    const box = document.createElement('div');
    box.className = 'sec-box' + (isOpen ? ' open' : '');
    box.style.background = g.color + '0A';
    box.style.borderColor = g.color + '33';
    box.innerHTML = `
      <button class="sec-head" aria-expanded="${{isOpen}}">
        <div class="sec-top">
          <span class="sec-idx" style="color:${{g.color}}">0${{gi + 1}}</span>
          <span class="sec-title" style="color:${{g.color}}">${{g.title}}</span>
          <span class="sec-chev" style="color:${{g.color}}">&#9662;</span>
        </div>
        <div class="sec-desc">${{g.desc}}</div>
        <div class="sec-expect">${{g.expect}}</div>
        <div class="sec-foot" style="color:${{g.color}}">
          <span>${{lessonCount}} lessons · ${{testCount}} test${{testCount === 1 ? '' : 's'}}</span>
          <span class="sec-bar"><i style="width:${{pct}}%;background:${{g.accent}}"></i></span>
          <span class="sec-toggle" style="border-color:${{g.color}}40;color:${{g.color}}">${{isOpen ? 'Hide lessons' : 'Show lessons'}}</span>
          ${{doneCount === items.length
            ? '<span class="sec-done">✓ Section complete</span>'
            : `<span>${{doneCount}}/${{items.length}} done</span>`}}
        </div>
      </button>
      <div class="sec-body">${{rows}}</div>`;

    box.querySelector('.sec-head').addEventListener('click', () => {{
      const set = readOpen();
      if (set.has(gi)) set.delete(gi); else set.add(gi);
      writeOpen(set);
      const nowOpen = set.has(gi);
      box.classList.toggle('open', nowOpen);
      box.querySelector('.sec-head').setAttribute('aria-expanded', String(nowOpen));
      box.querySelector('.sec-toggle').textContent = nowOpen ? 'Hide lessons' : 'Show lessons';
    }});

    root.appendChild(box);
  }});

  renderOverall();
}}

function renderOverall(){{
  const all = LESSONS.map(l => lessonProgress(l.id));
  const pct = Math.round(all.reduce((s, p) => s + p.pct, 0) / all.length);
  const done = all.filter(p => p.done).length;
  const ring = document.getElementById('overall-ring');
  ring.style.setProperty('--pct', pct + '%');
  document.getElementById('overall-pct').textContent = pct + '%';
  document.getElementById('overall-title').textContent = done
    ? `${{done}} of ${{all.length}} finished`
    : (pct ? 'In progress' : 'Nothing attempted yet');
  document.getElementById('overall-sub').textContent = 'Your progress across all ' + all.length + ' items.';

  // Per-section mini bars, so the cell says which part of the course is
  // moving rather than just the single overall number.
  document.getElementById('mini-progress').innerHTML = GROUPS.map((g, gi) => {{
    const items = LESSONS.slice(g.range[0], g.range[1]).map(l => lessonProgress(l.id));
    const p = Math.round(items.reduce((s, x) => s + x.pct, 0) / items.length);
    return `<div class="mini">
      <span class="mini-idx" style="color:${{g.color}}">0${{gi + 1}}</span>
      <span class="mini-name" style="color:${{g.color}}">${{g.title}}</span>
      <span class="mini-bar"><i style="width:${{p}}%;background:${{g.accent}}"></i></span>
      <span class="mini-pct">${{p}}%</span>
    </div>`;
  }}).join('');

  // Up next: first item that isn't finished.
  const nextIdx = all.findIndex(p => !p.done);
  const next = LESSONS[nextIdx === -1 ? LESSONS.length - 1 : nextIdx];
  const nextEl = document.getElementById('next-up');
  nextEl.href = withGroup(standaloneFilename(next.id));
  document.getElementById('next-title').textContent = next.title;
  nextEl.querySelector('.next-go').textContent = nextIdx === -1
    ? 'Course complete — revisit →'
    : (all[nextIdx].attempted ? 'Continue →' : 'Open →');
}}

function showWelcomeBack(name){{
  document.getElementById('welcome-heading').textContent = 'Welcome back, ' + name + '.';
  document.getElementById('welcome-copy').innerHTML =
    'Continuing <b>Workplace EQ</b> — the unwritten rules of professional presence, communication, and career velocity.';
  const form = document.getElementById('name-form');
  form.outerHTML = '<button class="change-name-link" id="change-name-btn" style="align-self:flex-start;margin:0">Not you? Change name</button>';
  document.getElementById('change-name-btn').addEventListener('click', () => {{
    localStorage.removeItem(STUDENT_NAME_KEY);
    location.reload();
  }});
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
  }});
}}

renderLessonIndex();

// Pull this student's rows down from Supabase (if connected) so the ticks
// and percentages reflect work done on other devices too, then re-render
// once. Never blocks first paint; a failure just leaves local numbers.
if (existingName && Course.isConnected()){{
  (async () => {{
    for (const l of LESSONS){{ await Course.syncFromSupabase(l.id); }}
    renderLessonIndex();
  }})();
}}
'''

    html = light_page_shell(title="Course home", body_html=body_html, extra_head=extra_head, page_script=page_script)
    src_path = os.path.join(ROOT, "index.html")
    with open(src_path, "w", encoding="utf-8") as f:
        f.write(html)
    rebuild_standalone(src_path, os.path.join(ROOT, "index-standalone.html"))
    return entries


# ==================================================================
# GLOSSARY PAGE
# ==================================================================
def build_glossary():
    body_html = '''  <header class="lesson-header">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap">
      <div class="lesson-eyebrow">\U0001f4d6 Personal word list</div>
      <a href="#" id="back-link" class="pill" style="text-decoration:none;font-size:12.5px">← Back to lesson</a>
    </div>
    <h1 class="lesson-title">My Glossary</h1>
    <p class="lesson-sub" id="glossary-sub">Loading…</p>
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
            <button class="btn btn-sm audio-btn" style="margin-bottom:0" data-speak="${data.word}">\U0001f50a</button>
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
    html = light_page_shell(title="My Glossary", body_html=body_html, page_script=page_script)
    src_path = os.path.join(ROOT, "glossary.html")
    with open(src_path, "w", encoding="utf-8") as f:
        f.write(html)
    rebuild_standalone(src_path, os.path.join(ROOT, "glossary-standalone.html"))


# ==================================================================
# TEACHER DASHBOARD
# ==================================================================
def build_teacher_dashboard(index_entries):
    extra_head = '''<style>
  .shell{max-width:920px}
</style>'''

    body_html = '''  <header class="lesson-header">
    <div class="lesson-eyebrow">\U0001f469‍\U0001f3eb Teacher view</div>
    <h1 class="lesson-title" id="dash-title">Teacher Dashboard</h1>
    <p class="lesson-sub" id="dash-sub">Loading…</p>
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
      <button class="btn btn-ghost wipe-btn" data-name="${{esc(name)}}">\U0001f5d1 Wipe answers</button>
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


def main():
    lesson_files, lesson_totals = build_lessons()
    test_files, test_totals = build_tests()
    all_totals = {**lesson_totals, **test_totals}
    index_entries = build_index(all_totals)
    build_glossary()
    build_teacher_dashboard(index_entries)

    total_lesson_test_files = len(lesson_files) * 2 + len(test_files) * 2
    infra_files = 6
    print(f"Built {len(lesson_files)} lessons + {len(test_files)} tests "
          f"({total_lesson_test_files} files) + {infra_files} infra files "
          f"= {total_lesson_test_files + infra_files} files total.")


if __name__ == "__main__":
    main()
