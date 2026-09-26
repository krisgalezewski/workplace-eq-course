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
  Error:   {"type": "errorspot", "words": [str, ...], "error_indices": [int], "explanation": str}
           (tap the wrong word; uses the same Course.initErrorSpot as lessons)
"""
from gen_common import nav_header, j
TOTAL_TESTS = 1


def _render_item(kind_prefix, i, item):
    if item["type"] == "mcq":
        opts_html = "".join(f'<button class="opt" data-value="{o["value"]}">{o["label"]}</button>' for o in item["options"])
        html = f'''
      <div style="margin-bottom:18px">
        <p style="margin-bottom:8px;font-weight:550">{i+1}. {item["prompt"]}</p>
        <div id="{kind_prefix}-q{i+1}">
          {opts_html}
        </div>
      </div>'''
        correct_value = next(o["value"] for o in item["options"] if o["correct"])
        wire = f'''  Course.initMCQ('{kind_prefix}-q{i+1}', {{lessonId: LESSON_ID, sectionId: '{kind_prefix}-{i+1}', correctValue: {j(correct_value)}, restoreAnswer: (sectionMap['{kind_prefix}-{i+1}']||{{}}).answer_given}});'''
        variety_entry = {"containerId": f"{kind_prefix}-q{i+1}", "correctValue": correct_value}
        return html, wire, variety_entry
    elif item["type"] == "errorspot":
        html = f'''
      <div style="margin-bottom:18px">
        <p style="margin-bottom:8px;font-weight:550">{i+1}. Find the mistake — tap the wrong word.</p>
        <div id="{kind_prefix}-e{i+1}" style="font-size:15px;line-height:1.9"></div>
      </div>'''
        wire = f'''  Course.initErrorSpot('{kind_prefix}-e{i+1}', {{lessonId: LESSON_ID, sectionId: '{kind_prefix}-err-{i+1}', words: {j(item["words"])}, errorIndices: {j(item["error_indices"])}, explanation: {j(item["explanation"])}, restore: sectionMap['{kind_prefix}-err-{i+1}'] ? {{answerGiven: sectionMap['{kind_prefix}-err-{i+1}'].answer_given}} : null}});'''
        return html, wire, None
    else:  # gapfill
        width = item.get("width", 170)
        html = f'''
      <div style="margin-bottom:18px">
        <p style="margin-bottom:8px">{i+1}. {item["before"]} <input type="text" id="{kind_prefix}-g{i+1}-input" placeholder="type here" style="border:1px solid var(--border-strong);border-radius:8px;padding:6px 10px;font-family:inherit;width:{width}px"> {item.get("after","")}</p>
        <button class="btn btn-sm" id="{kind_prefix}-g{i+1}-check">Check</button>
        <div id="{kind_prefix}-g{i+1}-fb"></div>
      </div>'''
        wire = f'''  Course.initGapFill('{kind_prefix}-g{i+1}-input','{kind_prefix}-g{i+1}-check','{kind_prefix}-g{i+1}-fb', {{lessonId: LESSON_ID, sectionId: '{kind_prefix}-gap-{i+1}', correctAnswers: Course.withContractions({j(item["answers"])}), restore: sectionMap['{kind_prefix}-gap-{i+1}'] ? {{answerGiven: sectionMap['{kind_prefix}-gap-{i+1}'].answer_given, isCorrect: sectionMap['{kind_prefix}-gap-{i+1}'].override_correct ?? sectionMap['{kind_prefix}-gap-{i+1}'].is_correct}} : null}});'''
        return html, wire, None


def render_test(d):
    """d: {id, num, title, subtitle, part1: {heading, intro, items}, part2: {heading, intro, items} | None}"""
    test_id = d["id"]
    header = nav_header('Final test' if TOTAL_TESTS == 1 else f'Test {d["num"]} of {TOTAL_TESTS}', d["title"], d["subtitle"], is_test=True, section_name='Lessons 1–7')

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

    part1_section = f'''
  <section class="section" id="sec-part1">
    <div class="section-label"><span class="num">1</span> {part1["heading"]}</div>
    <div class="card">
      <p style="margin-bottom:16px;font-size:14.5px;color:var(--text-secondary)">{part1["intro"]}</p>
      {"".join(p1_html_items)}
    </div>
  </section>'''

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
        part2_section = f'''
  <section class="section" id="sec-part2">
    <div class="section-label"><span class="num">2</span> {part2["heading"]}</div>
    <div class="card">
      <p style="margin-bottom:16px;font-size:14.5px;color:var(--text-secondary)">{part2["intro"]}</p>
      {"".join(p2_html_items)}
    </div>
  </section>'''

    total_items = len(part1["items"]) + (len(d["part2"]["items"]) if d.get("part2") else 0)
    section_num = 3 if d.get("part2") else 2

    summary_html = f'''
  <section class="section" id="sec-wrapup">
    <div class="section-label"><span class="num">{section_num}</span> Your results</div>
    <div class="card" id="summary-card">
      <h3 style="margin-bottom:14px">Test summary</h3>
      <div style="display:flex;align-items:center;gap:16px;margin-bottom:16px" id="summary-ring-row">
        <div id="score-ring-holder"></div>
        <div>
          <div style="font-weight:600" id="summary-name">—</div>
          <div style="font-size:13px;margin-top:4px" id="summary-completion"></div>
          <div style="font-size:13px;color:var(--text-secondary);margin-top:4px" id="summary-weak">Finish the test to see your results.</div>
        </div>
      </div>
      <button class="btn btn-primary" id="finish-btn">Finish test &amp; see results</button>
      <button class="btn" id="export-btn" style="margin-left:8px;display:none">Export PDF report</button>
    </div>
  </section>'''

    body = "\n".join([header, part1_section, part2_section, summary_html])

    script = f'''
const LESSON_ID = {j(test_id)};
Course.initPageChrome({{lessonId: LESSON_ID, isTest: true}});

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
