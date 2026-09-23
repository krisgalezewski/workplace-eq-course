# Workplace EQ

*The unwritten rules of professional presence, communication, and career velocity.*

A 7-lesson B2–C1 course by English Voiced with Kris. It teaches British workplace norms and flags US and international differences as it goes. It's built on the same generator and engine as the English+ B2+/C1 grammar course.

## Course plan

| # | Section | Lesson | Core content |
|---|---------|--------|--------------|
| 1 | Professional Presence | **First Impressions & Small Talk** ✅ | Introductions, names and titles (no "Mr + first name"), safe and unsafe topics, keeping a conversation going, leaving gracefully |
| 2 | Professional Presence | Politeness & Register | Indirectness, softening requests ("I was wondering if…"), distancing with past tense, British understatement, and "too blunt / too stiff / just right" |
| 3 | Communication That Lands | Emails & Messaging | Openings and closings, a formality scale, chasing politely, apologising for delays, CC/BCC/Reply All, Slack/Teams norms |
| 4 | Communication That Lands | Meetings & Calls | Interrupting politely, taking and handing back the floor, disagreeing diplomatically, keeping on track, video-call etiquette |
| 5 | Communication That Lands | Difficult Conversations | Saying no, apologising, complaining, giving and receiving feedback, bad news, helping people save face |
| 6 | Career Velocity | Visibility & Self-Advocacy | Taking credit gracefully, managing up, asking for a raise or stretch project, networking follow-up, hierarchy across cultures |
| 7 | Career Velocity | Capstone: A Week in London | One scenario that uses all six lessons: arrival, team intro, client dinner, a tense meeting, a follow-up email |
| – | – | Final test | Covers Lessons 1–7 |

The standalone englishvoiced.com lesson (Practical use of English) covers the same six areas as a quick overview, and each of its areas links to the matching course lesson.

## Differences from the grammar course

- Lesson ids use the `weq-` prefix. The course shares the grammar courses' Supabase project, and the ids can't collide.
- localStorage keys are `workplaceeq_*`, so progress, the glossary and the student name stay separate from the grammar courses, which are served from the same origin.
- The reading's `gram()` highlights mark **key phrases**. The toggle reads "Show key phrases in this text".
- Error-spot items can take `explanation` instead of `correction`. The engine then shows "✓ Spotted it — …", which suits faux-pas items.
- Rules panels end with a `🌍 Elsewhere` tip box for US and international notes.
- Tests have an `after_section` key, so a section can have zero or more tests.

## Build

```bash
python3 build.py            # generates lesson/test/index/glossary/dashboard HTML (+ standalone versions)
python3 generate_audio.py   # optional: Google TTS audio (needs GOOGLE_TTS_API_KEY); the browser's voice is used until then
```
