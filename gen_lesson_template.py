"""
Renders one lesson (a Python dict of content) into the standard
HTML skeleton + JS driver script.

Section order: warm-up -> quick check -> concept (browse/quiz widget,
full rules, tone cells, culture notes) -> reading (vocab + key-phrase
highlighting) -> vocabulary check -> practice (gap-fill, faux-pas
spotter, sentence builder) -> speaking (solo/group) -> listening
(Anna & Tomasz) -> wrap-up exit check + score summary.

Visual system: Workplace EQ "Annual Report · Bottle" reskin (see
shared/theme.css). Every element id the engine wires is unchanged.
"""
import re

from gen_common import nav_header, j
from culture_notes import CULTURE

TOTAL_LESSONS = 7


def vocab(key, text):
    return f'<span class="vocab" data-word="{key}">{text}</span>'


def gram(key, text):
    return f'<span class="gram" data-gram="{key}">{text}</span>'


# ------------------------------------------------------------------
# Tip / rules post-processing: every 💡/🎯/🌍 box becomes a
# "Key finding" row (label column + text column), and emoji become
# text labels, per the design handoff.
# ------------------------------------------------------------------
def key_finding(text, label="Key finding"):
    return f'<div class="kf"><span class="kf-l">{label}</span><div class="kf-t">{text}</div></div>'


def _box_to_kf(m):
    inner = m.group("inner").strip()
    label = "Key finding"
    lm = re.match(r"^<b>([^<]+?):</b>\s*", inner)
    if lm:
        label = lm.group(1).strip()
        inner = inner[lm.end():]
    return key_finding(inner, label)


def restyle_rules(html):
    # drop the "Elsewhere" box: its content now lives in the culture columns
    html = re.sub(r'<div class="tip-box"[^>]*>\s*🌍.*?</span></div>', "", html, flags=re.S)
    # warn-box: <div class="warn-box"><span>🎯</span><span ...>TEXT</span></div>
    html = re.sub(
        r'<div class="warn-box">\s*<span>🎯</span>\s*<span[^>]*>(?P<inner>.*?)</span>\s*</div>',
        _box_to_kf, html, flags=re.S)
    # tip-box with a leading emoji
    html = re.sub(
        r'<div class="tip-box"[^>]*>\s*\S+\s*<span[^>]*>(?P<inner>.*?)</span></div>',
        _box_to_kf, html, flags=re.S)
    # inside explanatory text (after a line break or an arrow) the marks
    # become small "Use" / "Avoid" labels; at the start of a formula line
    # they are simply dropped.
    html = re.sub(r"(<br>\s*|→\s*)✅\s*", r'\1<span class="lab-yes">Use</span>', html)
    html = re.sub(r"(<br>\s*|→\s*|^|>\s*)❌\s*", r'\1<span class="lab-no">Avoid</span>', html)
    html = html.replace("✅ ", "").replace("✅", "")
    return html


def _mcq_block(prefix, i, q):
    n = len(q["options"])
    cls = "opts opts-3" if n == 3 else "opts"
    opts = "".join(f'<button class="opt" data-value="{o["value"]}">{o["label"]}</button>' for o in q["options"])
    return f'''
      <div class="q-block">
        <p class="q-text">{q["prompt"]}</p>
        <div class="{cls}" id="{prefix}-q{i+1}">{opts}</div>
      </div>'''


def _gap_box(prefix, label, items, default_width):
    rows = "".join(
        f'''
        <div class="gap-row">
          <p class="gap-s">{g["before"]} <input type="text" id="{prefix}{i+1}-input" aria-label="Gap {i+1}" autocomplete="off" style="width:{max(g.get("width", default_width), 120)}px"> {g.get("after", "")}</p>
          <button class="btn btn-sm" id="{prefix}{i+1}-check">Check</button>
          <div id="{prefix}{i+1}-fb"></div>
        </div>'''
        for i, g in enumerate(items)
    )
    return f'<div class="gapbox"><div class="gap-label">{label}</div>{rows}</div>'


