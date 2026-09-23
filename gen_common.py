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

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900'
    '&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
)
SUPABASE_CDN = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js"></script>'


def j(data):
    """Compact JS-literal-safe JSON dump (used to embed lesson DATA objects)."""
    return json.dumps(data, ensure_ascii=False)


STEP_TABS = [
    ("sec-warmup", "1 Warm-up"), ("sec-diagnostic", "2 Check"), ("sec-concept", "3 Concept"),
    ("sec-reading", "4 Reading"), ("sec-vocab", "5 Vocab"), ("sec-practice", "6 Practice"),
    ("sec-speaking", "7 Speaking"), ("sec-listening", "8 Listening"),
]


def top_nav(left="Workplace EQ", links_html=None):
    """The bottle-green bar at the top of every page."""
    if links_html is None:
        links_html = (
            '<a id="all-lessons-link" href="index-standalone.html">All lessons</a>'
            '<a id="glossary-link" href="glossary-standalone.html">My glossary</a>'
        )
    return f'''<div class="eq-nav"><div class="eq-wrap">
  <span>{left}</span><span class="eq-nav-links">{links_html}</span>
</div></div>'''


ON_ATTR = ' class="on"'


def nav_header(eyebrow, title, sub, is_test=False, section_name="", steps=None):
    """Nav bar + green header band (+ step tabs for lessons).
    Keeps the ids the engine relies on: all-lessons-link, glossary-link,
    overall-progress, sync-status."""
    links = '<a id="all-lessons-link" href="index-standalone.html">All lessons</a>'
    if not is_test:
        links += '<a id="glossary-link" href="glossary-standalone.html">My glossary</a>'
    steps = STEP_TABS if steps is None else steps
    tabs = ""
    if steps:
        tabs = '<nav class="eq-steps" aria-label="Lesson sections"><div class="eq-wrap">' + "".join(
            f'<a href="#{sid}" data-step="{sid}"{ON_ATTR if i == 0 else ""}>{label}</a>'
            for i, (sid, label) in enumerate(steps)
        ) + '</div></nav>'
    sec_line = f'<br><span class="sec-name">{section_name}</span>' if section_name else ""
    return f'''{top_nav(links_html=links)}
  <header class="eq-band"><div class="eq-wrap grid12">
    <div class="eq-band-meta">
      <div>{eyebrow}{sec_line}</div>
      <div><div class="pb-track"><div class="pb-fill" id="overall-progress" style="width:0%"></div></div>
      <div id="sync-status" style="margin-top:8px"></div></div>
    </div>
    <div class="eq-band-main">
      <h1 class="lesson-title">{title}</h1>
      <p class="lesson-sub">{sub}</p>
    </div>
  </div></header>
  {tabs}'''


def page_shell(*, title, theme_class, body_html, extra_head="", page_script=""):
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
<body class="{theme_class}">
{body_html}

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
