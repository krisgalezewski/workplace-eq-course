"""
English+ course overview page (index) — 2026 redesign.

Shared by every English+ course: build.py (or build_index.py) passes the
course's own data and gets back the three pieces its page shell needs:

    extra_head, body_html, page_script = overview.render(cfg)

cfg keys
  top_line        mono line at the very top ("English+ … · by Kris Galezewski")
  labels          [solid chip, outlined chip, level chip] e.g. ["English+", "Function Words I", "B1+/B2"]
  heading         hero H1
  intro           hero paragraph (HTML allowed)
  hero_art        decorative word-chip cluster (HTML), or ""
  entries         [{id, title, isTest, chips:[[text, kind]]}] in course order; kind: s/o/x/d
  groups          [{title, color, deep, desc, expect, size}] — size = items in the section
  lesson_totals   {id: auto-graded exercises}  (a lesson is 100% once this many are attempted)
  name_key        localStorage key for the student's name (keep the course's existing key!)
  closed_key      localStorage key for collapsed sections
  file_prefix_re  JS regex source matching the short file prefix, e.g. "(lesson-\\d+|test-\\d+)"
  id_prefix       optional id prefix stripped before matching (e.g. "fw1-")
"""
import json


def _j(x):
    return json.dumps(x, ensure_ascii=False)


