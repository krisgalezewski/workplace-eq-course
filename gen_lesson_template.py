"""
Renders one lesson (a Python dict of content) into the standard
HTML skeleton + JS driver script, following the exact section order,
widget patterns and hard-learned rules from the handoff brief:
warm-up -> diagnostic -> concept (Structure/Examples/Quick check +
"Show full rules" with a tricky-part warn-box) -> reading (vocab +
grammar highlighting) -> vocabulary check -> grammar practice
(gap-fill, categorise/error-spot, sentence builder) -> speaking
(solo/group) -> listening (Anna & Tomasz dialogue) -> wrap-up exit
check + score summary.
"""
from gen_common import nav_header, j

TOTAL_LESSONS = 7


def vocab(key, text):
    return f'<span class="vocab" data-word="{key}">{text}</span>'


def gram(key, text):
    return f'<span class="gram" data-gram="{key}">{text}</span>'


def render_lesson(d):
    lesson_id = d["id"]
    eyebrow = f'Lesson {d["num"]} of {TOTAL_LESSONS} · {d["section_name"]}'
    header = nav_header(eyebrow, d["title"], d["subtitle"])

    # ---------- warm-up ----------
    warmup_qs = "".join(
        f'''
      <div style="margin-bottom:16px">
        <p style="margin-bottom:8px;font-weight:550">{i+1}. {q["prompt"]}</p>
        <div id="warm-q{i+1}">
          {"".join(f'<button class="opt" data-value="{o["value"]}">{o["label"]}</button>' for o in q["options"])}
        </div>
      </div>'''
        for i, q in enumerate(d["warmup"])
    )

    # ---------- diagnostic ----------
    diag_qs = "".join(
        f'''
      <div style="margin-bottom:18px">
        <p style="margin-bottom:8px;font-weight:550">{i+1}. {q["prompt"]}</p>
        <div id="diag-q{i+1}">
          {"".join(f'<button class="opt" data-value="{o["value"]}">{o["label"]}</button>' for o in q["options"])}
        </div>
      </div>'''
        for i, q in enumerate(d["diagnostic"])
    )

    widget = d["widget"]
    tabs_html = "".join(
        f'<button class="pill{" on" if i == 0 else ""}" id="mode-w-{t["key"]}">{t["label"]}</button>'
        for i, t in enumerate(widget["tabs"])
    )

    compare_html = ""
    if d.get("compare"):
        c = d["compare"]
        compare_html = f'''
    <div class="card">
      <h3 style="margin-bottom:6px">{c["title"]}</h3>
      <p style="font-size:13.5px;color:var(--text-secondary);margin-bottom:14px">{c["instruction"]}</p>
      <div id="compare-card" style="font-size:14.5px;line-height:1.9"></div>
    </div>'''

    concept_html = f'''
  <section class="section" id="sec-concept">
    <div class="section-label"><span class="num">3</span> The concept</div>

    <div class="card">
      <h3 style="margin-bottom:10px">{widget["heading"]}</h3>
      <p style="font-size:14.5px;line-height:1.7;margin-bottom:14px">{widget["intro"]}</p>
      <div class="mode-toggle mode-toggle-outline" style="flex-wrap:wrap;gap:8px">
        {tabs_html}
      </div>
      <div id="widget-area" style="margin-top:14px;padding:18px;border-radius:var(--radius-md);background:var(--surface-alt);border:1px solid var(--border)"></div>
      <p id="widget-hint" style="font-size:12.5px;color:var(--text-tertiary);margin-top:8px">— Click either cell to see another example.</p>

      <button class="pill" id="rules-toggle" style="margin-top:16px">📖 Show the full rules</button>
      <div class="expand-content" id="rules-content">
        <div style="margin-top:16px">
          {widget["rules_html"]}
        </div>
      </div>
    </div>
    {compare_html}
  </section>'''

    passage_paragraphs = "".join(f"<p>{p}</p>" for p in d["reading"]["passage_paragraphs"])
    reading_comp_qs = "".join(
        f'''
      <div style="margin-bottom:16px">
        <p style="margin-bottom:8px;font-weight:550">{i+1}. {q["prompt"]}</p>
        <div id="comp-q{i+1}">
          {"".join(f'<button class="opt" data-value="{o["value"]}">{o["label"]}</button>' for o in q["options"])}
        </div>
      </div>'''
        for i, q in enumerate(d["reading"]["comprehension"])
    )

    reading_html = f'''
  <section class="section" id="sec-reading">
    <div class="section-label"><span class="num">4</span> Reading — {d["reading"]["heading"]}</div>
    <div class="card">
      <button class="pill" id="gram-toggle">🔍 Show key phrases in this text</button>
      <div class="passage" id="passage" style="margin-top:14px">{passage_paragraphs}</div>
      <p style="font-size:12.5px;color:var(--text-tertiary);margin-top:10px">Tap a highlighted word for pronunciation, meaning and an example. With key phrases on, tap a highlighted phrase to see why it works (and what a less skilful speaker might have said).</p>
    </div>
    <div class="card">
      <h3 style="margin-bottom:12px">Did you follow it? Quick comprehension check</h3>
      {reading_comp_qs}
    </div>
  </section>'''

    vocab_match_html = "".join(
        f'''
      <div style="margin-bottom:16px">
        <p style="margin-bottom:8px;font-weight:550">{i+1}. {q["prompt"]}</p>
        <div id="vocab-q{i+1}">
          {"".join(f'<button class="opt" data-value="{o["value"]}">{o["label"]}</button>' for o in q["options"])}
        </div>
      </div>'''
        for i, q in enumerate(d["vocab_check"]["match"])
    )
    vocab_gap_html = "".join(
        f'''
      <div style="margin-bottom:16px">
        <p style="margin-bottom:8px">{i+1}. {g["before"]} <input type="text" id="vgap{i+1}-input" placeholder="type here" style="border:1px solid var(--border-strong);border-radius:8px;padding:6px 10px;font-family:inherit;width:{g.get("width",160)}px"> {g.get("after","")}</p>
        <button class="btn btn-sm" id="vgap{i+1}-check">Check</button>
        <div id="vgap{i+1}-fb"></div>
      </div>'''
        for i, g in enumerate(d["vocab_check"]["gapfill"])
    )

    vocab_html = f'''
  <section class="section" id="sec-vocab">
    <div class="section-label"><span class="num">5</span> Vocabulary check</div>
    <div class="card">
      <p style="font-size:14.5px;margin-bottom:16px">The key words from the text — mixed formats.</p>
      <h4 style="font-size:13px;text-transform:uppercase;letter-spacing:.03em;color:var(--text-tertiary);margin-bottom:12px">Match the meaning</h4>
      {vocab_match_html}
      <h4 style="font-size:13px;text-transform:uppercase;letter-spacing:.03em;color:var(--text-tertiary);margin-bottom:12px;padding-top:6px;border-top:1px solid var(--border)">Complete the sentence — vocabulary focus</h4>
      {vocab_gap_html}
    </div>
  </section>'''

    practice = d["practice"]
    practice_gap_html = "".join(
        f'''
      <div style="margin-bottom:18px">
        <p style="margin-bottom:8px">{i+1}. {g["before"]} <input type="text" id="gap{i+1}-input" placeholder="type here" style="border:1px solid var(--border-strong);border-radius:8px;padding:6px 10px;font-family:inherit;width:{g.get("width",170)}px"> {g.get("after","")}</p>
        <button class="btn btn-sm" id="gap{i+1}-check">Check</button>
        <div id="gap{i+1}-fb"></div>
      </div>'''
        for i, g in enumerate(practice["gapfill"])
    )

    second_widget = practice["second"]  # {"type":"categorise"|"errorspot", "title", "instruction", "root_id":"cat-root" or per-sentence divs}
    if second_widget["type"] == "categorise":
        second_html = f'''
    <div class="card">
      <h3 style="margin-bottom:6px">{second_widget["title"]}</h3>
      <p style="font-size:13.5px;color:var(--text-secondary);margin-bottom:16px">{second_widget["instruction"]}</p>
      <div id="cat-root"></div>
    </div>'''
    else:
        sentences_html = "".join(
            f'''
      <div style="margin-bottom:8px;font-size:12px;font-weight:650;text-transform:uppercase;letter-spacing:.03em;color:var(--text-tertiary){"" if i == 0 else ";padding-top:16px;border-top:1px solid var(--border)"}">Sentence {i+1}</div>
      <div id="err{i+1}" style="font-size:15px;line-height:1.9;margin-bottom:20px"></div>'''
            for i in range(len(second_widget["items"]))
        )
        second_html = f'''
    <div class="card">
      <h3 style="margin-bottom:6px">{second_widget["title"]}</h3>
      <p style="font-size:13.5px;color:var(--text-secondary);margin-bottom:16px">{second_widget["instruction"]}</p>
      {sentences_html}
    </div>'''

    practice_html = f'''
  <section class="section" id="sec-practice">
    <div class="section-label"><span class="num">6</span> Practice</div>
    <div class="card">
      <h3 style="margin-bottom:2px">Gap-fill</h3>
      <p style="font-size:12.5px;text-transform:uppercase;letter-spacing:.03em;color:var(--text-tertiary);margin-bottom:16px">Language focus — {practice["gapfill_focus"]}</p>
      {practice_gap_html}
    </div>
    {second_html}
    <div class="card">
      <h3 style="margin-bottom:6px">Sentence builder</h3>
      <p style="font-size:13.5px;color:var(--text-secondary);margin-bottom:14px">Tap the chips in the right order. Three rounds.</p>
      <div id="builders"></div>
    </div>
  </section>'''

    speaking_html = f'''
  <section class="section" id="sec-speaking">
    <div class="section-label"><span class="num">7</span> Speaking task</div>
    <div class="mode-toggle">
      <button class="pill on" id="mode-solo">👤 Solo</button>
      <button class="pill" id="mode-group">👥 Group (2–4)</button>
    </div>
    <div class="task-card" id="speak-solo">
      <div class="kicker">60-second task</div>
      <p style="font-size:14.5px;line-height:1.7">{d["speaking"]["solo_text"]}</p>
      <button class="btn btn-sm" id="solo-done-btn" style="margin-top:14px">✓ I've done this</button>
    </div>
    <div class="task-card" id="speak-group" style="display:none">
      <div class="kicker">Discussion — pick 1–2 questions to answer out loud</div>
      <p style="font-size:14.5px;line-height:1.7;margin-bottom:12px">Tap the question(s) you'll answer. Your teacher will see your pick and mark it after you speak.</p>
      <div id="discuss-questions" style="display:flex;flex-direction:column;gap:8px"></div>
      <p id="discuss-limit-msg" style="font-size:12.5px;color:var(--text-tertiary);margin-top:10px">You can select up to 2 questions.</p>
    </div>
  </section>'''

    listen_comp_qs = "".join(
        f'''
      <div style="margin-top:16px">
        <p style="margin-bottom:8px;font-weight:550">{i+1}. {q["prompt"]}</p>
        <div id="listen-q{i+1}">
          {"".join(f'<button class="opt" data-value="{o["value"]}">{o["label"]}</button>' for o in q["options"])}
        </div>
      </div>'''
        for i, q in enumerate(d["listening"]["comprehension"])
    )
    listening_html = f'''
  <section class="section" id="sec-listening">
    <div class="section-label"><span class="num">8</span> Listening</div>
    <div class="card">
      <p style="font-size:14px;color:var(--text-secondary);margin-bottom:12px">{d["listening"]["intro"]}</p>
      <audio id="dialogue-audio" preload="none" style="display:none"></audio>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <button class="btn btn-primary" id="play-dialogue">▶ Play dialogue</button>
        <button class="btn btn-ghost btn-sm" id="stop-dialogue">⏹ Stop</button>
        <button class="btn btn-ghost btn-sm" id="show-transcript">Show full transcript</button>
      </div>
      <div id="transcript"></div>
      {listen_comp_qs}
    </div>
  </section>'''

    exit_qs = "".join(
        f'''
      <div style="margin-bottom:16px">
        <p style="margin-bottom:8px;font-weight:550">{i+1}. {q["prompt"]}</p>
        <div id="exit-q{i+1}">
          {"".join(f'<button class="opt" data-value="{o["value"]}">{o["label"]}</button>' for o in q["options"])}
        </div>
      </div>'''
        for i, q in enumerate(d["exit"])
    )
    wrapup_html = f'''
  <section class="section" id="sec-wrapup">
    <div class="section-label"><span class="num">9</span> Wrap-up — exit check</div>
    <div class="card">
      {exit_qs}
    </div>
    <div class="card" id="summary-card">
      <h3 style="margin-bottom:14px">Your lesson summary</h3>
      <div style="display:flex;align-items:center;gap:16px;margin-bottom:16px" id="summary-ring-row">
        <div id="score-ring-holder"></div>
        <div>
          <div style="font-weight:600" id="summary-name">—</div>
          <div style="font-size:13px;margin-top:4px" id="summary-completion"></div>
          <div style="font-size:13px;color:var(--text-secondary);margin-top:4px" id="summary-weak">Finish the lesson to see your results.</div>
        </div>
      </div>
      <button class="btn btn-primary" id="finish-btn">Finish lesson &amp; see results</button>
      <button class="btn" id="export-btn" style="margin-left:8px;display:none">⬇ Export PDF report</button>
    </div>
  </section>'''

    body = "\n".join([
        header,
        f'\n  <section class="section" id="sec-warmup">\n    <div class="section-label"><span class="num">1</span> Warm-up</div>\n    <div class="card">\n      <p style="margin-bottom:14px;font-size:14.5px;color:var(--text-secondary)">{d["warmup_intro"]}</p>\n      {warmup_qs}\n      <div class="tip-box">💡 <span style="flex:1;min-width:0">{d["warmup_tip"]}</span></div>\n    </div>\n  </section>',
        f'\n  <section class="section" id="sec-diagnostic">\n    <div class="section-label"><span class="num">2</span> Quick check — before we explain anything</div>\n    <div class="card">\n      <p style="margin-bottom:16px;font-size:14.5px;color:var(--text-secondary)">Four quick questions. This isn\'t graded harshly — it just shows us where to focus.</p>\n      {diag_qs}\n    </div>\n  </section>',
        concept_html,
        reading_html,
        vocab_html,
        practice_html,
        speaking_html,
        listening_html,
        wrapup_html,
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
  {"Course.renderCompareCard('compare-card', " + j(d["compare"]["items"]) + ");" if d.get("compare") else ""}

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
