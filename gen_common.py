"""
Workplace EQ course — generator common utilities.

This mirrors the original course's architecture described in the
handoff brief: every lesson/test is authored as a lean HTML skeleton
(references shared/theme.css + shared/course-engine.js) plus a small
per-lesson JS data object that drives the shared, data-driven
renderers added to course-engine.js (renderMCQList, renderGapFillList,
renderBuilders, renderConceptWidget, initListening, etc.) — instead of
hand-writing near-identical markup 24 times over.

rebuild_standalone() is the generic string-replacement rebuild script
described in the handoff (§2): swaps the theme.css <link> for an
inlined <style>, and the two shared <script src="shared/..."> tags for
inlined <script> blocks. Works identically for lessons, tests, index,
glossary and the teacher dashboard.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SHARED = os.path.join(ROOT, "shared")

FONT_LINK = '<link rel="stylesheet" href="/fonts/fonts.css">'  # self-hosted, see /fonts/fonts.css on englishvoiced.com
SUPABASE_CDN = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>'


def j(data):
    """Compact JS-literal-safe JSON dump (used to embed lesson DATA objects)."""
    return json.dumps(data, ensure_ascii=False)


ATTRIBUTION = "Workplace EQ · B2–C1 · English Voiced with Kris"


def top_nav(left="Workplace EQ", links_html=None):
    """Top bar of the glossary and teacher-dashboard pages."""
    if links_html is None:
        links_html = (
            '<a id="all-lessons-link" href="index-standalone.html">All lessons</a>'
            '<a id="glossary-link" href="glossary-standalone.html">My glossary</a>'
        )
    return f'''<div class="eq-nav"><div class="eq-wrap">
  <span>{left}</span><span class="eq-nav-links">{links_html}</span>
</div></div>'''


def nav_header(eyebrow, title, sub, is_test=False, section_name="", steps=None):
    """Lesson/test header. The redesign chrome in course-engine.js turns it
    into the coloured hero + sticky section menu. Keeps the ids the engine
    relies on: all-lessons-link, glossary-link, overall-progress, sync-status."""
    links = '<a id="all-lessons-link" href="index-standalone.html" class="pill">All lessons</a>'
    if not is_test:
        links += '\n      <a id="glossary-link" href="glossary-standalone.html" class="pill">My glossary</a>'
    if section_name:
        eyebrow = f"{eyebrow} · {section_name}"
    return f'''  <header class="lesson-header">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap">
      <div class="lesson-eyebrow">{eyebrow}</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
      {links}
    </div>
    </div>
    <h1 class="lesson-title">{title}</h1>
    <p class="lesson-sub">{sub}</p>
    <div class="pb-track" style="margin-top:16px"><div class="pb-fill" id="overall-progress" style="width:0%"></div></div>
    <div id="sync-status" style="font-size:11.5px;color:var(--text-tertiary);margin-top:8px"></div>
  </header>'''


def page_shell(*, title, theme_class, body_html, extra_head="", page_script=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<script defer src="/analytics.js"></script>
<title>{title} | Workplace EQ</title>
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16.png">
<link rel="apple-touch-icon" href="assets/favicon-180.png">
{FONT_LINK}
<link rel="stylesheet" href="shared/theme.css">
{extra_head}
{SUPABASE_CDN}
<script src="shared/supabase-config.js"></script>
</head>
<body class="{theme_class}">

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


def rebuild_standalone(source_path, output_path):
    """Generic rebuild: inline shared/theme.css and shared/course-engine.js
    (and shared/supabase-config.js) into a single self-contained file.
    Pure string replacement — works for any page built with page_shell()."""
    with open(source_path, "r", encoding="utf-8") as f:
        html = f.read()

    with open(os.path.join(SHARED, "theme.css"), "r", encoding="utf-8") as f:
        theme_css = f.read()
    with open(os.path.join(SHARED, "course-engine.js"), "r", encoding="utf-8") as f:
        engine_js = f.read()
    with open(os.path.join(SHARED, "supabase-config.js"), "r", encoding="utf-8") as f:
        supabase_js = f.read()

    html = html.replace(
        '<link rel="stylesheet" href="shared/theme.css">',
        f"<style>\n{theme_css}\n</style>",
        1,
    )
    html = html.replace(
        '<script src="shared/supabase-config.js"></script>',
        f"<script>\n{supabase_js}\n</script>",
        1,
    )
    html = html.replace(
        '<script src="shared/course-engine.js"></script>',
        f"<script>\n{engine_js}\n</script>",
        1,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def check_structure(path):
    """Cheap structural sanity checks: balanced divs, no duplicate ids."""
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    open_divs = len(re.findall(r"<div\b", html))
    close_divs = len(re.findall(r"</div>", html))
    ids = re.findall(r'\bid="([^"]+)"', html)
    dupes = [i for i in set(ids) if ids.count(i) > 1]
    problems = []
    if open_divs != close_divs:
        problems.append(f"unbalanced divs: {open_divs} open vs {close_divs} close")
    if dupes:
        problems.append(f"duplicate ids: {dupes}")
    return problems


def check_js_syntax(path):
    """Extract every <script>...</script> block (no src attr) and run node --check."""
    import subprocess, tempfile
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    blocks = re.findall(r"<script(?:\s+[^>]*)?>(.*?)</script>", html, re.S)
    # filter out ones that were actually src= tags with empty body (shouldn't match anyway)
    problems = []
    for i, block in enumerate(blocks):
        if not block.strip():
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as tf:
            tf.write(block)
            tmp_path = tf.name
        result = subprocess.run(["node", "--check", tmp_path], capture_output=True, text=True)
        if result.returncode != 0:
            problems.append(f"script block {i}: {result.stderr.strip()[:300]}")
        os.unlink(tmp_path)
    return problems
