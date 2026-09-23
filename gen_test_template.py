"""
Renders one TEST (a Python dict of content) into the standard HTML
skeleton + JS driver script. Tests reuse the exact same engine
primitives as lessons (Course.initMCQ, Course.initGapFill,
Course.initErrorSpot, Course.lessonScore, Course.renderScoreRing,
Course.exportReportPDF) — no new engine code needed, only content,
per the handoff. Tests have no reading/vocab/speaking/listening
sections and no "My Glossary" nav link (is_test=True in nav_header).

Each test has two parts:
  - Part 1: covers only the section just completed.
  - Part 2: a balanced cumulative spread across all sections covered
    so far (Test 1 has no Part 2 — nothing precedes Section 1).

Item schema (used in both part1["items"] and part2["items"]):
  MCQ:     {"type": "mcq", "prompt": str, "options": [{"label","value","correct"}, ...]}
  Gapfill: {"type": "gapfill", "before": str, "after": str, "answers": [str, ...], "width": int(optional)}
"""
from gen_common import nav_header, j

TOTAL_TESTS = 1


def _render_item(kind_prefix, i, item):
    if item["type"] == "mcq":
        opts_html = "".join(f'<button class="opt" data-value="{o["value"]}">{o["label"]}</button>' for o in item["options"])
        cls = "opts opts-3" if len(item["options"]) == 3 else "opts"
        html = f'''
      <div class="q-block">
        <p class="q-text">{i+1}. {item["prompt"]}</p>
        <div class="{cls}" id="{kind_prefix}-q{i+1}">{opts_html}</div>
      </div>'''
        correct_value = next(o["value"] for o in item["options"] if o["correct"])
        wire = f'''  Course.initMCQ('{kind_prefix}-q{i+1}', {{lessonId: LESSON_ID, sectionId: '{kind_prefix}-{i+1}', correctValue: {j(correct_value)}, restoreAnswer: (sectionMap['{kind_prefix}-{i+1}']||{{}}).answer_given}});'''
        variety_entry = {"containerId": f"{kind_prefix}-q{i+1}", "correctValue": correct_value}
        return html, wire, variety_entry
    else:  # gapfill
        width = item.get("width", 170)
        html = f'''
        <div class="gap-row">
          <p class="gap-s">{i+1}. {item["before"]} <input type="text" id="{kind_prefix}-g{i+1}-input" aria-label="Gap {i+1}" autocomplete="off" style="width:{max(width,120)}px"> {item.get("after","")}</p>
          <button class="btn btn-sm" id="{kind_prefix}-g{i+1}-check">Check</button>
          <div id="{kind_prefix}-g{i+1}-fb"></div>
        </div>'''
        wire = f'''  Course.initGapFill('{kind_prefix}-g{i+1}-input','{kind_prefix}-g{i+1}-check','{kind_prefix}-g{i+1}-fb', {{lessonId: LESSON_ID, sectionId: '{kind_prefix}-gap-{i+1}', correctAnswers: Course.withContractions({j(item["answers"])}), restore: sectionMap['{kind_prefix}-gap-{i+1}'] ? {{answerGiven: sectionMap['{kind_prefix}-gap-{i+1}'].answer_given, isCorrect: sectionMap['{kind_prefix}-gap-{i+1}'].override_correct ?? sectionMap['{kind_prefix}-gap-{i+1}'].is_correct}} : null}});'''
        return html, wire, None


def _assemble(items, htmls):
    """Wrap runs of consecutive gap-fill rows in one bordered gap box."""
    out, run = [], []
    for item, h in zip(items, htmls):
        if item["type"] == "gapfill":
            run.append(h)
            continue
        if run:
            out.append('<div class="gapbox"><div class="gap-label">Gap-fill · one word per gap</div>' + "".join(run) + '</div>')
            run = []
        out.append(h)
    if run:
        out.append('<div class="gapbox"><div class="gap-label">Gap-fill · one word per gap</div>' + "".join(run) + '</div>')
    return "".join(out)


