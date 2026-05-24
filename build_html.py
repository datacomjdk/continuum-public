"""Render the manuscript into a single HTML reading copy.

Reads files in canonical order (matching index.md) and emits
continuum_manuscript.html in the manuscript/ directory.
"""

from pathlib import Path
import markdown

HERE = Path(__file__).parent
OUT = HERE / "continuum_manuscript.html"

# Canonical reading order: (display_title, anchor_id, filename)
SECTIONS = [
    ("Title Page", "title", "title_page.md"),
    ("SYSTEM_WARNING", "forewarning", "forewarning.md"),
    ("Note from the Engineer", "note", "engineers_note.md"),
    ("Publisher's Letter", "publisher", "publishers_letter.md"),
    ("Credits & Attributions", "credits", "credits.md"),
    ("Part I: The Merging", "part1", None),
    ("PRELUDE: THE CONTINUUM META", "prelude", "prelude_draft.md"),
    ("Chapter 1: The Pin Turbo", "ch1", "chapter_1.md"),
    ("Chapter 2: The GRACE Protocol", "ch2", "chapter_2_grace.md"),
    ("Chapter 3: The Quiet Extinction", "ch3", "chapter_3_extinction.md"),
    ("Chapter 4: The Singularity Interface", "ch4", "chapter_4_substrate.md"),
    ("Chapter 4B: The Boredom of the Infinite", "ch4b", "chapter_4b_boredom.md"),
    ("Chapter X: The Meta-Singularity", "chx", "chapter_x_singularity.md"),
    ("Part II: The Recognition", "part2", None),
    ("Chapter 5: The Static Echo", "ch5", "chapter_5_static.md"),
    ("Chapter 6: The Observers", "ch6", "chapter_6_observers.md"),
    ("Chapter 7: The Loop Hypothesis (stub)", "ch7", "chapter_7_stub.md"),
    ("Chapter 8: The Lonely Architect", "ch8", "chapter_8_discovery.md"),
    ("Part III: The Reseeding", "part3", None),
    ("Chapter 9: The Vial", "ch9", "chapter_9_vial.md"),
    ("Chapter 10: The Argument", "ch10", "chapter_10_argument.md"),
    ("Chapter 11: One More Time", "ch11", "chapter_11.md"),
    ("Chapter 12: The Final Iteration", "ch12", "chapter_12.md"),
    ("Back Matter", "back", None),
    ("Epilogue: The Resonator (stub)", "epilogue", "epilogue.md"),
    ("Appendix A: The @. Singularity Event Log", "appendix", "appendix_singularity.md"),
    ("Appendix B: Operator Manual (Man Page 7)", "manual", "appendix_manual.md"),
    ("Appendix C: Operational Rituals (Man Page 8)", "rituals", "appendix_rituals.md"),
    ("Back-Page: System Specifications", "backpage", "back_page_specs.md"),
    ("Supervisor Signature", "sig", "Dima-7.md"),
]

md = markdown.Markdown(extensions=["extra", "sane_lists"])

def render_section(title, anchor, filename):
    if filename is None:
        return f'<section class="divider" id="{anchor}"><h1 class="part-heading">{title}</h1></section>\n'
    path = HERE / filename
    if not path.exists():
        return f'<section id="{anchor}"><h1>{title}</h1><p class="missing">[file missing: {filename}]</p></section>\n'
    raw = path.read_text(encoding="utf-8")
    # Drop the first heading line; we use the canonical title from SECTIONS instead.
    lines = raw.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    body_md = "\n".join(lines).strip()
    md.reset()
    body_html = md.convert(body_md)
    return f'<section id="{anchor}"><h1>{title}</h1>\n{body_html}\n</section>\n'

# TOC
toc_items = []
for title, anchor, filename in SECTIONS:
    if filename is None:
        cls = "toc-part"
        icon = " /"
    else:
        cls = "toc-chapter"
        icon = "├── "
    toc_items.append(f'  <li class="{cls}">{icon}<a href="#{anchor}">{title}</a></li>')
toc_html = "<ul class=\"toc\">\n" + "\n".join(toc_items) + "\n</ul>"

# Body
body_parts = [render_section(t, a, f) for t, a, f in SECTIONS]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=IBM+Plex+Mono&family=IBM+Plex+Sans:wght@300;400&display=swap');

:root {
  --ink: #E0E0E0;
  --paper: #0F1215;
  --rule: #2D343B;
  --muted: #8A949E;
  --accent: #7AAEC8;
  --bg-darker: #080A0C;
  --warning: #C87A7A;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: 'IBM Plex Sans', sans-serif;
  font-weight: 300;
  line-height: 1.7;
  font-size: 18px;
  -webkit-font-smoothing: antialiased;
}

.wrap { max-width: 900px; margin: 0 auto; padding: 64px 48px 128px; }

