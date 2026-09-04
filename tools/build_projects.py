#!/usr/bin/env python3
"""Stamp /projects/<slug>.html pages from tools/projects.json.

Usage: python tools/build_projects.py   (run from the repo root or tools/)
Edit projects.json, re-run, commit both. No dependencies.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "projects"

PAGE = """<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" type="image/png" href="/favicon.png" />
  <title>{title} — CJ Williams</title>
  <meta name="description" content="{subtitle}" />
  <meta property="og:title" content="{title} — CJ Williams" />
  <meta property="og:image" content="https://hirecj.com{hero}" />
  <link href="https://fonts.googleapis.com/css?family=Raleway:400,300,500,600,700,800" rel="stylesheet" type="text/css" />
  <link href="/css/project.css?v=2" rel="stylesheet" type="text/css" />
</head>
<body class="pp">
  <header class="pp-bar">
    <a class="pp-name" href="/">CJ Williams</a>
    <a class="pp-back" href="/#Portfolio">&larr; All Work</a>
  </header>

  <main class="pp-main">
    <p class="pp-kicker">{kicker}</p>
    <h1>{title}</h1>
    <p class="pp-subtitle">{subtitle}</p>

    <img class="pp-hero" src="{hero}" alt="{title}" />

    <dl class="pp-facts">
      <div><dt>Client</dt><dd>{client}</dd></div>
      <div><dt>Role</dt><dd>{role}</dd></div>
      <div><dt>Timeline</dt><dd>{timeline}</dd></div>
      <div><dt>Team</dt><dd>{team}</dd></div>
    </dl>

    <p class="pp-tags">{tags}</p>

    <section>
      <h2>The Challenge</h2>
      {challenge}
    </section>

    <section>
      <h2>What I Did</h2>
      {work}
    </section>
{process}{outcomes}
    <div class="pp-links">{links}
      <a class="pp-button pp-button-ghost" href="/#Portfolio">&larr; Back to All Work</a>
    </div>
  </main>

  <footer class="pp-footer">
    <p>Humboldt Park &middot; Chicago, IL 60647</p>
    <p><a href="mailto:cj@silencekillsdesign.com">cj@silencekillsdesign.com</a></p>
    <p class="pp-copyright">Copyright 2026 &middot; CJ Williams</p>
  </footer>

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-1Y4FNXF79M"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() {{ dataLayer.push(arguments); }}
    gtag('js', new Date());
    gtag('config', 'G-1Y4FNXF79M');
  </script>
</body>
</html>
"""

PROCESS = """
    <section class="pp-cols">
{cols}    </section>
"""

PROCESS_COL = """      <div>
        <h3>{heading}</h3>
        <ul>{items}</ul>
      </div>
"""

OUTCOMES = """
    <section>
      <h2>The Outcome</h2>
      {metrics}
      <p class="pp-summary">{summary}</p>
    </section>
"""

GALLERY = """
    <section>
      <h2>{title}</h2>
      <div class="pp-gallery">
{items}      </div>
    </section>
"""


def figure(img, caption, cls="pp-fig", narrow=False):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    cls = (cls + " pp-narrow").strip() if narrow else cls
    return f'<figure class="{cls}"><img src="{img}" alt="{caption}" loading="lazy" />{cap}</figure>'


def paragraphs(items):
    return "\n      ".join(f"<p>{p}</p>" for p in items)


def build(p):
    work = "\n      ".join(
        f'<div class="pp-work"><h3><span>{i:02d}</span> {w["title"]}</h3>'
        f'<p class="pp-problem">{w["problem"]}</p>'
        f'<p>{w["solution"]}</p>'
        + (figure(w["image"], w.get("caption", ""), narrow=w.get("narrow", False)) if w.get("image") else "")
        + (
            f'<div class="pp-embed"><iframe src="{w["embed"]}" loading="lazy" '
            f'allowfullscreen title="{w.get("caption", w["title"])}"></iframe>'
            + (f'<p class="pp-embed-cap">{w["caption"]}</p>' if w.get("caption") else "")
            + "</div>"
            if w.get("embed") else ""
        )
        + "</div>"
        for i, w in enumerate(p["work"], 1)
    )

    gallery = ""
    if p.get("gallery"):
        items = "".join(
            "        " + figure(g["src"], g.get("caption", ""), cls="", narrow=g.get("narrow", False)) + "\n"
            for g in p["gallery"]
        )
        gallery = GALLERY.format(title=p.get("galleryTitle", "Gallery"), items=items)

    cols = "".join(
        PROCESS_COL.format(heading=heading, items="".join(f"<li>{v}</li>" for v in items))
        for heading, items in [
            ("How It Was Validated", p.get("validation", [])),
            ("After Launch", p.get("iteration", [])),
        ]
        if items
    )
    process = PROCESS.format(cols=cols) if cols else ""

    outcomes = ""
    if p.get("metrics") or p.get("summary"):
        metrics = ""
        if p.get("metrics"):
            metrics = '<div class="pp-metrics">' + "".join(
                f'<div><strong>{m["value"]}</strong><span>{m["label"]}</span></div>'
                for m in p["metrics"]
            ) + "</div>"
        outcomes = OUTCOMES.format(metrics=metrics, summary=p.get("summary", ""))

    links = "".join(
        f'\n      <a class="pp-button" href="{l["href"]}" target="_blank" rel="noopener">{l["label"]}</a>'
        for l in p.get("links", [])
    )

    return PAGE.format(
        title=p["title"],
        subtitle=p["subtitle"],
        kicker=p["kicker"],
        hero=p["hero"],
        client=p["client"],
        role=p["role"],
        timeline=p["timeline"],
        team=p["team"],
        tags=" &middot; ".join(p["tags"]),
        challenge=paragraphs(p["challenge"]),
        work=work,
        process=process,
        outcomes=outcomes + gallery,
        links=links,
    )


def main():
    data = json.loads((ROOT / "tools" / "projects.json").read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    for p in data["projects"]:
        out = OUT / f"{p['slug']}.html"
        out.write_text(build(p), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
