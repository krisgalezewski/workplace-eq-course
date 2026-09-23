/* ============================================================
   Workplace EQ — Shared Engine (forked from the English+ B2+/C1 engine)
   Reused as-is from the original B1+/B2 course per the handoff
   brief (§4: "reuse course-engine.js as-is; the new course's
   lessons just need their own vocab words and dialogues to work
   with the same mechanism automatically"). Used by every
   lesson-*.html. Handles:
     - progress logging (Supabase, with a localStorage fallback so
       the course still works fully offline)
     - vocab popovers (audio / IPA / example sentence / glossary)
     - generic exercise-checking helpers (MCQ, gap-fill, error-spot,
       matching)
     - end-of-lesson score summary + PDF export
   ============================================================ */

const Course = (() => {

  /* ----------------------------------------------------------
     SUPABASE CLIENT
     Loaded from shared/supabase-config.js + the supabase-js CDN
     script, both included before this file. If either is missing
     (offline, or a lesson opened before those scripts are added),
     Course still works entirely on localStorage — every Supabase
     call below is wrapped so a missing/failed connection never
     breaks the lesson itself, it just means that device's progress
     doesn't sync until it's back online.
     ---------------------------------------------------------- */
  let supabaseClient = null;
  try {
    if (window.supabase && window.SUPABASE_URL && window.SUPABASE_ANON_KEY){
      supabaseClient = window.supabase.createClient(window.SUPABASE_URL, window.SUPABASE_ANON_KEY);
    }
  } catch (e){ console.warn('Supabase client not initialised:', e); }

  function getGroupId(){
    const params = new URLSearchParams(window.location.search);
    return params.get('group') || 'local-demo';
  }
  const GROUP_ID = getGroupId();

  const knownMemberships = new Set(); // avoids re-checking group membership on every single answer
  async function ensureGroupMembership(groupId, studentName){
    if (!supabaseClient) return;
    const cacheKey = `${groupId}::${studentName}`;
    if (knownMemberships.has(cacheKey)) return;
    try {
      const { data } = await supabaseClient.from('groups').select('student_names').eq('group_id', groupId).maybeSingle();
      if (!data){
        await supabaseClient.from('groups').insert({ group_id: groupId, group_name: groupId, student_names: [studentName] });
      } else if (!data.student_names.includes(studentName)){
        await supabaseClient.from('groups').update({ student_names: [...data.student_names, studentName] }).eq('group_id', groupId);
      }
      knownMemberships.add(cacheKey);
    } catch (e){ console.warn('Supabase group membership check failed (will retry next answer):', e); }
  }

  /* ----------------------------------------------------------
     PROGRESS LOG
     Row shape mirrors the Supabase `lesson_progress` table.
     ---------------------------------------------------------- */
  const STORAGE_KEY = 'workplaceeq_progress';
  const GLOSSARY_KEY = 'workplaceeq_glossary';

  // Namespaced distinctly from the original B1+/B2 course's key so a
  // student who has taken both courses on the same device/origin gets
  // asked for their name independently in each — progress and "who am
  // I" never bleed across the two courses.
  const STUDENT_NAME_KEY = 'workplaceeq_student_name';
  function getStudentName(){
    let name = localStorage.getItem(STUDENT_NAME_KEY);
    if (!name){
      name = prompt("What's your name? (used to save your progress on this device)") || 'You';
      localStorage.setItem(STUDENT_NAME_KEY, name);
    }
    return name;
  }

  function readLog(){
    try{ return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; }
    catch(e){ return []; }
  }
  function writeLog(rows){
    localStorage.setItem(STORAGE_KEY, JSON.stringify(rows));
  }

  /**
   * Log one row of progress.
   * @param {Object} p
   * @param {string} p.lessonId
   * @param {string} p.sectionId
   * @param {'auto_graded'|'oral'} p.exerciseType
   * @param {'completed'|'absent'|'not_attempted'} p.status
   * @param {string} [p.answerGiven]
   * @param {boolean|null} [p.isCorrect]
   */
  function logProgress(p){
    const rows = readLog();
    const row = {
      group_id: GROUP_ID,
      student_name: getStudentName(),
      lesson_id: p.lessonId,
      section_id: p.sectionId,
      exercise_type: p.exerciseType || 'auto_graded',
      status: p.status || 'completed',
      answer_given: p.answerGiven ?? null,
      is_correct: p.isCorrect ?? null,
      override_correct: null,
      teacher_verdict: null,
      session_date: new Date().toISOString().slice(0,10),
      timestamp: new Date().toISOString()
    };
    rows.push(row);
    writeLog(rows);

    // Mirror to Supabase in the background — never blocks the UI, and a
    // failed/offline write here doesn't lose the answer, since the
    // localStorage copy above is already saved either way.
    if (supabaseClient){
      (async () => {
        await ensureGroupMembership(row.group_id, row.student_name);
        const { session_date, timestamp, ...dbRow } = row; // timestamp has a DB default; session_date matches the DB column
        dbRow.session_date = session_date;
        const { error } = await supabaseClient.from('lesson_progress').insert(dbRow);
        if (error) console.warn('Supabase progress insert failed:', error.message);
      })();
    }
  }

  function getLessonRows(lessonId){
    return readLog().filter(r => r.lesson_id === lessonId && r.student_name === getStudentName());
  }

  /**
   * Same rows as getLessonRows, but deduplicated to only the most recent
   * attempt per section_id.
   */
  function getCurrentRows(lessonId){
    const rows = getLessonRows(lessonId);
    const latestBySection = {};
    rows.forEach(r => {
      const existing = latestBySection[r.section_id];
      if (!existing || new Date(r.timestamp) >= new Date(existing.timestamp)){
        latestBySection[r.section_id] = r;
      }
    });
    return Object.values(latestBySection);
  }

  /** Same as getCurrentRows, but keyed by section_id for quick lookup — the shape rehydration needs. */
  function getSectionMap(lessonId){
    const map = {};
    getCurrentRows(lessonId).forEach(r => { map[r.section_id] = r; });
    return map;
  }

  function resetLocalProgress(lessonId){
    const rows = readLog().filter(r => !(r.lesson_id === lessonId && r.student_name === getStudentName()));
    writeLog(rows);
  }

  function lessonScore(lessonId, sectionPrefix){
    const rows = getCurrentRows(lessonId).filter(r =>
      r.exercise_type === 'auto_graded' &&
      (!sectionPrefix || r.section_id.startsWith(sectionPrefix)) &&
      r.is_correct !== null
    );
    const correct = rows.filter(r => (r.override_correct ?? r.is_correct)).length;
    return { correct, total: rows.length };
  }

  function weakSections(lessonId){
    const rows = getCurrentRows(lessonId).filter(r => (r.override_correct ?? r.is_correct) === false);
    return [...new Set(rows.map(r => r.section_id))];
  }

  /**
   * Pulls this student's rows down from Supabase and merges them into
   * local storage. Also PRUNES any local row whose section no longer
   * exists remotely — this is what makes a teacher's "wipe" on the
   * dashboard actually show up on the student's own device. Pruning
   * only ever happens right here, immediately after a confirmed-
   * successful fetch, never on a failed one.
   * Call this right before showing/exporting results, not continuously.
   */
  async function syncFromSupabase(lessonId){
    if (!supabaseClient) return;
    try {
      const { data, error } = await supabaseClient
        .from('lesson_progress')
        .select('*')
        .eq('group_id', GROUP_ID)
        .eq('student_name', getStudentName())
        .eq('lesson_id', lessonId);
      if (error || !data) { if (error) console.warn('Sync from Supabase failed:', error.message); return; }
      const remoteSections = new Set(data.map(r => r.section_id));
      let rows = readLog();
      let changed = false;

      data.forEach(remote => {
        const idx = rows.findIndex(r => r.lesson_id === lessonId && r.student_name === getStudentName() && r.section_id === remote.section_id);
        if (idx >= 0){
          if (rows[idx].override_correct !== remote.override_correct || rows[idx].teacher_verdict !== remote.teacher_verdict){
            rows[idx].override_correct = remote.override_correct;
            rows[idx].teacher_verdict = remote.teacher_verdict;
            changed = true;
          }
        } else {
          rows.push({ ...remote, timestamp: remote.created_at || new Date().toISOString() });
          changed = true;
        }
      });

      const beforeCount = rows.length;
      rows = rows.filter(r => {
        if (r.lesson_id !== lessonId || r.student_name !== getStudentName()) return true;
        return remoteSections.has(r.section_id);
      });
      if (rows.length !== beforeCount) changed = true;

      if (changed) writeLog(rows);
    } catch (e){ console.warn('Sync from Supabase failed:', e); }
  }

  function exportReport(lessonId, lessonTitle){
    const rows = getLessonRows(lessonId);
    const report = {
      student: getStudentName(),
      lesson_id: lessonId,
      lesson_title: lessonTitle,
      generated_at: new Date().toISOString(),
      rows
    };
    const blob = new Blob([JSON.stringify(report, null, 2)], {type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `${lessonId}-${getStudentName()}-progress.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  async function exportReportPDF(lessonId, lessonTitle, totalPossible){
    const rows = getCurrentRows(lessonId);
    const student = getStudentName();
    const date = new Date().toLocaleDateString();
    const autoRows = rows.filter(r => r.exercise_type === 'auto_graded');
    const oralRows = rows.filter(r => r.exercise_type === 'oral' && r.status === 'completed');
    const correct = autoRows.filter(r => (r.override_correct ?? r.is_correct)).length;
    const pct = autoRows.length ? Math.round((correct / autoRows.length) * 100) : 0;
    const esc = (s) => (s ?? '').toString().replace(/</g, '&lt;');

    let printRoot = document.getElementById('course-print-report');
    if (!printRoot){
      printRoot = document.createElement('div');
      printRoot.id = 'course-print-report';
      document.body.appendChild(printRoot);
    }
    printRoot.innerHTML = `
      <div style="border-bottom:3px solid #185FA5;padding-bottom:12px;margin-bottom:20px">
        <div style="font-size:11px;color:#5B6472;text-transform:uppercase;letter-spacing:.05em">Workplace EQ · English Voiced with Kris</div>
        <h1 style="font-size:21px;margin:4px 0 0">${esc(lessonTitle)}</h1>
      </div>
      <p style="font-size:13px;margin:0 0 3px"><b>Student:</b> ${esc(student)}</p>
      <p style="font-size:13px;margin:0 0 18px"><b>Date:</b> ${esc(date)}</p>
      <div style="background:#E6F1FB;border-radius:10px;padding:14px 18px;margin-bottom:${typeof totalPossible === 'number' ? '8px' : '22px'}">
        <div style="font-size:19px;font-weight:700;color:#0C4577">${correct} / ${autoRows.length} correct (${pct}%)</div>
      </div>
      ${typeof totalPossible === 'number' ? (autoRows.length < totalPossible ? `
      <div style="background:#FAEEDA;border:1px solid #E8C080;border-radius:8px;padding:10px 14px;margin-bottom:22px;font-size:12px;color:#633806">
        Note: only ${Math.round((autoRows.length / totalPossible) * 100)}% of the lesson attempted (${autoRows.length} of ${totalPossible} exercises) — this score reflects only what's been answered so far.
      </div>` : `
      <div style="background:#EAF3DE;border:1px solid #C0DD97;border-radius:8px;padding:10px 14px;margin-bottom:22px;font-size:12px;color:#27500A">
        ✓ Every exercise in this lesson has been attempted.
      </div>`) : ''}
      <h2 style="font-size:14px;margin-bottom:8px">Exercise breakdown</h2>
      <table style="width:100%;border-collapse:collapse;font-size:11.5px;margin-bottom:22px">
        <thead><tr style="background:#EEF1F5;text-align:left">
          <th style="padding:5px 7px;border-bottom:1px solid #DFE3E9">Section</th>
          <th style="padding:5px 7px;border-bottom:1px solid #DFE3E9">Your answer</th>
          <th style="padding:5px 7px;border-bottom:1px solid #DFE3E9">Result</th>
        </tr></thead>
        <tbody>
          ${autoRows.map(r => {
            const ok = r.override_correct ?? r.is_correct;
            const resultLabel = r.override_correct !== null && r.override_correct !== undefined ? (ok ? 'Correct (revised)' : 'Needs review (revised)') : (ok ? 'Correct' : 'Needs review');
            return `<tr>
              <td style="padding:5px 7px;border-bottom:1px solid #EEF1F5">${esc(r.section_id)}</td>
              <td style="padding:5px 7px;border-bottom:1px solid #EEF1F5">${esc(r.answer_given)}</td>
              <td style="padding:5px 7px;border-bottom:1px solid #EEF1F5;color:${ok ? '#27500A' : '#791F1F'}">${resultLabel}</td>
            </tr>`;
          }).join('')}
        </tbody>
      </table>
      ${oralRows.length ? `
        <h2 style="font-size:14px;margin-bottom:8px">Speaking / discussion</h2>
        <ul style="font-size:11.5px;padding-left:16px;margin:0">
          ${oralRows.map(r => `<li style="margin-bottom:5px">${esc(r.answer_given)} — <i>${esc(r.teacher_verdict) || 'not yet marked'}</i></li>`).join('')}
        </ul>` : ''}
    `;
    window.print();
  }

  /* ----------------------------------------------------------
     AUDIO: file-first, speechSynthesis fallback
     Checks (via cached fetch HEAD, once per session per word) whether
     a pre-generated audio file exists before falling back to the
     browser's built-in speechSynthesis. The course works immediately
     with zero real audio files present, and silently upgrades the
     moment real files are dropped in — no code changes needed.
     ---------------------------------------------------------- */
  function slugifyForAudio(text){
    return text.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
      .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  }
  const audioFileCache = new Map(); // slug -> true|false, checked once per session
  let currentAudioEl = null;
  async function speakSmart(text, fallback){
    const slug = slugifyForAudio(text);
    const src = `audio/vocab/${slug}.mp3`;
    if (!audioFileCache.has(slug)){
      try {
        const res = await fetch(src, { method: 'HEAD' });
        audioFileCache.set(slug, res.ok);
      } catch (e) { audioFileCache.set(slug, false); }
    }
    if (audioFileCache.get(slug)){
      if (currentAudioEl) currentAudioEl.pause();
      currentAudioEl = new Audio(src);
      currentAudioEl.play().catch(() => fallback());
    } else {
      fallback();
    }
  }
  function speak(text){
    speakSmart(text, () => {
      if (!('speechSynthesis' in window)) return;
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.rate = 0.92;
      window.speechSynthesis.speak(u);
    });
  }

  /* ----------------------------------------------------------
     GLOSSARY
     ---------------------------------------------------------- */
  function getGlossary(){
    try { return JSON.parse(localStorage.getItem(GLOSSARY_KEY)) || {}; }
    catch (e){ return {}; }
  }
  function writeGlossaryLocal(glossary){
    localStorage.setItem(GLOSSARY_KEY, JSON.stringify(glossary));
  }

  async function saveToGlossary(wordKey, data, lessonId){
    const glossary = getGlossary();
    glossary[wordKey] = { word: data.word, ipa: data.ipa, meaning: data.meaning, example: data.example, lessonId: lessonId || null };
    writeGlossaryLocal(glossary);

    if (supabaseClient){
      (async () => {
        await ensureGroupMembership(GROUP_ID, getStudentName());
        const { error } = await supabaseClient.from('glossary').upsert({
          group_id: GROUP_ID, student_name: getStudentName(), word_key: wordKey,
          word: data.word, ipa: data.ipa, meaning: data.meaning, example: data.example, lesson_id: lessonId || null
        }, { onConflict: 'group_id,student_name,word_key' });
        if (error) console.warn('Glossary sync failed:', error.message);
      })();
    }
  }

  async function removeFromGlossary(wordKey){
    const glossary = getGlossary();
    delete glossary[wordKey];
    writeGlossaryLocal(glossary);
    if (supabaseClient){
      const { error } = await supabaseClient.from('glossary').delete()
        .eq('group_id', GROUP_ID).eq('student_name', getStudentName()).eq('word_key', wordKey);
      if (error) console.warn('Glossary remove failed:', error.message);
    }
  }

  async function syncGlossaryFromSupabase(){
    if (!supabaseClient) return;
    try {
      const { data, error } = await supabaseClient.from('glossary').select('*')
        .eq('group_id', GROUP_ID).eq('student_name', getStudentName());
      if (error || !data) { if (error) console.warn('Glossary sync failed:', error.message); return; }
      const glossary = getGlossary();
      data.forEach(r => {
        glossary[r.word_key] = { word: r.word, ipa: r.ipa, meaning: r.meaning, example: r.example, lessonId: r.lesson_id };
      });
      writeGlossaryLocal(glossary);
    } catch (e){ console.warn('Glossary sync failed:', e); }
  }

  function initVocab(vocabData, lessonId){
    document.querySelectorAll('.vocab').forEach(el => {
      el.addEventListener('click', () => {
        const key = el.dataset.word;
        const data = vocabData[key];
        if (!data) return;
        if (popupTrigger === el){ hidePopup(); return; }
        const alreadySaved = !!getGlossary()[key];
        const html = `
          <div class="vocab-pop-word">${data.word}</div>
          <div class="vocab-pop-ipa">${data.ipa}</div>
          <button class="audio-btn vocab-audio-btn" data-speak="${data.word}">Hear it</button>
          <div style="font-size:14px;margin-bottom:8px">${data.meaning}</div>
          <div class="vocab-pop-ex">"${data.example}"</div>
          <button class="btn btn-sm glossary-btn" data-word="${key}" ${alreadySaved ? 'disabled' : ''}>${alreadySaved ? 'Saved ✓' : '+ Add to my glossary'}</button>
        `;
        showPopup(html, el);
        const content = document.getElementById('course-popup-content');
        content.querySelector('.vocab-audio-btn')?.addEventListener('click', (e) => { e.stopPropagation(); speak(data.word); });
        content.querySelector('.glossary-btn')?.addEventListener('click', async (e) => {
          e.stopPropagation();
          await saveToGlossary(key, data, lessonId);
          const btn = content.querySelector('.glossary-btn');
          btn.textContent = 'Saved ✓'; btn.disabled = true;
        });
      });
    });
  }

  /* ----------------------------------------------------------
     SHUFFLING
     ---------------------------------------------------------- */
  function shuffleArray(arr){
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--){
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function shuffleOptions(containerId){
    const container = document.getElementById(containerId);
    if (!container) return;
    const buttons = Array.from(container.querySelectorAll('.opt'));
    shuffleArray(buttons).forEach(btn => container.appendChild(btn));
  }

  /* ----------------------------------------------------------
     POPUP
     ---------------------------------------------------------- */
  let popupTrigger = null;
  function ensurePopupRoot(){
    let root = document.getElementById('course-popup-root');
    if (!root){
      root = document.createElement('div');
      root.id = 'course-popup-root';
      root.innerHTML = `
        <div id="course-popup-backdrop" class="course-popup-backdrop"></div>
        <div id="course-popup-box" class="course-popup-box" role="dialog">
          <button id="course-popup-close" class="course-popup-close" aria-label="Close">&times;</button>
          <div id="course-popup-content"></div>
        </div>
      `;
      document.body.appendChild(root);
      document.getElementById('course-popup-backdrop').addEventListener('click', hidePopup);
      document.getElementById('course-popup-close').addEventListener('click', hidePopup);
    }
    return root;
  }
  function showPopup(html, triggerEl){
    const root = ensurePopupRoot();
    if (triggerEl && popupTrigger === triggerEl){ hidePopup(); return; }
    document.getElementById('course-popup-content').innerHTML = html;
    root.classList.add('open');
    popupTrigger = triggerEl || null;
  }
  function hidePopup(){
    const root = document.getElementById('course-popup-root');
    if (root) root.classList.remove('open');
    popupTrigger = null;
  }

  /* ----------------------------------------------------------
     SHUFFLE-WITH-VARIETY
     After a whole task's worth of related MCQs has been built (each
     one already independently shuffled by shuffleOptions inside
     initMCQ), this spreads the CORRECT answer's on-screen position as
     evenly as mathematically possible across the group, so a task
     never ends up with every correct answer in the same spot (e.g.
     always "top") purely by chance — which independent per-question
     randomising can easily produce, especially with only 2 options.

     items: [{ containerId, correctValue }] for one task's questions.
     For N questions sharing K on-screen positions, exactly floor(N/K)
     or ceil(N/K) of them get each position (counts differ by at most
     1) — e.g. 3 two-option questions -> a 2/1 split, 5 -> a 3/2 split
     — while WHICH question lands on which position stays randomised.
     ---------------------------------------------------------- */
  function ensureAnswerPositionVariety(items){
    const usable = (items || []).filter(it => it && document.getElementById(it.containerId));
    if (usable.length < 2) return;
    const numOptions = Math.min(...usable.map(it => document.getElementById(it.containerId).querySelectorAll('.opt').length));
    if (numOptions < 2) return;

    const n = usable.length;
    const base = Math.floor(n / numOptions);
    let extra = n - base * numOptions;
    const targetPositions = [];
    for (let p = 0; p < numOptions; p++){
      const count = base + (extra > 0 ? 1 : 0);
      if (extra > 0) extra--;
      for (let k = 0; k < count; k++) targetPositions.push(p);
    }
    const assigned = shuffleArray(targetPositions);

    usable.forEach((it, idx) => {
      const container = document.getElementById(it.containerId);
      const opts = Array.from(container.querySelectorAll('.opt'));
      const correctIdx = opts.findIndex(o => o.dataset.value === it.correctValue);
      if (correctIdx === -1) return;
      const targetIdx = Math.min(assigned[idx], opts.length - 1);
      if (correctIdx === targetIdx) return;
      const [correctEl] = opts.splice(correctIdx, 1);
      opts.splice(targetIdx, 0, correctEl);
      opts.forEach(o => container.appendChild(o));
    });
  }

  /* ----------------------------------------------------------
     GENERIC MULTIPLE-CHOICE EXERCISE
     ---------------------------------------------------------- */
  function initMCQ(containerId, {lessonId, sectionId, correctValue, onAnswered, restoreAnswer}){
    const container = document.getElementById(containerId);
    if (!container) return;
    shuffleOptions(containerId); // randomise displayed order so the correct answer isn't always first
    const opts = container.querySelectorAll('.opt');
    let answered = false;

    function applyResult(chosenValue){
      opts.forEach(o => {
        if (o.dataset.value === correctValue) o.classList.add('ok');
        else if (o.dataset.value === chosenValue) o.classList.add('bad');
        else o.classList.add('dim');
      });
    }

    if (restoreAnswer !== undefined && restoreAnswer !== null){
      answered = true;
      applyResult(restoreAnswer);
    }

    opts.forEach(opt => {
      opt.addEventListener('click', () => {
        if (answered) return;
        answered = true;
        const chosen = opt.dataset.value;
        const isCorrect = chosen === correctValue;
        applyResult(chosen);
        logProgress({ lessonId, sectionId, answerGiven: chosen, isCorrect });
        if (onAnswered) onAnswered(isCorrect, chosen);
      });
    });
  }

  /* ----------------------------------------------------------
     FIND-THE-ERROR
     ---------------------------------------------------------- */
  function initErrorSpot(containerId, {lessonId, sectionId, words, errorIndices, correction, explanation, onAnswered, restore}){
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = words.map((w, i) => `<span class="err-word" data-idx="${i}">${w}</span>`).join(' ');
    const spans = container.querySelectorAll('.err-word');
    let answered = false;

    function reveal(clickedIdx){
      spans.forEach(s => {
        const idx = Number(s.dataset.idx);
        if (errorIndices.includes(idx)) s.classList.add('err-target');
        else if (idx === clickedIdx) s.classList.add('err-wrong-pick');
        s.style.pointerEvents = 'none';
      });
      const isCorrect = errorIndices.includes(clickedIdx);
      const note = document.createElement('div');
      note.className = isCorrect ? 'fb-ok' : 'fb-no';
      note.style.marginTop = '8px';
      // Workplace EQ: faux-pas items pass `explanation` (a full sentence
      // on why the word is socially wrong) instead of a `correction`.
      const target = errorIndices.map(i => words[i]).join(' ');
      if (explanation){
        note.textContent = isCorrect
          ? `✓ Spotted it — ${explanation}`
          : `Not quite — the problem was "${target}". ${explanation}`;
      } else {
        note.textContent = isCorrect
          ? `✓ Correct — should be "${correction}"`
          : `Not quite — the error was "${target}", which should be "${correction}"`;
      }
      container.insertAdjacentElement('afterend', note);
    }

    if (restore){
      answered = true;
      reveal(Number(restore.answerGiven));
      return;
    }

    spans.forEach(s => {
      s.addEventListener('click', () => {
        if (answered) return;
        answered = true;
        const idx = Number(s.dataset.idx);
        const isCorrect = errorIndices.includes(idx);
        reveal(idx);
        logProgress({ lessonId, sectionId, answerGiven: String(idx), isCorrect });
        if (onAnswered) onAnswered(isCorrect);
      });
    });
  }

  /* ----------------------------------------------------------
     MATCHING
     ---------------------------------------------------------- */
  function initMatching(containerId, {lessonId, sectionPrefix, pairs, onAnswered, sectionMap}){
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = `
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px 16px">
        <div id="${containerId}-left" style="display:flex;flex-direction:column;gap:8px"></div>
        <div id="${containerId}-right" style="display:flex;flex-direction:column;gap:8px"></div>
      </div>
    `;
    const leftEl = document.getElementById(`${containerId}-left`);
    const rightEl = document.getElementById(`${containerId}-right`);
    const leftItems = pairs.map((p, i) => ({ text: p.left, idx: i }));
    let rightItems;
    let attempts = 0;
    do {
      rightItems = shuffleArray(pairs.map((p, i) => ({ text: p.right, idx: i })));
      attempts++;
    } while (rightItems.filter((item, row) => item.idx === row).length > 1 && attempts < 50);

    let selectedLeftIdx = null;
    const answeredLeft = new Map();
    const usedRight = new Set();

    if (sectionMap){
      pairs.forEach((p, i) => {
        const row = sectionMap[`${sectionPrefix}-${i + 1}`];
        if (row){
          const isCorrect = row.override_correct ?? row.is_correct;
          answeredLeft.set(i, isCorrect);
          if (isCorrect) usedRight.add(i);
        }
      });
    }

    function renderLeft(){
      leftEl.innerHTML = '';
      leftItems.forEach(item => {
        const btn = document.createElement('button');
        btn.className = 'chip match-item';
        if (answeredLeft.has(item.idx)){
          btn.classList.add(answeredLeft.get(item.idx) ? 'match-correct' : 'match-wrong');
          btn.disabled = true;
        } else {
          if (selectedLeftIdx === item.idx) btn.classList.add('sel');
          btn.addEventListener('click', () => { selectedLeftIdx = item.idx; renderLeft(); });
        }
        btn.textContent = item.text;
        leftEl.appendChild(btn);
      });
    }
    function renderRight(){
      rightEl.innerHTML = '';
      rightItems.forEach(item => {
        const btn = document.createElement('button');
        btn.className = 'chip match-item';
        if (usedRight.has(item.idx)){
          btn.classList.add('match-correct');
          btn.disabled = true;
        } else {
          btn.addEventListener('click', () => {
            if (selectedLeftIdx === null || answeredLeft.has(selectedLeftIdx)) return;
            const isCorrect = item.idx === selectedLeftIdx;
            const sectionId = `${sectionPrefix}-${selectedLeftIdx + 1}`;
            answeredLeft.set(selectedLeftIdx, isCorrect);
            if (isCorrect) usedRight.add(item.idx);
            logProgress({ lessonId, sectionId, answerGiven: item.text, isCorrect });
            selectedLeftIdx = null;
            renderLeft(); renderRight();
            if (onAnswered) onAnswered(isCorrect);
          });
        }
        btn.textContent = item.text;
        rightEl.appendChild(btn);
      });
    }
    renderLeft();
    renderRight();
  }

  /* ----------------------------------------------------------
     GENERIC GAP-FILL (typed answer, case-insensitive, trims)
     ---------------------------------------------------------- */
  function withContractions(answers){
    const subjectMap = { have:"'ve", has:"'s", am:"'m", are:"'re", is:"'s", will:"'ll", would:"'d", had:"'d" };
    const modalMap = { would:"would've", could:"could've", might:"might've", should:"should've", must:"must've" };
    const expanded = [...answers];
    answers.forEach(a => {
      const words = a.split(' ');
      const firstWord = words[0].toLowerCase();
      const rest = a.slice(words[0].length);

      if (subjectMap[firstWord] && rest) expanded.push(subjectMap[firstWord] + rest);

      if (modalMap[firstWord]){
        if (words[1] && words[1].toLowerCase() === 'have'){
          const tail = words.slice(2).join(' ');
          expanded.push(`${modalMap[firstWord]}${tail ? ' ' + tail : ''}`);
        } else if (words[2] && words[2].toLowerCase() === 'have'){
          const adverb = words[1];
          const tail = words.slice(3).join(' ');
          expanded.push(`${modalMap[firstWord]} ${adverb}${tail ? ' ' + tail : ''}`);
        }
      }
    });
    return expanded;
  }

  function initGapFill(inputId, checkBtnId, feedbackId, {lessonId, sectionId, correctAnswers, showAnswerHint = false, restore, onAnswered}){
    const input = document.getElementById(inputId);
    const btn = document.getElementById(checkBtnId);
    const fb = document.getElementById(feedbackId);
    if (!input || !btn) return;

    function normalizeAnswer(s){
      return s
        .trim()
        .toLowerCase()
        .replace(/[‘’ʼ']/g, '')
        .replace(/[.!?]+$/, '')
        .replace(/\s+/g, ' ');
    }

    function showFeedback(isCorrect){
      const hintAnswers = correctAnswers.filter(a => !a.startsWith("'"));
      if (isCorrect){
        fb.innerHTML = showAnswerHint
          ? `<div class="fb-ok">✓ Correct — "${hintAnswers.join(' OR ')}"</div>`
          : `<div class="fb-ok">✓ Correct!</div>`;
        return;
      }
      if (hintAnswers.length > 1){
        const list = hintAnswers.map(a => `"${a}"`).join(' or ');
        fb.innerHTML = `<div class="fb-no">Not quite. A few answers would work here: ${list} — we'll go over this one together.</div>`;
      } else {
        fb.innerHTML = `<div class="fb-no">Not quite. A correct answer would be: "${hintAnswers[0]}".</div>`;
      }
    }

    if (restore){
      input.value = restore.answerGiven ?? '';
      input.disabled = true; btn.disabled = true;
      showFeedback(restore.isCorrect);
      return;
    }

    btn.addEventListener('click', () => {
      const val = normalizeAnswer(input.value);
      const accepted = correctAnswers.map(normalizeAnswer);
      const isCorrect = accepted.includes(val);
      showFeedback(isCorrect);
      input.disabled = true; btn.disabled = true;
      logProgress({ lessonId, sectionId, answerGiven: input.value.trim(), isCorrect });
      if (onAnswered) onAnswered(isCorrect);
    });
  }

  /* ----------------------------------------------------------
     SCORE SUMMARY RENDER
     ---------------------------------------------------------- */
  function renderScoreRing(elId, correct, total){
    const el = document.getElementById(elId);
    if (!el) return;
    const pct = total ? Math.round((correct/total)*100) : 0;
    el.innerHTML = `<div class="score-ring">${pct}%</div>`;
  }

  /* ============================================================
     B2+/C1 COURSE ADDITIONS
     A small set of DATA-DRIVEN renderers layered on top of the
     primitives above (initMCQ/initGapFill/initErrorSpot/initMatching
     etc. are unchanged). These let every lesson/test file stay a
     thin HTML skeleton + one JS data object, instead of hand-writing
     near-identical markup 24 times (20 lessons + 4 tests) — the
     exact same widgets and interaction rules from the original
     course, just generated from data rather than copy-pasted.
     ============================================================ */

  function esc(s){ return (s ?? '').toString().replace(/</g, '&lt;'); }
  function vocabSpan(key, text){ return `<span class="vocab" data-word="${key}">${text}</span>`; }
  function gramSpan(key, text){ return `<span class="gram" data-gram="${key}">${text}</span>`; }

  /* ---------------- Renders a numbered list of MCQ questions into a
     root container from data, wiring initMCQ per question. Restores
     prior answers from a sectionMap when provided. ---------------- */
  function renderMCQList(rootId, items, {lessonId, sectionPrefix}){
    const root = document.getElementById(rootId);
    if (!root) return;
    const sectionMap = getSectionMap(lessonId);
    root.innerHTML = items.map((item, i) => {
      const opts = shuffleArray(item.options);
      return `
      <div style="margin-bottom:18px" id="${rootId}-q${i+1}-wrap">
        <p style="margin-bottom:8px;font-weight:550">${i+1}. ${item.prompt}</p>
        <div id="${rootId}-q${i+1}">
          ${opts.map(o => `<button class="opt" data-value="${esc(o.value ?? o.label)}">${o.label}</button>`).join('')}
        </div>
      </div>`;
    }).join('');
    const positionItems = [];
    items.forEach((item, i) => {
      const sectionId = `${sectionPrefix}-${i+1}`;
      const correctOpt = item.options.find(o => o.correct);
      const correctValue = correctOpt.value ?? correctOpt.label;
      const restore = sectionMap[sectionId];
      initMCQ(`${rootId}-q${i+1}`, {
        lessonId, sectionId, correctValue,
        restoreAnswer: restore ? restore.answer_given : null
      });
      positionItems.push({ containerId: `${rootId}-q${i+1}`, correctValue });
    });
    ensureAnswerPositionVariety(positionItems);
  }

  /* ---------------- Renders a numbered list of gap-fill questions.
     item: { before, after, answers: [...], hint (bool) } ---------------- */
  function renderGapFillList(rootId, items, {lessonId, sectionPrefix}){
    const root = document.getElementById(rootId);
    if (!root) return;
    const sectionMap = getSectionMap(lessonId);
    root.innerHTML = items.map((item, i) => `
      <div style="margin-bottom:18px">
        <p style="margin-bottom:8px">${i+1}. ${item.before} <input type="text" id="${rootId}-in${i+1}" placeholder="type here" style="border:1px solid var(--border-strong);border-radius:8px;padding:6px 10px;font-family:inherit;width:${item.width || 170}px"> ${item.after || ''}</p>
        <button class="btn btn-sm" id="${rootId}-chk${i+1}">Check</button>
        <div id="${rootId}-fb${i+1}"></div>
      </div>`).join('');
    items.forEach((item, i) => {
      const sectionId = `${sectionPrefix}-${i+1}`;
      const restoreRow = sectionMap[sectionId];
      const answers = item.contractible === false ? item.answers : withContractions(item.answers);
      initGapFill(`${rootId}-in${i+1}`, `${rootId}-chk${i+1}`, `${rootId}-fb${i+1}`, {
        lessonId, sectionId, correctAnswers: answers, showAnswerHint: !!item.hint,
        restore: restoreRow ? { answerGiven: restoreRow.answer_given, isCorrect: restoreRow.override_correct ?? restoreRow.is_correct } : null
      });
    });
  }

  /* ---------------- Sentence builder: tap chips (in a shuffled bank)
     in the correct order. round: { words: [...correctOrderWords] } —
     the bank is shuffled from these words; success = rebuilding the
     exact order. Multiple rounds rendered together. ---------------- */
  function renderBuilders(rootId, rounds, {lessonId, sectionPrefix}){
    const root = document.getElementById(rootId);
    if (!root) return;
    const sectionMap = getSectionMap(lessonId);
    root.innerHTML = rounds.map((r, i) => `
      <div style="margin-bottom:20px" id="${rootId}-r${i+1}">
        <p style="font-size:12px;font-weight:650;text-transform:uppercase;letter-spacing:.03em;color:var(--text-tertiary);margin-bottom:8px">Round ${i+1}</p>
        <div class="builder-target" id="${rootId}-target${i+1}"></div>
        <div class="builder-bank" id="${rootId}-bank${i+1}" style="margin-top:10px"></div>
        <div style="margin-top:10px;display:flex;gap:8px">
          <button class="btn btn-ghost btn-sm" id="${rootId}-reset${i+1}">↺ Reset</button>
          <button class="btn btn-primary btn-sm" id="${rootId}-check${i+1}" disabled>Check order</button>
        </div>
        <div id="${rootId}-fb${i+1}" style="margin-top:8px"></div>
      </div>`).join('');

    rounds.forEach((r, i) => {
      const sectionId = `${sectionPrefix}-${i+1}`;
      const bankEl = document.getElementById(`${rootId}-bank${i+1}`);
      const targetEl = document.getElementById(`${rootId}-target${i+1}`);
      const fbEl = document.getElementById(`${rootId}-fb${i+1}`);
      const resetBtn = document.getElementById(`${rootId}-reset${i+1}`);
      const checkBtn = document.getElementById(`${rootId}-check${i+1}`);
      const restoreRow = sectionMap[sectionId];
      let placed = []; // [{ w, idx }]
      let done = false;
      let dragFromPos = null;

      function normalize(s){ return s.toLowerCase().replace(/[.!?]+$/, '').replace(/\s+/g,' ').trim(); }

      function updateCheckState(){
        checkBtn.disabled = done || placed.length !== r.words.length;
      }

      function finish(){
        done = true;
        const built = placed.map(p => p.w).join(' ');
        const correct = normalize(built) === normalize(r.words.join(' '));
        fbEl.innerHTML = correct
          ? `<div class="fb-ok">✓ Correct!</div>`
          : `<div class="fb-no">Not quite. A correct order: "${r.words.join(' ')}"</div>`;
        logProgress({ lessonId, sectionId, answerGiven: built, isCorrect: correct });
        [...bankEl.children].forEach(c => c.style.pointerEvents = 'none');
        checkBtn.disabled = true;
        resetBtn.style.display = 'none';
        renderTarget();
      }

      function renderBank(bankWords){
        bankEl.innerHTML = '';
        bankWords.forEach(item => {
          const chip = document.createElement('button');
          chip.type = 'button';
          chip.className = 'chip';
          chip.textContent = item.w;
          if (placed.some(p => p.idx === item.idx)) chip.classList.add('used');
          chip.addEventListener('click', () => {
            if (done || chip.classList.contains('used')) return;
            chip.classList.add('used');
            placed.push(item);
            renderTarget();
            updateCheckState();
          });
          bankEl.appendChild(chip);
        });
      }

      // Placed chips can be dragged to swap their order — so a course
      // taker who needs to fix the order of two words doesn't have to
      // send them back to the bank and re-place them from scratch.
      function renderTarget(){
        targetEl.innerHTML = '';
        placed.forEach((item, pos) => {
          const chip = document.createElement('span');
          chip.className = 'chip';
          chip.textContent = item.w;
          if (!done){
            chip.draggable = true;
            chip.addEventListener('dragstart', (e) => {
              dragFromPos = pos;
              chip.classList.add('dragging');
              e.dataTransfer.effectAllowed = 'move';
              e.dataTransfer.setData('text/plain', String(pos));
            });
            chip.addEventListener('dragend', () => {
              chip.classList.remove('dragging');
              dragFromPos = null;
            });
            chip.addEventListener('dragover', (e) => {
              e.preventDefault();
              e.dataTransfer.dropEffect = 'move';
              chip.classList.add('drag-over');
            });
            chip.addEventListener('dragleave', () => chip.classList.remove('drag-over'));
            chip.addEventListener('drop', (e) => {
              e.preventDefault();
              chip.classList.remove('drag-over');
              const fromPos = dragFromPos !== null ? dragFromPos : Number(e.dataTransfer.getData('text/plain'));
              if (Number.isNaN(fromPos) || fromPos === pos) return;
              const [moved] = placed.splice(fromPos, 1);
              placed.splice(pos, 0, moved);
              renderTarget();
            });
          }
          targetEl.appendChild(chip);
        });
      }

      resetBtn.addEventListener('click', () => {
        placed = [];
        done = false;
        fbEl.innerHTML = '';
        renderBank(shuffleArray(r.words.map((w, idx) => ({ w, idx }))));
        renderTarget();
        updateCheckState();
      });

      checkBtn.addEventListener('click', () => {
        if (checkBtn.disabled) return;
        finish();
      });

      if (restoreRow){
        placed = r.words.map((w, idx) => ({ w, idx }));
        done = true;
        renderTarget();
        const correct = restoreRow.override_correct ?? restoreRow.is_correct;
        fbEl.innerHTML = correct ? `<div class="fb-ok">✓ Correct!</div>` : `<div class="fb-no">A correct order: "${r.words.join(' ')}"</div>`;
        bankEl.innerHTML = '';
        checkBtn.disabled = true;
        resetBtn.style.display = 'none';
      } else {
        renderBank(shuffleArray(r.words.map((w, idx) => ({ w, idx }))));
        updateCheckState();
      }
    });
  }

  /* ---------------- Categorise: read a prompt, tap which category it
     belongs to (2-4 category buttons). items: [{prompt, correct,
     categories:[...]}] — categories list is shared across all items
     unless overridden per item. ---------------- */
  function renderCategorise(rootId, items, categories, {lessonId, sectionPrefix}){
    const root = document.getElementById(rootId);
    if (!root) return;
    const sectionMap = getSectionMap(lessonId);
    root.innerHTML = items.map((item, i) => {
      const cats = item.categories || categories;
      return `
      <div style="margin-bottom:18px">
        <p style="margin-bottom:8px;font-weight:550">${i+1}. ${item.prompt}</p>
        <div id="${rootId}-q${i+1}">
          ${cats.map(c => `<button class="opt" data-value="${esc(c)}">${c}</button>`).join('')}
        </div>
      </div>`;
    }).join('');
    const positionItems = [];
    items.forEach((item, i) => {
      const sectionId = `${sectionPrefix}-${i+1}`;
      const restore = sectionMap[sectionId];
      initMCQ(`${rootId}-q${i+1}`, {
        lessonId, sectionId, correctValue: item.correct,
        restoreAnswer: restore ? restore.answer_given : null
      });
      positionItems.push({ containerId: `${rootId}-q${i+1}`, correctValue: item.correct });
    });
    ensureAnswerPositionVariety(positionItems);
  }

  /* ---------------- Hoverable compare cards (shared across every
     lesson's concept section — same tooltip element, positioning and
     "click outside to close" handling everywhere). ---------------- */
  function ensureCompareTooltip(){
    let el = document.getElementById('compare-tooltip');
    if (!el){
      el = document.createElement('div');
      el.id = 'compare-tooltip';
      document.body.appendChild(el);
    }
    return el;
  }
  let compareTooltipEl = null;
  function showCompareTooltip(html, anchorEl){
    if (!compareTooltipEl) compareTooltipEl = ensureCompareTooltip();
    compareTooltipEl.innerHTML = html;
    const rect = anchorEl.getBoundingClientRect();
    const scrollY = window.scrollY || document.documentElement.scrollTop;
    const scrollX = window.scrollX || document.documentElement.scrollLeft;
    compareTooltipEl.style.top = `${rect.bottom + scrollY + 8}px`;
    compareTooltipEl.style.left = `${rect.left + scrollX}px`;
    compareTooltipEl.classList.add('visible');
  }
  function hideCompareTooltip(){
    if (compareTooltipEl) compareTooltipEl.classList.remove('visible');
  }
  document.addEventListener('click', (e) => {
    // Recognises BOTH .trait-pill and .compare-box — checking only one
    // class causes the other's tooltip to flicker open and immediately
    // slam shut on click (a real bug from the original course, fixed
    // by checking both here, once, centrally).
    if (!e.target.closest('.trait-pill') && !e.target.closest('.compare-box')) hideCompareTooltip();
  });
  function renderCompareCard(containerId, items){
    const el = document.getElementById(containerId);
    if (!el) return;
    // Each row is a CSS Grid (not an independent flex container) so the
    // label/box columns line up across every row regardless of how long
    // any one row's text is. flex-wrap here previously let each row
    // decide, on its own, whether its label+box fit on one line — since
    // that decision depends on that row's own text length, rows with
    // shorter text stayed inline while longer ones wrapped, staggering
    // the boxes out of alignment with each other.
    el.innerHTML = items.map(it => `
      <div class="compare-row" style="margin-bottom:${it.groupEnd ? 20 : 8}px">
        <span style="font-size:11px;text-transform:uppercase;letter-spacing:.03em;color:var(--text-tertiary)">${it.label}</span>
        <span class="compare-box" data-key="${it.key}">"${it.text}"</span>
      </div>
    `).join('');
    el.querySelectorAll('.compare-box').forEach((node, i) => {
      const html = `<div>${items[i].explain}</div>`;
      node.addEventListener('mouseenter', () => showCompareTooltip(html, node));
      node.addEventListener('mouseleave', hideCompareTooltip);
      node.addEventListener('click', () => showCompareTooltip(html, node));
    });
  }

  /* ---------------- The "browse / quiz" concept widget (generalised
     from the original course's modal-verbs widget): N category tabs,
     each holding a list of {label, example} items to click through in
     Structure/Examples mode, plus a Quick check mode that quizzes
     "which category does this belong to." The quiz prompt is always
     just the label/example text, never restating the category name,
     so it can't be answered by text-matching alone. When several
     widgets on one page share a single "Show the full rules" toggle,
     pass a shared `tracker` object + `rulesToggleId` so the button
     only re-enables once every widget sharing it has left quiz mode. ---------------- */
  function renderConceptWidget({areaId, hintId, tabIds, categories, quizLabels, rulesToggleId, tracker, trackerKey}){
    let cat = Object.keys(categories)[0];
    let idx = {};
    Object.keys(categories).forEach(k => idx[k] = 0);
    const areaEl = document.getElementById(areaId);
    const hintEl = hintId ? document.getElementById(hintId) : null;
    const quizPool = Object.entries(categories).flatMap(([key, items]) => items.map(it => ({ ...it, cat: key })));

    function renderBrowse(){
      const items = categories[cat];
      const canCycle = items.length > 1;
      if (hintEl){ hintEl.style.display = canCycle ? 'block' : 'none'; }
      const item = items[idx[cat]];
      areaEl.innerHTML = `
        <div style="overflow-x:auto;padding-bottom:2px">
          <div style="display:grid;grid-template-columns:1fr 1.6fr;gap:10px;align-items:center;min-width:380px">
            <div class="static-cell is-primary-cell${canCycle ? ' clickable-cell' : ''}">${item.label}</div>
            <div class="static-cell is-primary-cell${canCycle ? ' clickable-cell' : ''}">${item.example}</div>
          </div>
        </div>`;
      if (canCycle){
        areaEl.querySelectorAll('.clickable-cell').forEach(c => {
          c.addEventListener('click', () => { idx[cat] = (idx[cat] + 1) % items.length; renderBrowse(); });
        });
      }
    }

    function renderQuiz(){
      if (hintEl) hintEl.style.display = 'none';
      areaEl.innerHTML = `
        <p id="${areaId}-word" style="font-size:16.5px;font-weight:650;text-align:center;color:var(--accent);margin-bottom:10px;line-height:1.5"></p>
        <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap" id="${areaId}-options">
          ${Object.keys(categories).map(k => `<button class="opt" data-answer="${k}" style="flex:0 1 auto">${quizLabels[k]}</button>`).join('')}
        </div>
        <div id="${areaId}-fb" style="text-align:center;min-height:16px;margin-top:8px;font-size:13.5px"></div>
        <div style="text-align:center;margin-top:10px"><button class="btn btn-primary" id="${areaId}-next" style="display:none">Next →</button></div>`;
      let order = shuffleArray(quizPool.map((_, i) => i));
      let pos = 0, answered = false;
      const wordEl = document.getElementById(`${areaId}-word`);
      const optionsEl = document.getElementById(`${areaId}-options`);
      const fbEl = document.getElementById(`${areaId}-fb`);
      const nextBtn = document.getElementById(`${areaId}-next`);
      function renderQ(){
        answered = false; fbEl.textContent = ''; nextBtn.style.display = 'none';
        wordEl.textContent = quizPool[order[pos]].label;
        [...optionsEl.children].forEach(b => b.className = 'opt');
      }
      optionsEl.querySelectorAll('button').forEach(btn => {
        btn.addEventListener('click', () => {
          if (answered) return;
          answered = true;
          const item = quizPool[order[pos]];
          const correct = btn.dataset.answer === item.cat;
          [...optionsEl.children].forEach(b => {
            if (b === btn) b.classList.add(correct ? 'ok' : 'bad');
            else if (b.dataset.answer === item.cat) b.classList.add('ok');
            else b.classList.add('dim');
          });
          fbEl.innerHTML = correct
            ? `<span style="color:var(--ok)">✓ Correct! "${item.label}" is ${quizLabels[item.cat]}.</span>`
            : `<span style="color:var(--bad)">Not quite — "${item.label}" is ${quizLabels[item.cat]}.</span>`;
          nextBtn.style.display = 'inline-block';
        });
      });
      nextBtn.addEventListener('click', () => {
        pos += 1;
        if (pos >= order.length){ order = shuffleArray(quizPool.map((_, i) => i)); pos = 0; }
        renderQ();
      });
      renderQ();
    }

    function updateRulesToggle(){
      if (!rulesToggleId) return;
      if (tracker && trackerKey) tracker[trackerKey] = cat === 'quiz';
      const anyQuizActive = tracker ? Object.values(tracker).some(Boolean) : cat === 'quiz';
      const btn = document.getElementById(rulesToggleId);
      const content = document.getElementById('rules-content');
      if (!btn) return;
      if (anyQuizActive){
        btn.disabled = true; btn.textContent = 'Rules hidden during the quick check';
        if (content) content.classList.remove('open');
      } else {
        btn.disabled = false;
        const isOpen = content && content.classList.contains('open');
        btn.textContent = isOpen ? 'Hide the full rules' : 'Show the full rules';
      }
    }
    function switchCat(newCat){
      cat = newCat;
      tabIds.forEach(t => document.getElementById(t.id).classList.toggle('on', t.key === newCat));
      if (newCat === 'quiz') renderQuiz(); else renderBrowse();
      updateRulesToggle();
    }
    tabIds.forEach(t => document.getElementById(t.id).addEventListener('click', () => switchCat(t.key)));
    if (rulesToggleId){
      const rulesBtn = document.getElementById(rulesToggleId);
      const rulesContent = document.getElementById('rules-content');
      if (rulesBtn){
        rulesBtn.addEventListener('click', () => {
          if (rulesBtn.disabled) return;
          if (rulesContent) rulesContent.classList.toggle('open');
          updateRulesToggle();
        });
      }
    }
    switchCat(cat);
    return { switchCat };
  }

  /* ---------------- Listening dialogue: sequential speechSynthesis
     playback (two alternating voices/pitches for the two speakers),
     transcript lines revealing one-by-one during playback (or all at
     once via "Show full transcript"), and the zero-height-until-shown
     transcript container from theme.css. ---------------- */
  // Per-lesson combined dialogue audio (one MP3 per lesson, stitched by
  // generate_audio.py) + a small sidecar JSON of {start,end} seconds per
  // line, used to drive the same "reveal line as it's spoken" UX as the
  // speechSynthesis fallback, but timed against the real recording.
  // File-first with a cached fetch(HEAD) check, exactly like speakSmart —
  // missing files (nothing generated yet) transparently fall back to the
  // per-line speechSynthesis loop with zero code changes needed later.
  const dialogueAudioCache = new Map(); // shortPrefix -> {mp3, timings}|false
  async function checkDialogueAudio(shortPrefix){
    if (dialogueAudioCache.has(shortPrefix)) return dialogueAudioCache.get(shortPrefix);
    const mp3 = `audio/${shortPrefix}-listening.mp3`;
    const jsonUrl = `audio/${shortPrefix}-listening.json`;
    let result = false;
    try {
      const res = await fetch(mp3, { method: 'HEAD' });
      if (res.ok){
        const timingRes = await fetch(jsonUrl);
        const timings = timingRes.ok ? await timingRes.json() : null;
        result = { mp3, timings };
      }
    } catch (e){ result = false; }
    dialogueAudioCache.set(shortPrefix, result);
    return result;
  }

  function initListening({dialogue, speakerA, speakerB, lessonId}){
    const audioEl = document.getElementById('dialogue-audio');
    const playBtn = document.getElementById('play-dialogue');
    const stopBtn = document.getElementById('stop-dialogue');
    const showBtn = document.getElementById('show-transcript');
    const transcriptEl = document.getElementById('transcript');
    if (!playBtn) return;

    transcriptEl.innerHTML = dialogue.map((line, i) =>
      `<div class="transcript-line" data-idx="${i}"><b>${esc(line.speaker)}:</b> ${esc(line.line)}</div>`
    ).join('');
    const lineEls = transcriptEl.querySelectorAll('.transcript-line');
    // "lesson-01" from "b2c1-lesson-01-narrative-tenses" — matches the
    // short-prefix convention every other generated filename already uses.
    const shortPrefixMatch = (lessonId || '').match(/^weq-(lesson-\d+)/);
    const shortPrefix = shortPrefixMatch ? shortPrefixMatch[1] : lessonId;

    // Transcript stays fully hidden until "Show full transcript" is
    // pressed, exactly like the original course — playback only ever
    // highlights the current line (via .active), it never auto-reveals
    // text, so listening practice stays an actual listening exercise.
    let transcriptShown = false;
    function setTranscriptShown(shown){
      transcriptShown = shown;
      lineEls.forEach(l => l.classList.toggle('shown', shown));
      transcriptEl.classList.toggle('expanded', shown);
      showBtn.textContent = shown ? 'Hide transcript' : 'Show full transcript';
    }

    // ---- Mode state: resolved once (real audio file vs. speechSynthesis
    // fallback), then the single Play/Pause button drives whichever mode
    // is active, matching the original course's toggle-button pattern
    // (no separate pause button — the Play button becomes Pause/Resume). ----
    let audioInfo = null;      // {mp3, timings} | false, once resolved
    let mode = null;           // 'audio' | 'tts', once resolved
    let isPlaying = false;
    let currentIdx = 0;        // tts mode: which line we're on/resuming from
    let finished = false;

    function updateButtonLabel(){
      if (isPlaying){ playBtn.textContent = 'Pause'; return; }
      if (mode === 'tts' && window.speechSynthesis && window.speechSynthesis.paused){ playBtn.textContent = 'Resume'; return; }
      if (mode === 'audio' && audioEl && audioEl.currentTime > 0 && !finished){ playBtn.textContent = 'Resume'; return; }
      playBtn.textContent = 'Play dialogue';
    }

    function setActiveLine(idx){
      lineEls.forEach(l => l.classList.remove('active'));
      if (idx >= 0 && idx < lineEls.length){
        lineEls[idx].classList.add('active');
        if (transcriptShown) lineEls[idx].scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    }

    function resetToStart(){
      isPlaying = false;
      finished = false;
      currentIdx = 0;
      if ('speechSynthesis' in window) window.speechSynthesis.cancel();
      if (audioEl){ audioEl.pause(); audioEl.currentTime = 0; }
      lineEls.forEach(l => l.classList.remove('active'));
      updateButtonLabel();
    }

    /* ---- speechSynthesis mode: recursive line-by-line playback so
       pause/resume can work mid-dialogue (speechSynthesis.pause() only
       pauses the utterance in flight; resume() continues it). ---- */
    function speakLineAt(idx){
      if (idx >= dialogue.length){
        isPlaying = false; finished = true; currentIdx = 0;
        lineEls.forEach(l => l.classList.remove('active'));
        updateButtonLabel();
        return;
      }
      currentIdx = idx;
      setActiveLine(idx);
      if (!('speechSynthesis' in window)){
        setTimeout(() => { if (isPlaying) speakLineAt(idx + 1); }, 900);
        return;
      }
      const u = new SpeechSynthesisUtterance(dialogue[idx].line);
      u.rate = 0.95;
      u.pitch = dialogue[idx].speaker === speakerA ? 1.15 : 0.85;
      u.onend = () => { if (isPlaying) speakLineAt(idx + 1); };
      u.onerror = () => { if (isPlaying) speakLineAt(idx + 1); };
      window.speechSynthesis.speak(u);
    }

    function onAudioTimeUpdate(){
      const timings = audioInfo && audioInfo.timings;
      if (!timings) return;
      const t = audioEl.currentTime;
      const idx = timings.findIndex(seg => t >= seg.start && t < seg.end);
      if (idx === -1) return;
      setActiveLine(idx);
    }
    function onAudioEnded(){
      isPlaying = false; finished = true;
      lineEls.forEach(l => l.classList.remove('active'));
      updateButtonLabel();
    }

    async function togglePlay(){
      // Resolve mode once, on first press.
      if (mode === null){
        audioInfo = shortPrefix ? await checkDialogueAudio(shortPrefix) : false;
        mode = audioInfo ? 'audio' : 'tts';
        if (mode === 'audio'){
          audioEl.src = audioInfo.mp3;
          audioEl.addEventListener('timeupdate', onAudioTimeUpdate);
          audioEl.addEventListener('ended', onAudioEnded);
          audioEl.addEventListener('error', onAudioEnded);
        }
      }

      if (mode === 'audio'){
        if (finished){ resetToStart(); }
        if (audioEl.paused){
          isPlaying = true;
          audioEl.play().catch(onAudioEnded);
        } else {
          isPlaying = false;
          audioEl.pause();
        }
        updateButtonLabel();
        return;
      }

      // tts mode
      if (!isPlaying){
        isPlaying = true;
        if (finished) currentIdx = 0;
        finished = false;
        if (window.speechSynthesis.paused){
          window.speechSynthesis.resume();
        } else {
          // Defensive reset, fresh-start only (never on resume/pause):
          // speechSynthesis has a well-documented browser bug where it
          // can silently stop accepting new speech after earlier calls
          // elsewhere on the page (e.g. the vocab-word audio buttons).
          window.speechSynthesis.cancel();
          speakLineAt(currentIdx);
        }
      } else {
        isPlaying = false;
        window.speechSynthesis.pause();
      }
      updateButtonLabel();
    }

    playBtn.addEventListener('click', togglePlay);
    stopBtn.addEventListener('click', resetToStart);
    showBtn.addEventListener('click', () => setTranscriptShown(!transcriptShown));
  }

  /* ---------------- Speaking: solo/group mode toggle + the solo
     "I've done this" mark, which is a real toggle (restorable, and can
     be switched back off) rather than a one-way lock — matching the
     original course. ---------------- */
  function initSpeaking({max = 2, lessonId, sectionMap = {}, soloTaskLabel = ''} = {}){
    const soloBtn = document.getElementById('mode-solo');
    const groupBtn = document.getElementById('mode-group');
    const soloPane = document.getElementById('speak-solo');
    const groupPane = document.getElementById('speak-group');
    if (soloBtn){
      soloBtn.addEventListener('click', () => {
        soloBtn.classList.add('on'); groupBtn.classList.remove('on');
        soloPane.style.display = 'block'; groupPane.style.display = 'none';
      });
      groupBtn.addEventListener('click', () => {
        groupBtn.classList.add('on'); soloBtn.classList.remove('on');
        groupPane.style.display = 'block'; soloPane.style.display = 'none';
      });
    }
    const doneBtn = document.getElementById('solo-done-btn');
    if (doneBtn){
      let soloDone = !!(sectionMap['speaking-solo'] && sectionMap['speaking-solo'].status === 'completed');
      function renderSoloBtn(){
        doneBtn.textContent = soloDone ? '✓ Marked as done' : "✓ I've done this";
        doneBtn.classList.toggle('btn-primary', soloDone);
      }
      renderSoloBtn();
      doneBtn.addEventListener('click', () => {
        soloDone = !soloDone;
        renderSoloBtn();
        logProgress({
          lessonId, sectionId: 'speaking-solo', exerciseType: 'oral',
          status: soloDone ? 'completed' : 'not_attempted', answerGiven: soloTaskLabel
        });
      });
    }
  }

  /* Renders the group discussion-question picker AND wires it, in one
     self-contained call — restorable from sectionMap, capped at `max`
     picks. (Previously this only rendered markup, and the actual click
     wiring lived in initSpeaking — but initSpeaking always ran BEFORE
     this had rendered any buttons yet, so it found zero .discuss-q
     elements and wired nothing. Self-contained avoids that class of
     ordering bug entirely.) */
  function renderDiscussQuestions(rootId, questions, {lessonId, max = 2, sectionPrefix = 'speaking-q'} = {}){
    const root = document.getElementById(rootId);
    if (!root) return;
    const sectionMap = getSectionMap(lessonId);
    const msgEl = document.getElementById('discuss-limit-msg');
    root.innerHTML = questions.map((q, i) => `
      <button class="discuss-q" data-idx="${i}"><span class="chk"></span><span>${q}</span></button>
    `).join('');
    const buttons = [...root.querySelectorAll('.discuss-q')];
    const picked = new Set();
    buttons.forEach((b, i) => {
      const sectionId = `${sectionPrefix}${i+1}`;
      const restored = sectionMap[sectionId];
      if (restored && restored.status === 'completed'){
        picked.add(i);
        b.classList.add('picked');
      }
    });
    function setMsg(text, isWarning){
      if (!msgEl) return;
      msgEl.textContent = text;
      msgEl.style.color = isWarning ? 'var(--bad)' : '';
    }
    buttons.forEach((b, i) => {
      b.addEventListener('click', () => {
        const sectionId = `${sectionPrefix}${i+1}`;
        const isPicked = picked.has(i);
        if (isPicked){
          picked.delete(i);
          b.classList.remove('picked');
        } else {
          if (picked.size >= max){
            setMsg(`You can only pick up to ${max} — deselect one first.`, true);
            return;
          }
          picked.add(i);
          b.classList.add('picked');
        }
        setMsg(`You can select up to ${max} questions.`, false);
        logProgress({
          lessonId, sectionId, exerciseType: 'oral',
          status: isPicked ? 'not_attempted' : 'completed', answerGiven: questions[i]
        });
      });
    });
  }

  /* ---------------- Reading passage + comprehension, wired together. ---------------- */
  function initReading({passageHtml, comprehension, lessonId, sectionPrefix, vocabData}){
    const passageEl = document.getElementById('passage');
    passageEl.innerHTML = passageHtml;
    passageEl.classList.add('passage');
    const gramToggle = document.getElementById('gram-toggle');
    if (gramToggle){
      gramToggle.addEventListener('click', function(){
        const on = passageEl.classList.toggle('show-grammar');
        this.classList.toggle('on', on);
        this.textContent = on ? 'Hide key phrases' : 'Show key phrases in this text';
      });
    }
    if (vocabData) initVocab(vocabData, lessonId);
    if (comprehension && comprehension.rootId){
      renderMCQList(comprehension.rootId, comprehension.items, { lessonId, sectionPrefix });
    }
  }
  function wireGramSpans(explanations){
    document.querySelectorAll('.gram').forEach(el => {
      el.addEventListener('click', () => {
        showPopup(`<div style="font-size:14.5px;line-height:1.6">${explanations[el.dataset.gram]}</div>`, el);
      });
    });
  }

  // Wires the "Show grammar in this text" button that toggles the
  // highlight styling on every .gram span inside #passage. Split out
  // from initReading (which also re-renders the passage from a string —
  // not needed here, since lesson pages pre-render the passage HTML
  // directly) so lessons can wire just the toggle behaviour.
  function initGramToggle(){
    const passageEl = document.getElementById('passage');
    const gramToggle = document.getElementById('gram-toggle');
    if (gramToggle && passageEl){
      gramToggle.addEventListener('click', function(){
        const on = passageEl.classList.toggle('show-grammar');
        this.classList.toggle('on', on);
        this.textContent = on ? 'Hide key phrases' : 'Show key phrases in this text';
      });
    }
  }

  /* ---------------- Page chrome: nav-link group-param wiring, reset
     button, sync status, and the finish/export summary card. Every
     lesson/test calls this once, near the end of its script. ---------------- */
  function initPageChrome({lessonId, totalExercises, isTest}){
    const groupParam = new URLSearchParams(window.location.search).get('group');
    const currentFile = window.location.pathname.split('/').pop();
    const allLessonsLink = document.getElementById('all-lessons-link');
    if (allLessonsLink){
      allLessonsLink.href = groupParam ? `index-standalone.html?group=${encodeURIComponent(groupParam)}` : 'index-standalone.html';
    }
    const glossaryLink = document.getElementById('glossary-link');
    if (glossaryLink){
      let href = `glossary-standalone.html?from=${encodeURIComponent(currentFile)}`;
      if (groupParam) href += `&group=${encodeURIComponent(groupParam)}`;
      glossaryLink.href = href;
    }
  }

  async function initSyncStatus(lessonId){
    const el = document.getElementById('sync-status');
    if (el) el.textContent = supabaseClient ? `Syncing your progress…` : `Progress is saved on this device`;
    await syncFromSupabase(lessonId);
    if (el) el.textContent = supabaseClient ? `Synced · Group: ${GROUP_ID}` : `Progress is saved on this device`;
  }

  function initSummary({lessonId, totalExercises, sectionPrefixesForProgress}){
    const finishBtn = document.getElementById('finish-btn');
    const exportBtn = document.getElementById('export-btn');
    const ringHolder = document.getElementById('score-ring-holder');
    const nameEl = document.getElementById('summary-name');
    const completionEl = document.getElementById('summary-completion');
    const weakEl = document.getElementById('summary-weak');
    if (!finishBtn) return;

    function updateOverallProgress(){
      const { correct, total } = lessonScore(lessonId);
      const bar = document.getElementById('overall-progress');
      if (bar && totalExercises) bar.style.width = `${Math.min(100, Math.round((total / totalExercises) * 100))}%`;
    }
    updateOverallProgress();
    document.body.addEventListener('click', () => setTimeout(updateOverallProgress, 50), true);

    finishBtn.addEventListener('click', async () => {
      const { correct, total } = lessonScore(lessonId);
      nameEl.textContent = getStudentName();
      renderScoreRing('score-ring-holder', correct, total);
      const pct = total ? Math.round((correct/total)*100) : 0;
      if (completionEl){
        completionEl.textContent = totalExercises
          ? `${total} / ${totalExercises} exercises attempted`
          : `${total} exercises attempted`;
      }
      const weak = weakSections(lessonId);
      weakEl.textContent = total === 0
        ? 'No exercises answered yet.'
        : (weak.length ? `Review these sections: ${weak.join(', ')}` : 'Great work — no weak spots flagged!');
      document.getElementById('summary-card').classList.add('summary-pulse');
      finishBtn.style.display = 'none';
      exportBtn.style.display = 'inline-block';
    });
    exportBtn.addEventListener('click', () => {
      exportReportPDF(lessonId, document.querySelector('.lesson-title')?.textContent || lessonId, totalExercises);
    });
  }


  /* ---------------- Workplace EQ reskin additions ---------------- */
  // Tone cells: the "too blunt / just right / too stiff" comparison as
  // three columns with a formality bar. Items come in groups (groupEnd
  // closes a group); each group is shown blunt | just right | stiff.
  // Hover (desktop) or tap (touch) reveals the explanation in place.
  function renderToneCells(containerId, items){
    const el = document.getElementById(containerId);
    if (!el) return;
    const kindOf = label => { const l = (label || '').toLowerCase(); return l.includes('right') ? 'right' : (l.includes('blunt') ? 'blunt' : 'stiff'); };
    const width = { blunt: '90%', right: '50%', stiff: '15%' };
    const order = { blunt: 0, right: 1, stiff: 2 };
    const groups = []; let cur = [];
    items.forEach(it => { cur.push(it); if (it.groupEnd){ groups.push(cur); cur = []; } });
    if (cur.length) groups.push(cur);
    el.innerHTML = groups.map(g => {
      const sorted = [...g].sort((a, b) => order[kindOf(a.label)] - order[kindOf(b.label)]);
      return '<div class="tone-set">' + sorted.map(it => {
        const k = kindOf(it.label);
        return `<button type="button" class="tone-cell${k === 'right' ? ' is-right' : ''}" data-key="${it.key}" aria-expanded="false">
          <span class="tone-lbl">${esc(it.label)}</span>
          <span class="tone-bar" style="width:${width[k]}"></span>
          <span class="tone-line">"${esc(it.text)}"</span>
          <span class="tone-why">${esc(it.explain)}</span>
        </button>`;
      }).join('') + '</div>';
    }).join('');
    el.querySelectorAll('.tone-cell').forEach(c => c.addEventListener('click', () => {
      const open = c.classList.toggle('open');
      c.setAttribute('aria-expanded', open ? 'true' : 'false');
    }));
  }

  // Step tabs under the lesson header: highlight the section currently
  // in view, and keep the active tab visible when the strip scrolls
  // horizontally on small screens.
  function initStepTabs(){
    const tabs = Array.from(document.querySelectorAll('.eq-steps a[data-step]'));
    if (!tabs.length || !('IntersectionObserver' in window)) return;
    const byId = {}; tabs.forEach(t => byId[t.dataset.step] = t);
    let current = tabs[0].dataset.step;
    function setOn(id){
      if (!byId[id] || id === current) return;
      current = id;
      tabs.forEach(t => t.classList.toggle('on', t.dataset.step === id));
      const strip = byId[id].parentElement;
      if (strip && strip.scrollWidth > strip.clientWidth) strip.scrollTo({ left: byId[id].offsetLeft - 20, behavior: 'smooth' });
    }
    const obs = new IntersectionObserver(entries => {
      entries.filter(e => e.isIntersecting).forEach(e => setOn(e.target.id));
    }, { rootMargin: '-45% 0px -50% 0px' });
    document.querySelectorAll('section.eq-sec[id]').forEach(s => { if (byId[s.id]) obs.observe(s); });
  }

  return { logProgress, getLessonRows, getCurrentRows, getSectionMap, lessonScore, weakSections, exportReport, exportReportPDF,
           speak, speakSmart, initVocab, initMCQ, initGapFill, initErrorSpot, initMatching, withContractions, renderScoreRing, getStudentName,
           shuffleArray, shuffleOptions, ensureAnswerPositionVariety, showPopup, hidePopup, resetLocalProgress, syncFromSupabase,
           getGlossary, saveToGlossary, removeFromGlossary, syncGlossaryFromSupabase,
           getGroupId: () => GROUP_ID, isConnected: () => !!supabaseClient, renderToneCells, initStepTabs,
           vocabSpan, gramSpan, renderMCQList, renderGapFillList, renderBuilders, renderCategorise,
           renderCompareCard, showCompareTooltip, hideCompareTooltip, renderConceptWidget,
           initListening, initSpeaking, renderDiscussQuestions, initReading, wireGramSpans, initGramToggle,
           initPageChrome, initSyncStatus, initSummary };
})();