EXTRA_HEAD = '''<style>
  /* ---------- Course overview (2026 redesign) ---------- */
  body .shell{max-width:none !important;padding:0 !important}
  .course-attribution{display:none !important}
  .ov{min-height:100vh;padding-bottom:80px}
  .ov-hero{background-color:var(--accent);background-image:var(--dots);background-size:20px 20px;color:var(--cream)}
  .ov-top{max-width:1180px;margin:0 auto;padding:22px 28px 0;display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
  .ov-topline{font-family:var(--font-mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;opacity:.85}
  .ov-hero-grid{max-width:1180px;margin:0 auto;padding:48px 28px 64px;display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:48px;align-items:center}
  .ov-left{display:flex;flex-direction:column;gap:22px;min-width:0}
  .ov-labels{display:flex;gap:8px;flex-wrap:wrap}
  .ov-label{font-family:var(--font-display);font-weight:700;font-size:15px;padding:5px 12px;border-radius:9px;background:rgba(0,0,0,.18);color:var(--cream)}
  .ov-label.s{font-weight:800;background:var(--cream);color:var(--accent)}
  .ov-label.o{padding:4px 12px;border-radius:999px;background:none;border:1.5px solid rgba(246,238,221,.7)}
  .ov-hero h1{margin:0;color:var(--cream);font-family:var(--font-display);font-weight:900;font-size:clamp(40px,5.4vw,68px);line-height:.98;letter-spacing:-.02em;text-wrap:balance}
  .ov-intro{margin:0;font-size:18px;line-height:1.6;max-width:560px;color:var(--cream);text-wrap:pretty}
  .ov-intro b,.ov-intro strong{color:var(--cream)}
  .ov-start{display:flex;flex-direction:column;gap:10px}
  .ov-start-note{font-size:15px;opacity:.9}
  .ov-hello{font-family:var(--font-display);font-weight:700;font-size:20px;line-height:1.35}
  .ov-hello .change-name-link{display:block;font-family:var(--font-sans);font-weight:500;font-size:14px;margin-top:8px;color:var(--cream)}
  .ov-right{display:flex;flex-direction:column;gap:18px;min-width:0}
  .ov-art{display:flex;flex-direction:column;gap:10px;align-items:flex-end;font-family:var(--font-display);font-weight:800}
  .ov-card{background:var(--cream);color:var(--ink);border-radius:24px;padding:24px;display:flex;flex-direction:column;gap:18px}
  .ov-ring-row{display:flex;gap:18px;align-items:center}
  .ov-ring{width:84px;height:84px;border-radius:50%;flex:none;display:grid;place-items:center;background:conic-gradient(var(--accent) var(--pct,0%),#E4DACB 0)}
  .ov-ring > span{width:64px;height:64px;border-radius:50%;background:var(--cream);display:flex;align-items:center;justify-content:center;font-family:var(--font-display);font-weight:800;font-size:20px;white-space:nowrap}
  .ov-ring-t{font-family:var(--font-display);font-weight:800;font-size:19px}
  .ov-ring-s{font-size:15px;color:var(--text-secondary)}
  .ov-stats{display:grid;grid-template-columns:repeat(3,1fr);border-top:1.5px solid #E4DACB;border-bottom:1.5px solid #E4DACB}
  .ov-stats > div{padding:14px 0}
  .ov-stat-n{font-family:var(--font-display);font-weight:900;font-size:30px;line-height:1.1}
  .ov-stat-l{font-family:var(--font-mono);font-size:11px;letter-spacing:.12em;color:var(--text-secondary);text-transform:uppercase}
  .ov-next{display:flex;justify-content:space-between;align-items:center;gap:16px;text-align:left;padding:16px 18px;border-radius:16px;background:var(--accent);color:var(--cream);text-decoration:none;transition:background .15s}
  .ov-next:hover{background:var(--accent-dark);color:var(--cream)}
  .ov-next-k{display:block;font-family:var(--font-mono);font-size:11px;letter-spacing:.14em;opacity:.8;text-transform:uppercase}
  .ov-next-t{display:block;font-family:var(--font-display);font-weight:800;font-size:18px;line-height:1.2;margin-top:4px}
  .ov-next-a{font-size:24px;flex:none}

  .ov-secs{max-width:1180px;margin:0 auto;padding:56px 28px 0;display:flex;flex-direction:column;gap:56px}
  .ov-sec{display:flex;flex-direction:column;gap:22px}
  .ov-sec-head{display:grid;grid-template-columns:auto minmax(0,1fr);gap:22px;align-items:start}
  .ov-sec-n{font-family:var(--font-display);font-weight:900;font-size:64px;line-height:.85;letter-spacing:-.03em}
  .ov-sec-body{display:flex;flex-direction:column;gap:10px}
  .ov-sec-row{display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
  .ov-sec-row h2{margin:0;font-family:var(--font-display);font-weight:800;font-size:32px;letter-spacing:-.01em;line-height:1.1}
  .ov-sec-meta{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
  .ov-sec-count{font-family:var(--font-mono);font-size:13px}
  .ov-toggle{padding:7px 14px;border-radius:999px;border:1.5px solid;background:transparent;font-weight:600;font-size:14px;cursor:pointer;font-family:inherit}
  .ov-toggle:hover{background:rgba(0,0,0,.04)}
  .ov-lead{margin:0;font-size:18px;line-height:1.55;color:var(--ink);max-width:780px;text-wrap:pretty}
  .ov-body{margin:0;font-size:15px;line-height:1.6;color:var(--text-secondary);max-width:780px;text-wrap:pretty}
  .ov-tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
  .ov-sec.closed .ov-tiles{display:none}
  .ov-tile{min-height:200px;display:flex;flex-direction:column;justify-content:space-between;gap:20px;text-align:left;padding:20px;border-radius:22px;
    background-image:var(--dots-sm);background-size:18px 18px;color:var(--cream);text-decoration:none;transition:transform .15s}
  .ov-tile:hover{transform:translateY(-3px);color:var(--cream)}
  .ov-tile-chips{display:flex;gap:6px;flex-wrap:wrap;font-family:var(--font-display);font-weight:800}
  .ov-tile-chips .rd-chip{font-size:17px;padding:4px 11px;border-radius:9px}
  .ov-tile-foot{display:flex;flex-direction:column;gap:6px}
  .ov-tile-k{display:flex;justify-content:space-between;gap:10px;font-family:var(--font-mono);font-size:11px;letter-spacing:.14em;opacity:.85;text-transform:uppercase}
  .ov-tile-t{font-family:var(--font-display);font-weight:800;font-size:19px;line-height:1.2;text-wrap:balance}
  .ov-tile.done .ov-tile-k span:last-child{opacity:1;font-weight:600}

  /* Free preview on englishvoiced.com/courses/ (body[data-preview-open]) */
  .ov-tile.locked{opacity:.45;filter:grayscale(.3);cursor:pointer}
  .ov-tile.locked:hover{transform:none;opacity:.7}
  .ov-tile.locked.flagged{opacity:1;filter:none;outline:3px solid var(--ink);outline-offset:2px}
  .ov-preview{display:flex;flex-direction:column;gap:12px}
  .ov-banner,.ov-locked{padding:16px 20px;border-radius:18px;font-size:15px;line-height:1.55;color:var(--text-body)}
  .ov-banner{background:var(--cream);display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px}
  .ov-locked{background:#fff;border:2px solid var(--accent)}
  .ov-locked[hidden]{display:none}
  .ov-banner b,.ov-locked b{color:var(--ink)}
  .ov-banner a,.ov-locked a{color:var(--accent);font-weight:700}
  .ov-back{color:var(--cream);text-decoration:none;font-family:var(--font-mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;margin-right:14px}
  .ov-back:hover{color:var(--cream);text-decoration:underline}

  @media (max-width:640px){
    .ov-top{padding:16px 16px 0}
    .ov-hero-grid{padding:36px 16px 44px;gap:32px;grid-template-columns:minmax(0,1fr)}
    .ov-art{align-items:flex-start}
    .ov-art > div{justify-content:flex-start !important}
    .ov-secs{padding:44px 16px 0;gap:44px}
    .ov-sec-head{grid-template-columns:minmax(0,1fr);gap:8px}
    .ov-sec-n{font-size:48px}
    .ov-sec-row h2{font-size:26px}
    .ov-card{padding:20px}
  }
</style>'''

