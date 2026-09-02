"""Build a self-contained verification report HTML from a manifest.json.

Usage: python3 build_report.py <manifest.json> <output.html>

Embeds every screenshot as a base64 data URI so the output is a single file
and the source screenshots can be deleted afterward. Styling comes from the
plugin's shared assets/report.css, inlined so the report stays self-contained
and so verify-feature, review-suite and visual-spec keep matching.

The manifest carries header fields, "flows" (UI flows with screenshots) and
"sections" (non-UI results: tables, evidence blocks, notes). Flow notes and
captions are escaped plain text, backwards compatible with the older ui-report
manifests. Section notes, table headers/cells and notes-blocks are trusted raw
HTML so the authoring skill can mark up <code>, <span class="ok"> and
<span class="warn"> - the manifest is always machine-authored, never untrusted
input. Evidence-block text is escaped and rendered mono/pre-wrap.
"""

import base64
import html
import json
import sys
from pathlib import Path

# skills/verify-feature/scripts/build_report.py -> plugin root is 3 up
CSS_PATH = Path(__file__).resolve().parents[3] / "assets" / "report.css"

FALLBACK_CSS = """
:root { --ivory:#101418; --slate:#e8e5df; --clay:#D97757; --oat:#2a323c;
        --oat-deep:#98a1ab; --olive:#8fb573; --gray-light:#1d242c; --gray-dark:#98a1ab; }
* { box-sizing:border-box; }
body { margin:0; background:var(--ivory); color:var(--slate);
       font-family:system-ui,-apple-system,sans-serif; line-height:1.55; }
.wrap { max-width:1120px; margin:0 auto; padding:48px 24px 96px; }
h1,h2 { font-family:ui-serif,Georgia,serif; font-weight:600; }
.eyebrow { font-family:ui-monospace,monospace; text-transform:uppercase;
           letter-spacing:.08em; font-size:.72rem; color:var(--gray-dark); }
.meta { font-family:ui-monospace,monospace; font-size:.8rem;
        color:var(--gray-dark); margin-bottom:28px; }
.flow,.summary { border:1px solid var(--oat); border-radius:14px; background:#171d24;
                 padding:24px 28px; margin-bottom:36px; }
.flow-head { display:flex; align-items:baseline; gap:14px; }
.badge { font-family:ui-monospace,monospace; font-size:.7rem; color:#10151a;
         border-radius:999px; padding:3px 12px; }
.badge.ok { background:var(--olive); } .badge.bad { background:var(--clay); }
.badge.muted { background:var(--gray-dark); } .badge.na { background:var(--oat-deep); }
.notes { margin:12px 0 4px; }
.console,.evidence { font-family:ui-monospace,monospace; font-size:.78rem;
           background:var(--gray-light); border-radius:10px; padding:10px 14px;
           margin:12px 0; white-space:pre-wrap; overflow-x:auto; color:var(--gray-dark); }
.console.errors,.evidence { border-left:3px solid var(--clay); }
.shots { display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:20px; }
figure { margin:0; }
figure img { width:100%; border:1.5px solid var(--oat); border-radius:10px; display:block; }
figcaption { font-size:.85rem; color:var(--gray-dark); margin-top:8px; }
figcaption .n { font-family:ui-monospace,monospace; color:var(--clay); margin-right:6px; }
.tablewrap { overflow-x:auto; }
table.results { width:100%; border-collapse:collapse; margin:14px 0 6px; font-size:.88rem; }
table.results th { font-family:ui-monospace,monospace; text-transform:uppercase;
                   letter-spacing:.06em; font-size:.68rem; color:var(--gray-dark);
                   text-align:left; padding:8px 12px; border-bottom:1.5px solid var(--oat); }
table.results td { padding:8px 12px; border-bottom:1px solid var(--gray-light);
                   vertical-align:top; }
code { font-family:ui-monospace,monospace; font-size:.82em;
       background:var(--gray-light); border-radius:5px; padding:1px 5px; }
.ok { color:var(--olive); font-weight:600; }
.warn { color:var(--clay); font-weight:600; }
"""