def _section(sid, num, title, inner, sub=""):
    sub_html = f'<div class="sec-sub">{sub}</div>' if sub else ""
    return f'''
  <section class="section eq-sec" id="{sid}">
    <div class="sec-num">{num:02d}</div>
    <div class="sec-body">
      <h2 class="sec-h">{title}</h2>{sub_html}
      {inner}
    </div>
  </section>'''


def _tone_label_kind(label):
    l = label.lower()
    if "right" in l:
        return "right"
    if "blunt" in l:
        return "blunt"
    return "stiff"


def render_lesson(d):
    lesson_id = d["id"]
    header = nav_header(f'Lesson {d["num"]} of {TOTAL_LESSONS}', d["title"], d["subtitle"],
                        section_name=d["section_name"])

    warmup_qs = "".join(_mcq_block("warm", i, q) for i, q in enumerate(d["warmup"]))
    diag_qs = "".join(_mcq_block("diag", i, q) for i, q in enumerate(d["diagnostic"]))

    widget = d["widget"]
    tabs_html = "".join(
        f'<button class="pill{" on" if i == 0 else ""}" id="mode-w-{t["key"]}">{t["label"]}</button>'
        for i, t in enumerate(widget["tabs"])
    )

    # ---------- tone cells + culture notes ----------
    tone_html = ""
    if d.get("compare"):
        c = d["compare"]
        tone_html = f'''
      <div class="card">
        <div class="sec-sub-h">{c["title"]}</div>
        <p class="tone-hint" style="margin:8px 0 14px">Hover over (or tap) each line to see how a British listener is likely to hear it.</p>
        <div id="compare-card"></div>
      </div>'''
    culture = CULTURE.get(d["num"])
    culture_html = ""
    if culture:
        cols = "".join(f'<div><div class="culture-h">{h}</div>{t}</div>' for h, t in culture)
        culture_html = f'<div class="culture">{cols}</div>'

    concept_inner = f'''
    <p style="font-size:17px;line-height:1.6">{widget["intro"]}</p>
    <div class="mode-toggle mode-toggle-outline">{tabs_html}</div>
    <div id="widget-area"></div>
    <p id="widget-hint">Click either cell to see another example.</p>
    <button class="pill align-start" id="rules-toggle">Show the full rules</button>
    <div class="expand-content" id="rules-content">
      <div>
        {restyle_rules(widget["rules_html"])}
      </div>
    </div>
    {tone_html}
    {culture_html}'''
    concept_html = _section("sec-concept", 3, widget["heading"], concept_inner, sub="The concept")

    passage_paragraphs = "".join(f"<p>{p}</p>" for p in d["reading"]["passage_paragraphs"])
    reading_comp_qs = "".join(_mcq_block("comp", i, q) for i, q in enumerate(d["reading"]["comprehension"]))
    reading_inner = f'''
    <button class="pill align-start" id="gram-toggle">Show key phrases in this text</button>
    <div class="passage" id="passage">{passage_paragraphs}</div>
    <p class="tone-hint">Tap a highlighted word for pronunciation, meaning and an example. With key phrases on, tap a highlighted phrase to see why it works (and what a less skilful speaker might have said).</p>
    <div class="card">
      <h3 style="margin-bottom:16px">Did you follow it?</h3>
      {reading_comp_qs}
    </div>'''
    reading_html = _section("sec-reading", 4, d["reading"]["heading"], reading_inner, sub="Reading")

    vocab_match_html = "".join(_mcq_block("vocab", i, q) for i, q in enumerate(d["vocab_check"]["match"]))
    vocab_inner = f'''
    <p style="font-size:17px">The key words from the text, in mixed formats.</p>
    <div class="card"><h4 style="margin-bottom:14px">Match the meaning</h4>{vocab_match_html}</div>
    {_gap_box("vgap", "Complete the sentence · vocabulary", d["vocab_check"]["gapfill"], 160)}'''
    vocab_html = _section("sec-vocab", 5, "Vocabulary", vocab_inner)

    practice = d["practice"]
    second_widget = practice["second"]
    if second_widget["type"] == "categorise":
        second_html = f'''
    <div class="card">
      <h3 style="margin-bottom:6px">{second_widget["title"]}</h3>
      <p style="font-size:15px;margin-bottom:16px">{second_widget["instruction"]}</p>
      <div id="cat-root"></div>
    </div>'''
    else:
        sentences_html = "".join(
            f'''
      <div style="font-size:13px;font-weight:700;{"" if i == 0 else "padding-top:16px;border-top:1px solid var(--grey-rule);"}margin-bottom:8px">Sentence {i+1}</div>
      <div id="err{i+1}" style="line-height:2;margin-bottom:18px"></div>'''
            for i in range(len(second_widget["items"]))
        )
        second_html = f'''
    <div class="card">
      <h3 style="margin-bottom:6px">{second_widget["title"]}</h3>
      <p style="font-size:15px;margin-bottom:16px">{second_widget["instruction"]}</p>
      {sentences_html}
    </div>'''

    practice_inner = f'''
    {_gap_box("gap", "Gap-fill · " + practice["gapfill_focus"], practice["gapfill"], 170)}
    {second_html}
    <div class="card">
      <h3 style="margin-bottom:6px">Sentence builder</h3>
      <p style="font-size:15px;margin-bottom:14px">Tap the words in the right order. Three rounds.</p>
      <div id="builders"></div>
    </div>'''
    practice_html = _section("sec-practice", 6, "Practice", practice_inner)

    speaking_inner = f'''
    <div class="mode-toggle">
      <button class="pill on" id="mode-solo">Solo</button>
      <button class="pill" id="mode-group">Group (2–4)</button>
    </div>
    <div class="task-card" id="speak-solo">
      <div class="kicker">60-second task</div>
      <p>{d["speaking"]["solo_text"]}</p>
      <button class="btn btn-sm" id="solo-done-btn" style="margin-top:16px">I've done this</button>
    </div>
    <div class="task-card" id="speak-group" style="display:none">
      <div class="kicker">Discussion · pick 1–2 questions to answer out loud</div>
      <p style="margin-bottom:14px">Tap the question(s) you'll answer. Your teacher will see your pick and mark it after you speak.</p>
      <div id="discuss-questions" style="display:flex;flex-direction:column;gap:8px"></div>
      <p id="discuss-limit-msg" class="tone-hint" style="margin-top:10px">You can select up to 2 questions.</p>
    </div>'''
    speaking_html = _section("sec-speaking", 7, "Speaking", speaking_inner)

    listen_comp_qs = "".join(_mcq_block("listen", i, q) for i, q in enumerate(d["listening"]["comprehension"]))
    listening_inner = f'''
    <p style="font-size:17px">{d["listening"]["intro"]}</p>
    <audio id="dialogue-audio" preload="none" style="display:none"></audio>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <button class="btn btn-primary" id="play-dialogue">Play dialogue</button>
      <button class="btn btn-sm" id="stop-dialogue">Stop</button>
      <button class="btn btn-ghost btn-sm" id="show-transcript">Show full transcript</button>
    </div>
    <div id="transcript"></div>
    <div class="card" style="margin-top:8px">{listen_comp_qs}</div>'''
    listening_html = _section("sec-listening", 8, "Listening", listening_inner)

    exit_qs = "".join(_mcq_block("exit", i, q) for i, q in enumerate(d["exit"]))
    wrapup_inner = f'''
    <div class="card" style="border-top:0;padding-top:0">{exit_qs}</div>
    <div class="card" id="summary-card">
      <h3 style="margin-bottom:14px">Your lesson summary</h3>
      <div style="display:flex;align-items:center;gap:20px;margin-bottom:18px" id="summary-ring-row">
        <div id="score-ring-holder"></div>
        <div>
          <div id="summary-name">—</div>
          <div style="font-size:15px;margin-top:4px" id="summary-completion"></div>
          <div style="font-size:15px;color:var(--text-secondary);margin-top:4px" id="summary-weak">Finish the lesson to see your results.</div>
        </div>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <button class="btn btn-primary" id="finish-btn">Finish lesson &amp; see results</button>
        <button class="btn" id="export-btn" style="display:none">Export PDF report</button>
      </div>
    </div>'''
    wrapup_html = _section("sec-wrapup", 9, "Wrap-up", wrapup_inner, sub="Exit check")

    warmup_inner = f'''
    <p style="font-size:17px;line-height:1.6">{d["warmup_intro"]}</p>
    {warmup_qs}
    {key_finding(d["warmup_tip"])}'''
    diag_inner = f'''
    <p style="font-size:17px;line-height:1.6">Four quick questions before we explain anything. This isn't graded harshly — it just shows us where to focus.</p>
    {diag_qs}'''

    body = "\n".join([
        header,
        '<main class="shell">',
        _section("sec-warmup", 1, "Warm-up", warmup_inner),
        _section("sec-diagnostic", 2, "Quick check", diag_inner),
        concept_html,
        reading_html,
        vocab_html,
        practice_html,
        speaking_html,
        listening_html,
        wrapup_html,
        '</main>',
    ])

    # ---------- JS driver ----------
    tab_ids_js = j([{"id": f'mode-w-{t["key"]}', "key": t["key"]} for t in widget["tabs"]])
    categories_js = j(widget["categories"])
    quiz_labels_js = j(widget["quiz_labels"])

    total_exercises = (
        len(d["warmup"]) + len(d["diagnostic"])
        + len(d["reading"]["comprehension"])
        + len(d["vocab_check"]["match"]) + len(d["vocab_check"]["gapfill"])
        + len(practice["gapfill"]) + len(second_widget["items"]) + len(practice["builders"])
        + len(d["listening"]["comprehension"]) + len(d["exit"])
    )

    second_js = ""
    if second_widget["type"] == "categorise":
        second_js = f'''
  Course.renderCategorise('cat-root', {j(second_widget["items"])}, {j(second_widget["categories"])}, {{lessonId: LESSON_ID, sectionPrefix: 'practice-cat'}});'''
    else:
        parts = []
        for i, item in enumerate(second_widget["items"]):
            parts.append(
                f'''  Course.initErrorSpot('err{i+1}', {{
    lessonId: LESSON_ID, sectionId: 'practice-err-{i+1}',
    words: {j(item["words"])}, errorIndices: {j(item["error_indices"])}, correction: {j(item.get("correction", ""))}, explanation: {j(item.get("explanation"))}
  }});'''
            )
        second_js = "\n".join(parts)

    # warmup/diagnostic containers are pre-rendered in HTML with fixed ids (warm-q1 etc.), so
    # instead of renderMCQList (which also renders markup) we just wire initMCQ directly against
    # the pre-built option buttons — matching the original course's hand-authored pattern exactly.
    def _mcq_group(prefix, section_prefix, questions):
        """Wires one initMCQ per question, then a single
        ensureAnswerPositionVariety call so the group's correct answers
        don't all end up on the same on-screen position by chance."""
        wires = [
            f'''  Course.initMCQ('{prefix}-q{i+1}', {{lessonId: LESSON_ID, sectionId: '{section_prefix}-{i+1}', correctValue: {j(next(o["value"] for o in q["options"] if o["correct"]))}, restoreAnswer: (sectionMap['{section_prefix}-{i+1}']||{{}}).answer_given}});'''
            for i, q in enumerate(questions)
        ]
        variety_items = j([
            {"containerId": f"{prefix}-q{i+1}", "correctValue": next(o["value"] for o in q["options"] if o["correct"])}
            for i, q in enumerate(questions)
        ])
        wires.append(f'''  Course.ensureAnswerPositionVariety({variety_items});''')
        return "\n".join(wires)

    warmup_wire = _mcq_group("warm", "warmup", d["warmup"])
    diag_wire = _mcq_group("diag", "diagnostic", d["diagnostic"])
    comp_wire = _mcq_group("comp", "reading-comp", d["reading"]["comprehension"])
    vocab_wire = _mcq_group("vocab", "vocab", d["vocab_check"]["match"])
    listen_wire = _mcq_group("listen", "listening", d["listening"]["comprehension"])
    exit_wire = _mcq_group("exit", "exit", d["exit"])

    script = f'''
const LESSON_ID = {j(lesson_id)};
Course.initPageChrome({{lessonId: LESSON_ID}});
Course.initStepTabs();

(async function initLesson(){{
  await Course.initSyncStatus(LESSON_ID);
  const sectionMap = Course.getSectionMap(LESSON_ID);

{warmup_wire}
{diag_wire}

  /* ---------------- concept widget ---------------- */
  Course.renderConceptWidget({{
    areaId: 'widget-area', hintId: 'widget-hint',
    tabIds: {tab_ids_js},
    categories: {categories_js},
    quizLabels: {quiz_labels_js},
    rulesToggleId: 'rules-toggle'
  }});
  {"Course.renderToneCells('compare-card', " + j(d["compare"]["items"]) + ");" if d.get("compare") else ""}

  /* ---------------- reading ---------------- */
  Course.initGramToggle();
  Course.wireGramSpans({j(d["reading"]["gram_explanations"])});
  Course.initVocab({j(d["reading"]["vocab_data"])}, LESSON_ID);
{comp_wire}

  /* ---------------- vocab check ---------------- */
{vocab_wire}
  {chr(10).join(f"  Course.initGapFill('vgap{i+1}-input','vgap{i+1}-check','vgap{i+1}-fb',{{lessonId:LESSON_ID, sectionId:'vocab-gap-{i+1}', correctAnswers:{j(g['answers'])}, restore: sectionMap['vocab-gap-{i+1}'] ? {{answerGiven: sectionMap['vocab-gap-{i+1}'].answer_given, isCorrect: sectionMap['vocab-gap-{i+1}'].override_correct ?? sectionMap['vocab-gap-{i+1}'].is_correct}} : null}});" for i, g in enumerate(d["vocab_check"]["gapfill"]))}

  /* ---------------- practice ---------------- */
  {chr(10).join(f"  Course.initGapFill('gap{i+1}-input','gap{i+1}-check','gap{i+1}-fb',{{lessonId:LESSON_ID, sectionId:'practice-gap-{i+1}', correctAnswers:Course.withContractions({j(g['answers'])}), restore: sectionMap['practice-gap-{i+1}'] ? {{answerGiven: sectionMap['practice-gap-{i+1}'].answer_given, isCorrect: sectionMap['practice-gap-{i+1}'].override_correct ?? sectionMap['practice-gap-{i+1}'].is_correct}} : null}});" for i, g in enumerate(practice["gapfill"]))}
{second_js}
  Course.renderBuilders('builders', {j(practice["builders"])}, {{lessonId: LESSON_ID, sectionPrefix: 'practice-builder'}});

  /* ---------------- speaking ---------------- */
  Course.initSpeaking({{max: 2, lessonId: LESSON_ID, sectionMap, soloTaskLabel: {j(d["speaking"]["solo_text"])}}});
  Course.renderDiscussQuestions('discuss-questions', {j(d["speaking"]["group_questions"])}, {{lessonId: LESSON_ID, max: 2, sectionPrefix: 'speaking-q'}});

  /* ---------------- listening ---------------- */
  Course.initListening({{dialogue: {j(d["listening"]["dialogue"])}, speakerA: 'Anna', speakerB: 'Tomasz', lessonId: LESSON_ID}});
{listen_wire}

  /* ---------------- wrap-up ---------------- */
{exit_wire}
  Course.initSummary({{lessonId: LESSON_ID, totalExercises: {total_exercises}}});
}})();
'''

    return body, script