BODY = '''<div class="ov">
  <div class="ov-hero">
    <div class="ov-top">
      <div class="ov-topline">__TOP__</div>
      <a class="rd-pill" id="glossary-link" href="glossary-standalone.html">My glossary&nbsp;·&nbsp;<span id="glossary-count">0</span></a>
    </div>
    <div class="ov-hero-grid">
      <div class="ov-left">
        <div class="ov-labels">__LABELS__</div>
        <h1 id="welcome-heading">__HEADING__</h1>
        <p class="ov-intro" id="welcome-copy">__INTRO__</p>
        <div class="ov-start" id="welcome-start">
          <div class="ov-start-note">Add your name, so that you can track your progress throughout the course.</div>
          <form class="name-form" id="name-form">
            <input type="text" id="name-input" class="name-input" placeholder="Your name" autocomplete="off" aria-label="Your name">
            <button type="submit" class="btn btn-primary">Start &rarr;</button>
          </form>
        </div>
      </div>
      <div class="ov-right">
        __ART__
        <div class="ov-card">
          <div class="ov-ring-row">
            <div class="ov-ring" id="overall-ring"><span id="overall-pct">0%</span></div>
            <div>
              <div class="ov-ring-t" id="overall-title">Nothing attempted yet</div>
              <div class="ov-ring-s" id="overall-sub">Your progress across all __N__ items.</div>
            </div>
          </div>
          <div class="ov-stats">
            <div><div class="ov-stat-n">__NSEC__</div><div class="ov-stat-l">Sections</div></div>
            <div><div class="ov-stat-n">__NLES__</div><div class="ov-stat-l">Lessons</div></div>
            <div><div class="ov-stat-n">__NTEST__</div><div class="ov-stat-l">Tests</div></div>
          </div>
          <a class="ov-next" id="next-up" href="#">
            <span><span class="ov-next-k" id="next-kicker">Up next</span><span class="ov-next-t" id="next-title"></span></span>
            <span class="ov-next-a" aria-hidden="true">&rarr;</span>
          </a>
        </div>
      </div>
    </div>
  </div>
  <div class="ov-secs" id="lesson-index"></div>
</div>'''

