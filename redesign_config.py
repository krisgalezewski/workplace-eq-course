# -*- coding: utf-8 -*-
"""2026 redesign (Claude Design handoff "English+ course redesign").

Course-overview copy and art, the word chips shown on lesson tiles and
lesson heroes, and the section colours. Used by build.py; the lesson-page
chrome reads its own copy of the chips from the REDESIGN CHROME block at
the end of shared/course-engine.js.

Chip kinds: s = solid cream, o = outlined, x = dashed, d = dim.
"""

OVERVIEW_TOP = "English Voiced · Workplace EQ · B2–C1 · by Kris Galezewski"
OVERVIEW_LABELS = ["English Voiced", "Workplace EQ", "B2–C1"]
INDEX_HEADING = "Workplace EQ"
WELCOME_COPY = "The unwritten rules of professional presence, communication, and career velocity. Your grammar can be perfect and you can still sound rude, cold or junior. This course is about the other half: what British colleagues actually mean, what they expect to hear, and how to say it (with notes on US and international norms along the way)."
OVERVIEW_ART = "<div style=\"display:flex;flex-direction:column;gap:10px;align-items:flex-end;font-family:'Archivo';font-weight:800\">\n          <div style=\"display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:flex-end\"><span style=\"padding:4px 12px;border-radius:999px;border:1.5px dashed rgba(246,238,221,.7);font-size:18px\">“Mr Tom”</span><span style=\"font-size:18px;opacity:.6\">→</span><span style=\"padding:5px 12px;border-radius:9px;background:#F6EEDD;color:#17614F;font-size:18px\">“Tom”</span></div>\n          <div style=\"display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:flex-end\"><span style=\"padding:4px 12px;border-radius:999px;border:1.5px solid rgba(246,238,221,.7);font-size:18px\">small talk</span><span style=\"padding:5px 12px;border-radius:9px;background:rgba(0,0,0,.2);font-size:18px\">register</span></div>\n          <div style=\"display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:flex-end\"><span style=\"padding:5px 12px;border-radius:9px;background:#3A8597;color:#F6EEDD;font-size:18px\">rapport</span></div>\n          <div style=\"display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:flex-end\"><span style=\"padding:5px 12px;border-radius:9px;background:#7D8B36;color:#F6EEDD;font-size:18px\">Lovely to meet you.</span></div>\n        </div>"
LESSON_CHIPS = {
    1: [["Mr Tom", "o"], ["Tom", "s"]],
    2: [["Could you…?", "s"], ["Do it.", "d"]],
    3: [["Hi Tom,", "s"], ["Best,", "o"]],
    4: [["Can I just come in here?", "s"]],
    5: [["I hear you, but…", "s"]],
    6: [["I led", "s"], ["we", "o"]],
    7: [["Mon", "o"], ["Wed", "d"], ["Fri", "s"]],
}

# main / deep colour per section, in section order
SECTION_COLORS = [{"color": "#17614F", "deep": "#0C3E33"}, {"color": "#1D6475", "deep": "#113F4A"}, {"color": "#5E6B1F", "deep": "#3B4412"}]