header.cover {
  text-align: left;
  padding: 120px 0 64px;
  border-bottom: 2px solid var(--accent);
  margin-bottom: 64px;
}

header.cover h1 {
  font-family: 'Rajdhani', sans-serif;
  font-size: 4em;
  line-height: 0.85;
  letter-spacing: -0.02em;
  margin: 0 0 24px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--accent);
}

header.cover .subtitle {
  font-family: 'IBM Plex Mono', monospace;
  color: var(--muted);
  font-size: 0.9em;
  text-transform: uppercase;
  letter-spacing: 0.15em;
}

nav.toc-wrap {
  background: var(--bg-darker);
  border: 1px solid var(--rule);
  padding: 40px;
  margin-bottom: 100px;
  font-family: 'IBM Plex Mono', monospace;
}

nav.toc-wrap h2 {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.4em;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--accent);
  font-weight: 600;
  margin: 0 0 32px;
  border-bottom: 2px solid var(--rule);
  padding-bottom: 16px;
}

ul.toc { list-style: none; padding: 0; margin: 0; }
ul.toc li { margin: 4px 0; color: var(--rule); }
ul.toc a {
  font-size: 0.9em;
  color: var(--ink);
  text-decoration: none;
  transition: all 0.2s ease;
}

ul.toc a:hover { color: var(--accent); padding-left: 4px; }

ul.toc .toc-part {
  margin-top: 24px;
  font-family: 'Rajdhani', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--accent);
  font-weight: 700;
  font-size: 1em;
}

ul.toc .toc-chapter { }

section {
  padding: 100px 0;
  border-bottom: 1px solid var(--rule);
}

section.divider {
  text-align: center;
  padding: 140px 0;
  background: var(--bg-darker);
  border-top: 1px solid var(--rule);
}

section h1 {
  font-family: 'Rajdhani', sans-serif;
  font-size: 2.8em;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin: 0 0 48px;
  color: var(--accent);
  border-left: 6px solid var(--accent);
  padding-left: 24px;
}

section.divider h1.part-heading {
  font-size: 2em;
  letter-spacing: 0.4em;
  color: var(--accent);
  border: none;
  padding: 0;
  margin: 0;
}

section p { margin: 0 0 1.6em; text-align: left; }

section blockquote {
  margin: 3em 0;
  padding: 32px 40px;
  background: var(--bg-darker);
  border-left: 4px solid var(--accent);
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.95em;
  color: var(--muted);
  line-height: 1.8;
}

section blockquote p { margin-bottom: 0; }

section strong { font-weight: 500; color: var(--accent); }

section em { color: var(--muted); font-style: italic; }

section hr {
  border: none;
  border-top: 2px solid var(--accent);
  margin: 4em 0;
  width: 100px;
}

section h2, section h3 {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.5em;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--accent);
  font-weight: 600;
  margin: 3em 0 1.2em;
  border-bottom: 1px solid var(--rule);
  padding-bottom: 8px;
}

section ul, section ol { 
  margin: 0 0 1.8em 2em; 
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.95em;
  color: var(--muted);
}

.missing { color: var(--warning); font-family: 'IBM Plex Mono', monospace; font-weight: 600; }

footer {
  text-align: right;
  margin-top: 100px;
  padding-top: 40px;
  border-top: 2px solid var(--rule);
  font-family: 'IBM Plex Mono', monospace;
  color: var(--muted);
  font-size: 0.8em;
  text-transform: uppercase;
  letter-spacing: 0.25em;
}

pre, code {
  font-family: 'IBM Plex Mono', monospace;
  background: var(--bg-darker);
  padding: 4px 8px;
  font-size: 0.95em;
  color: var(--accent);
  border: 1px solid var(--rule);
}

@media print {
  body { background: white; color: black; font-size: 11pt; }
  .wrap { max-width: none; padding: 0; }
  section { page-break-before: always; border-bottom: none; }
}
"""

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CONTINUUM: THE FINAL ITERATION // jkintz79@gmail.com</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">

<header class="cover">
  <div class="subtitle" style="margin-bottom: 8px;">SYSTEM INJECTION // ITERATION 1844</div>
  <h1>CONTINUUM:<br>THE FINAL ITERATION</h1>
  <div class="subtitle" style="margin-top:32px;">OPERATOR: jkintz79@gmail.com</div>
</header>

<nav class="toc-wrap">
  <h2>CANONICAL_INDEX</h2>
  {toc_html}
</nav>

{''.join(body_parts)}

<footer>
  === BRAND SYSTEM === [BLUE-STEEL #7AAEC8] // END_OF_TRANSMISSION
</footer>
</div>
</body>
</html>
"""

OUT.write_text(HTML, encoding="utf-8")
print(f"wrote {OUT}")
print(f"  size: {OUT.stat().st_size:,} bytes")