SCRIPT = r'''
const OV = __CFG__;
// Free preview (englishvoiced.com/courses/): build_preview.py sets
// data-preview-open / -contact / -course on <body>. Only the first N
// lessons ship; the rest are listed, faded and locked.
const PV = (() => { const d = document.body.dataset; return d.previewOpen ? { open: Number(d.previewOpen), contact: d.previewContact || '/contact/', course: d.previewCourse || '' } : null; })();
let FLAGGED_IDX = null;
const LESSONS = OV.entries;
const LESSON_TOTALS = OV.lessonTotals;
const DEFAULT_TOTAL = 12;
function totalFor(id){ return LESSON_TOTALS[id] || DEFAULT_TOTAL; }
const GROUPS = (() => { let s = 0; return OV.groups.map(g => { const r = [s, s + g.size]; s += g.size; return { ...g, range: r }; }); })();

const STUDENT_NAME_KEY = OV.nameKey;
const CLOSED_KEY = OV.closedKey;
const groupParam = new URLSearchParams(window.location.search).get('group');
function withGroup(href){ return groupParam ? `${href}?group=${encodeURIComponent(groupParam)}` : href; }
const FILE_RE = new RegExp('^' + (OV.idPrefix || '') + OV.filePrefixRe);
function standaloneFilename(id){
  const m = id.match(FILE_RE);
  return `${m ? m[1] : id}-preview-standalone.html`;
}
function esc(s){ return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }

/* ---------- Progress ---------- */
function lessonProgress(id){
  if (!localStorage.getItem(STUDENT_NAME_KEY)) return { attempted: 0, total: totalFor(id), pct: 0, done: false };
  let attempted = 0;
  try { attempted = Course.getCurrentRows(id).filter(r => r.exercise_type === 'auto_graded').length; } catch (e){ attempted = 0; }
  const total = totalFor(id);
  const pct = total ? Math.min(100, Math.round((attempted / total) * 100)) : 0;
  return { attempted, total, pct, done: pct >= 100 };
}
function readClosed(){ try { return new Set(JSON.parse(localStorage.getItem(CLOSED_KEY)) || []); } catch (e){ return new Set(); } }
function writeClosed(set){ try { localStorage.setItem(CLOSED_KEY, JSON.stringify([...set])); } catch (e){} }

// Lesson / test numbering straight from course order.
const NUMS = (() => { let l = 0, t = 0; return LESSONS.map(x => x.isTest ? { test: true, n: ++t } : { test: false, n: ++l }); })();
function shortTitle(l){ return l.isTest ? l.title : l.title.replace(/^Lesson\s+\d+\s+[—–-]\s*/, ''); }
function kicker(i){ const k = NUMS[i]; return k.test ? 'Test ' + k.n : 'Lesson ' + String(k.n).padStart(2, '0'); }
function chip(c, color){
  const [t, k] = c;
  return `<span class="rd-chip ${k || 's'}" style="--chip-on:${color}">${esc(t)}</span>`;
}

function renderLessonIndex(){
  const root = document.getElementById('lesson-index');
  const closed = readClosed();
  root.innerHTML = '';
  GROUPS.forEach((g, gi) => {
    const items = LESSONS.slice(g.range[0], g.range[1]);
    const progress = items.map(l => lessonProgress(l.id));
    const doneCount = progress.filter(p => p.done).length;
    const lessonCount = items.filter(l => !l.isTest).length;
    const testCount = items.length - lessonCount;
    const isClosed = closed.has(gi);
    const tiles = items.map((l, i) => {
      const idx = g.range[0] + i, p = progress[i];
      if (PV && idx >= PV.open){
        return `<div class="ov-tile locked${idx === FLAGGED_IDX ? ' flagged' : ''}" data-locked="${idx}" role="button" tabindex="0" title="Not included in this preview — contact Kris for the full course" style="background-color:${l.isTest ? g.deep : g.color}">
          <span class="ov-tile-chips">${(l.chips || []).map(c => chip(c, l.isTest ? g.deep : g.color)).join('')}</span>
          <span class="ov-tile-foot">
            <span class="ov-tile-k"><span>${kicker(idx)}</span><span>Full course</span></span>
            <span class="ov-tile-t">${esc(shortTitle(l))}</span>
          </span>
        </div>`;
      }
      const status = p.done ? '✓ Done' : (p.attempted ? p.pct + '%' : (l.isTest ? 'Mixed review' : ''));
      const chips = (l.chips || []).map(c => chip(c, l.isTest ? g.deep : g.color)).join('');
      return `<a class="ov-tile${p.done ? ' done' : ''}" href="${withGroup(standaloneFilename(l.id))}" style="background-color:${l.isTest ? g.deep : g.color}">
          <span class="ov-tile-chips">${chips}</span>
          <span class="ov-tile-foot">
            <span class="ov-tile-k"><span>${kicker(idx)}</span><span>${status}</span></span>
            <span class="ov-tile-t">${esc(shortTitle(l))}</span>
          </span>
        </a>`;
    }).join('');
    const sec = document.createElement('section');
    sec.className = 'ov-sec' + (isClosed ? ' closed' : '');
    sec.innerHTML = `
      <div class="ov-sec-head">
        <div class="ov-sec-n" style="color:${g.color}">${String(gi + 1).padStart(2, '0')}</div>
        <div class="ov-sec-body">
          <div class="ov-sec-row">
            <h2 style="color:${g.color}">${g.title}</h2>
            <div class="ov-sec-meta">
              <span class="ov-sec-count" style="color:${g.color}">${lessonCount} lesson${lessonCount === 1 ? '' : 's'}${testCount ? ` · ${testCount} test${testCount === 1 ? '' : 's'}` : ''} · ${doneCount}/${items.length} done</span>
              <button class="ov-toggle" type="button" style="border-color:${g.color};color:${g.color}" aria-expanded="${!isClosed}">${isClosed ? 'Show lessons' : 'Hide lessons'}</button>
            </div>
          </div>
          <p class="ov-lead">${g.desc}</p>
          <p class="ov-body">${g.expect}</p>
        </div>
      </div>
      <div class="ov-tiles">${tiles}</div>`;
    sec.querySelector('.ov-toggle').addEventListener('click', (e) => {
      const set = readClosed();
      if (set.has(gi)) set.delete(gi); else set.add(gi);
      writeClosed(set);
      const nowClosed = set.has(gi);
      sec.classList.toggle('closed', nowClosed);
      e.currentTarget.textContent = nowClosed ? 'Show lessons' : 'Hide lessons';
      e.currentTarget.setAttribute('aria-expanded', String(!nowClosed));
    });
    root.appendChild(sec);
  });
  renderOverall();
}

function renderOverall(){
  const all = LESSONS.map(l => lessonProgress(l.id));
  const pct = Math.round(all.reduce((s, p) => s + p.pct, 0) / all.length);
  const done = all.filter(p => p.done).length;
  document.getElementById('overall-ring').style.setProperty('--pct', pct + '%');
  document.getElementById('overall-pct').textContent = pct + '%';
  document.getElementById('overall-title').textContent = done ? `${done} of ${all.length} finished` : (pct ? 'In progress' : 'Nothing attempted yet');
  document.getElementById('overall-sub').textContent = 'Your progress across all ' + all.length + ' items.';
  let nextIdx = all.findIndex(p => !p.done);
  if (PV && (nextIdx === -1 || nextIdx >= PV.open)) nextIdx = all.slice(0, PV.open).every(p => p.done) ? -1 : PV.open - 1;
  const i = nextIdx === -1 ? (PV ? PV.open - 1 : LESSONS.length - 1) : nextIdx;
  const next = LESSONS[i];
  const nextEl = document.getElementById('next-up');
  nextEl.href = withGroup(standaloneFilename(next.id));
  document.getElementById('next-kicker').textContent = nextIdx === -1 ? (PV ? 'Preview complete · revisit' : 'Course complete · revisit') : ((all[i].attempted ? 'Continue · ' : 'Up next · ') + kicker(i));
  document.getElementById('next-title').textContent = shortTitle(next);
  try { document.getElementById('glossary-count').textContent = Object.keys(Course.getGlossary() || {}).length; } catch (e){}
}

function showWelcomeBack(name){
  const start = document.getElementById('welcome-start');
  start.outerHTML = `<div class="ov-hello" id="welcome-hello">Good to see you, ${esc(name)}. Your progress is saved on this device.<button class="change-name-link" id="change-name-btn" type="button">Not you? Change name</button></div>`;
  document.getElementById('change-name-btn').addEventListener('click', () => {
    localStorage.removeItem(STUDENT_NAME_KEY);
    location.reload();
  });
}

const glossaryLink = document.getElementById('glossary-link');
if (glossaryLink && groupParam) glossaryLink.href = `glossary-standalone.html?group=${encodeURIComponent(groupParam)}`;

const existingName = localStorage.getItem(STUDENT_NAME_KEY);
if (existingName){
  showWelcomeBack(existingName);
} else {
  document.getElementById('name-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const val = document.getElementById('name-input').value.trim();
    if (!val) return;
    localStorage.setItem(STUDENT_NAME_KEY, val);
    showWelcomeBack(val);
    renderLessonIndex();
    syncIndexFromSupabase();
  });
}

if (PV){
  const secs = document.getElementById('lesson-index');
  const n = PV.open;
  const openTxt = n === 1 ? 'Lesson 1 is' : `Lessons 1&ndash;${n} are`;
  const onlyTxt = n === 1 ? 'Lesson 1 only' : `Lessons 1&ndash;${n} only`;
  const box = document.createElement('div');
  box.className = 'ov-preview';
  box.innerHTML = `<div class="ov-banner"><span>This is a <b>free preview</b> &mdash; ${openTxt} fully open below; the rest of the syllabus is shown so you can see where the course goes, but isn't unlocked here.</span>`
    + `<span><b>Contact Kris</b> if you're interested in the full course &mdash; <a href="${PV.contact}">get in touch</a></span></div>`
    + `<div class="ov-locked" id="locked-notice" role="status" hidden></div>`;
  secs.before(box);
  box.style.cssText = 'max-width:1180px;margin:0 auto;padding:40px 28px 0';
  const top = document.querySelector('.ov-top');
  if (top){ const a = document.createElement('a'); a.className = 'ov-back'; a.href = '/courses/'; a.innerHTML = '&larr; All courses'; top.firstElementChild.prepend(a); }
  window.showLockedNotice = function(idx, scroll){
    const l = LESSONS[idx];
    const note = document.getElementById('locked-notice');
    if (!l || !note) return;
    FLAGGED_IDX = idx;
    note.innerHTML = `<b>${esc(l.title)}</b> is part of the full ${PV.course} course. This free preview includes ${onlyTxt}. Want access to the whole course? <a href="${PV.contact}">Get in touch with Kris</a>.`;
    note.hidden = false;
    const gi = GROUPS.findIndex(g => idx >= g.range[0] && idx < g.range[1]);
    if (gi !== -1){ const set = readClosed(); set.delete(gi); writeClosed(set); }
    renderLessonIndex();
    if (scroll !== false) note.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };
  secs.addEventListener('click', e => { const t = e.target.closest('[data-locked]'); if (t){ e.preventDefault(); showLockedNotice(Number(t.dataset.locked)); } });
  secs.addEventListener('keydown', e => { const t = e.target.closest('[data-locked]'); if (t && (e.key === 'Enter' || e.key === ' ')){ e.preventDefault(); showLockedNotice(Number(t.dataset.locked)); } });
}

renderLessonIndex();

if (PV){
  const n = parseInt(new URLSearchParams(location.search).get('locked'), 10);
  if (n >= 1){ let c = 0; const idx = LESSONS.findIndex(l => !l.isTest && ++c === n); if (idx >= PV.open) showLockedNotice(idx); }
}

// Pull this student's rows from Supabase (if connected) so ticks and
// percentages include other devices, then re-render once.
function syncIndexFromSupabase(){
  if (!localStorage.getItem(STUDENT_NAME_KEY) || !Course.isConnected()) return;
  (async () => {
    for (const l of LESSONS){ await Course.syncFromSupabase(l.id); }
    try { await Course.syncGlossaryFromSupabase(); } catch (e){}
    renderLessonIndex();
  })();
}
syncIndexFromSupabase();

window.addEventListener('pageshow', (e) => { if (e.persisted){ renderLessonIndex(); syncIndexFromSupabase(); } });
window.addEventListener('storage', () => renderLessonIndex());
'''