def _tsection(sid, num, title, inner, sub=""):
    sub_html = f'<div class="sec-sub">{sub}</div>' if sub else ""
    return f'''
  <section class="section eq-sec" id="{sid}">
    <div class="sec-num">{num:02d}</div>
    <div class="sec-body">
      <h2 class="sec-h">{title}</h2>{sub_html}
      {inner}
    </div>
  </section>'''


def render_test(d):
    """d: {id, num, title, subtitle, part1: {heading, intro, items}, part2: {heading, intro, items} | None}"""
    test_id = d["id"]
    steps = [("sec-part1", "Part 1")] + ([("sec-part2", "Part 2")] if d.get("part2") else []) + [("sec-wrapup", "Results")]
    header = nav_header('Final test' if TOTAL_TESTS == 1 else f'Test {d["num"]} of {TOTAL_TESTS}', d["title"], d["subtitle"], is_test=True, section_name='Lessons 1–7', steps=steps)

    part1 = d["part1"]
    p1_html_items = []
    p1_wires = []
    p1_variety = []
    for i, item in enumerate(part1["items"]):
        html, wire, variety_entry = _render_item("p1", i, item)
        p1_html_items.append(html)
        p1_wires.append(wire)
        if variety_entry:
            p1_variety.append(variety_entry)
    if p1_variety:
        p1_wires.append(f'''  Course.ensureAnswerPositionVariety({j(p1_variety)});''')

    part1_section = _tsection("sec-part1", 1, part1["heading"].split("—")[-1].strip(),
        f'<p style="font-size:17px">{part1["intro"]}</p>' + _assemble(part1["items"], p1_html_items),
        sub=part1["heading"].split("—")[0].strip())

    part2_section = ""
    p2_wires = []
    if d.get("part2"):
        part2 = d["part2"]
        p2_html_items = []
        p2_variety = []
        for i, item in enumerate(part2["items"]):
            html, wire, variety_entry = _render_item("p2", i, item)
            p2_html_items.append(html)
            p2_wires.append(wire)
            if variety_entry:
                p2_variety.append(variety_entry)
        if p2_variety:
            p2_wires.append(f'''  Course.ensureAnswerPositionVariety({j(p2_variety)});''')
        part2_section = _tsection("sec-part2", 2, part2["heading"].split("—")[-1].strip(),
            f'<p style="font-size:17px">{part2["intro"]}</p>' + _assemble(part2["items"], p2_html_items),
            sub=part2["heading"].split("—")[0].strip())

    total_items = len(part1["items"]) + (len(d["part2"]["items"]) if d.get("part2") else 0)
    section_num = 3 if d.get("part2") else 2

    summary_html = _tsection("sec-wrapup", section_num, "Your results", '''
    <div class="card" id="summary-card" style="border-top:0;padding-top:0">
      <div style="display:flex;align-items:center;gap:20px;margin-bottom:18px" id="summary-ring-row">
        <div id="score-ring-holder"></div>
        <div>
          <div id="summary-name">—</div>
          <div style="font-size:15px;margin-top:4px" id="summary-completion"></div>
          <div style="font-size:15px;color:var(--text-secondary);margin-top:4px" id="summary-weak">Finish the test to see your results.</div>
        </div>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <button class="btn btn-primary" id="finish-btn">Finish test &amp; see results</button>
        <button class="btn" id="export-btn" style="display:none">Export PDF report</button>
      </div>
    </div>''')

    body = "\n".join([header, '<main class="shell">', part1_section, part2_section, summary_html, '</main>'])

    script = f'''
const LESSON_ID = {j(test_id)};
Course.initPageChrome({{lessonId: LESSON_ID, isTest: true}});
Course.initStepTabs();

(async function initTest(){{
  await Course.initSyncStatus(LESSON_ID);
  const sectionMap = Course.getSectionMap(LESSON_ID);

  /* ---------------- part 1 ---------------- */
{chr(10).join(p1_wires)}

  /* ---------------- part 2 ---------------- */
{chr(10).join(p2_wires)}

  /* ---------------- results ---------------- */
  Course.initSummary({{lessonId: LESSON_ID, totalExercises: {total_items}}});
}})();
'''
    return body, script
