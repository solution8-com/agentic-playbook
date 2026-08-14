"""Build a self-contained UI report HTML from a manifest.json.

Usage: python build_report.py <manifest.json> <output.html>

Embeds every screenshot as a base64 data URI so the output is a single file
and the source screenshots can be deleted afterward. Styling comes from the
plugin's shared assets/report.css, inlined so the report stays self-contained.
Same house style as before: ivory/slate/clay palette, serif headings, mono labels.
"""

import base64
import html
import json
import sys
from pathlib import Path

# skills/utilities/ui-report/scripts/build_report.py -> plugin root is 4 up
CSS_PATH = Path(__file__).resolve().parents[4] / "assets" / "report.css"

FALLBACK_CSS = """
:root { --ivory:#FAF9F5; --slate:#141413; --clay:#D97757; --oat:#E3DACC;
        --olive:#788C5D; --gray-light:#F0EEE6; --gray-dark:#3D3D3A; }
* { box-sizing:border-box; }
body { margin:0; background:var(--ivory); color:var(--slate);
       font-family:system-ui,-apple-system,sans-serif; line-height:1.55; }
.wrap { max-width:1120px; margin:0 auto; padding:48px 24px 96px; }
h1,h2 { font-family:ui-serif,Georgia,serif; font-weight:600; }
.flow,.summary { border:1.5px solid var(--oat); border-radius:14px; background:#fff;
                 padding:24px 28px; margin-bottom:36px; }
.flow-head { display:flex; align-items:baseline; gap:14px; }
.badge { font-family:ui-monospace,monospace; font-size:.7rem; color:#fff;
         border-radius:999px; padding:3px 12px; }
.badge.ok { background:var(--olive); } .badge.bad { background:var(--clay); }
.badge.muted { background:var(--gray-dark); }
.console { font-family:ui-monospace,monospace; font-size:.78rem; background:var(--gray-light);
           border-radius:10px; padding:10px 14px; white-space:pre-wrap; }
.console.errors { border-left:3px solid var(--clay); }
.shots { display:grid; grid-template-columns:repeat(auto-fit,minmax(320px,1fr)); gap:20px; }
figure { margin:0; }
figure img { width:100%; border:1.5px solid var(--oat); border-radius:10px; display:block; }
figcaption { font-size:.85rem; color:var(--gray-dark); margin-top:8px; }
figcaption .n { font-family:ui-monospace,monospace; color:var(--clay); margin-right:6px; }
"""

STATUS = {
    "pass": ("PASS", "ok"),
    "fail": ("FAIL", "bad"),
    "blocked": ("BLOCKED", "muted"),
}


def load_css():
    """Shared stylesheet if it shipped with the plugin, else a minimal fallback."""
    try:
        return CSS_PATH.read_text(encoding="utf-8")
    except OSError:
        return FALLBACK_CSS

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<div class="wrap">
    <div class="eyebrow">UI report &middot; {date}</div>
    <h1>{title}</h1>
    <div class="meta">{repo} &middot; {branch} @ {commit} &middot; {base_url}</div>
    <div class="summary">{summary}</div>
    {flows}
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


def embed(path):
    data = base64.b64encode(Path(path).read_bytes()).decode("ascii")
    ext = Path(path).suffix.lstrip(".").lower() or "png"
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    return f"data:image/{mime};base64,{data}"


def main():
    manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])

    flows_html = []
    for flow in manifest.get("flows", []):
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
        flows_html.append(
            FLOW.format(
                name=html.escape(flow.get("name", "Flow")),
                label=label,
                cls=cls,
                notes=html.escape(flow.get("notes", "")),
                console=console_html,
                shots="".join(shots),
            )
        )

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        PAGE.format(
            css=load_css(),
            title=html.escape(manifest.get("title", "UI report")),
            date=html.escape(manifest.get("date", "")),
            repo=html.escape(manifest.get("repo", "")),
            branch=html.escape(manifest.get("branch", "")),
            commit=html.escape(manifest.get("commit", "")),
            base_url=html.escape(manifest.get("base_url", "")),
            summary=html.escape(manifest.get("summary", "")),
            flows="".join(flows_html),
        ),
        encoding="utf-8",
    )
    print(f"wrote {out} ({out.stat().st_size // 1024} KB, {len(flows_html)} flows)")


if __name__ == "__main__":
    main()