def render(cfg):
    labels = cfg["labels"]
    labels_html = (f'<span class="ov-label s">{labels[0]}</span>'
                   f'<span class="ov-label o">{labels[1]}</span>'
                   f'<span class="ov-label">{labels[2]}</span>')
    entries = cfg["entries"]
    n_tests = sum(1 for e in entries if e["isTest"])
    body = (BODY.replace("__TOP__", cfg["top_line"])
                .replace("__LABELS__", labels_html)
                .replace("__HEADING__", cfg["heading"])
                .replace("__INTRO__", cfg["intro"])
                .replace("__ART__", cfg.get("hero_art") or "")
                .replace("__N__", str(len(entries)))
                .replace("__NSEC__", str(len(cfg["groups"])))
                .replace("__NLES__", str(len(entries) - n_tests))
                .replace("__NTEST__", str(n_tests)))
    js_cfg = {
        "entries": [{"id": e["id"], "title": e["title"], "isTest": bool(e["isTest"]), "chips": e.get("chips", [])} for e in entries],
        "groups": cfg["groups"],
        "lessonTotals": cfg["lesson_totals"],
        "nameKey": cfg["name_key"],
        "closedKey": cfg["closed_key"],
        "filePrefixRe": cfg["file_prefix_re"],
        "idPrefix": cfg.get("id_prefix", ""),
    }
    assert sum(g["size"] for g in cfg["groups"]) == len(entries), "group sizes must add up to the entries"
    script = SCRIPT.replace("__CFG__", json.dumps(js_cfg, ensure_ascii=False, indent=1))
    return EXTRA_HEAD, body, script