# Label plus badge class. "na" and "notes" exist so a category the diff never
# touched renders explicitly - a silently missing section is indistinguishable
# from a forgotten one.
STATUS = {
    "pass": ("PASS", "ok"),
    "fail": ("FAIL", "bad"),
    "blocked": ("BLOCKED", "muted"),
    "accepted": ("ACCEPTED", "muted"),
    "na": ("N/A", "na"),
    "notes": ("NOTES", "muted"),
}

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
<div class="wrap">
    <div class="eyebrow">Verification report &middot; {date}</div>
    <h1>{title}</h1>
    <div class="meta">{repo} &middot; {branch} @ {commit} &middot; {base_url}</div>
    <div class="summary">{summary}</div>
    {flows}
    {sections}
</div>
</body>
</html>
"""

FLOW = """<section class="flow">
    <div class="flow-head">
        <h2>{name}</h2>
        <span class="badge {cls}">{label}</span>
    </div>
    <p class="notes">{notes}</p>
    {console}
    <div class="shots">{shots}</div>
</section>
"""

SECTION = """<section class="flow">
    <div class="flow-head">
        <h2>{name}</h2>
        <span class="badge {cls}">{label}</span>
    </div>
    {notes}
    {blocks}
</section>
"""


def load_css():
    try:
        return CSS_PATH.read_text(encoding="utf-8")
    except OSError:
        return FALLBACK_CSS


def embed(path):
    data = base64.b64encode(Path(path).read_bytes()).decode("ascii")
    ext = Path(path).suffix.lstrip(".").lower() or "png"
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    return f"data:image/{mime};base64,{data}"


def render_flow(flow):
    label, cls = STATUS.get(flow.get("status", "blocked"), STATUS["blocked"])
    console = flow.get("console", "").strip()
    console_html = (
        f'<div class="console errors">{html.escape(console)}</div>' if console else ""
    )
    shots = []
    for i, shot in enumerate(flow.get("shots", []), 1):
        shots.append(
            '<figure><img src="{src}" alt="{alt}">'
            '<figcaption><span class="n">{n:02d}</span>{cap}</figcaption></figure>'.format(
                src=embed(shot["path"]),
                alt=html.escape(shot.get("caption", "")),
                n=i,
                cap=html.escape(shot.get("caption", "")),
            )
        )
    return FLOW.format(
        name=html.escape(flow.get("name", "Flow")),
        label=label,
        cls=cls,
        notes=html.escape(flow.get("notes", "")),
        console=console_html,
        shots="".join(shots),
    )


def render_block(block):
    kind = block.get("type", "notes")
    if kind == "table":
        head = "".join(f"<th>{h}</th>" for h in block.get("headers", []))
        rows = "".join(
            "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
            for row in block.get("rows", [])
        )
        head_html = f"<tr>{head}</tr>" if head else ""
        return f'<div class="tablewrap"><table class="results">{head_html}{rows}</table></div>'
    if kind == "evidence":
        return f'<div class="evidence">{html.escape(block.get("text", ""))}</div>'
    return f'<p class="notes">{block.get("html", "")}</p>'


def render_section(sec):
    label, cls = STATUS.get(sec.get("status", "notes"), STATUS["notes"])
    notes = sec.get("notes", "")
    notes_html = f'<p class="notes">{notes}</p>' if notes else ""
    blocks = "".join(render_block(b) for b in sec.get("blocks", []))
    return SECTION.format(
        name=html.escape(sec.get("name", "Section")),
        label=label,
        cls=cls,
        notes=notes_html,
        blocks=blocks,
    )


def main():
    manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])

    flows_html = "".join(render_flow(f) for f in manifest.get("flows", []))
    sections_html = "".join(render_section(s) for s in manifest.get("sections", []))

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        PAGE.format(
            css=load_css(),
            title=html.escape(manifest.get("title", "Verification report")),
            date=html.escape(manifest.get("date", "")),
            repo=html.escape(manifest.get("repo", "")),
            branch=html.escape(manifest.get("branch", "")),
            commit=html.escape(manifest.get("commit", "")),
            base_url=html.escape(manifest.get("base_url", "")),
            summary=manifest.get("summary", ""),
            flows=flows_html,
            sections=sections_html,
        ),
        encoding="utf-8",
        newline="\n",
    )
    n = len(manifest.get("flows", [])) + len(manifest.get("sections", []))
    print(f"wrote {out} ({out.stat().st_size // 1024} KB, {n} sections)")


if __name__ == "__main__":
    main()
