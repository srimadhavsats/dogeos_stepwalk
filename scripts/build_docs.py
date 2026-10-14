"""Build the public reading pages for the whitepaper and tokenomics.

The Markdown files in docs/ are the source of truth. This script turns them into
standalone HTML pages next to the prototype, so the live site can link to them:

    python scripts/build_docs.py

It handles the small Markdown subset our docs use (headings, paragraphs, lists,
tables, blockquotes, code blocks, bold, italics, inline code and links), so it
needs nothing beyond the Python standard library.
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/srimadhavsats/dogeos_stepwalk/blob/main/docs/"
PAGES = [
    ("WHITEPAPER.md", "whitepaper.html", "Whitepaper", "MuchWalk Whitepaper",
     "MuchWalk: a dog-walking game on DogeOS where real dog walks fill a shared Treat Bowl. Points first, token later."),
    ("TOKENOMICS.md", "tokenomics.html", "Tokenomics", "MuchWalk Tokenomics",
     "The dog-walk economy: revenue-linked Treat Bowl, claim with commitment, leash energy, sponsored walks and a careful launch."),
]
LOCAL = {"WHITEPAPER.md": "whitepaper.html", "TOKENOMICS.md": "tokenomics.html"}


def slug(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.UNICODE)
    return re.sub(r"[\s_]+", "-", text).strip("-")


def link_target(url):
    if url in LOCAL:
        return LOCAL[url], False
    if url.endswith(".md") and "://" not in url:
        return REPO + url, True
    return url, url.startswith("http")


def inline(text):
    codes = []

    def keep_code(m):
        codes.append("<code>" + html.escape(m.group(1)) + "</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text, quote=False)

    def make_link(m):
        href, external = link_target(m.group(2))
        attrs = ' target="_blank" rel="noopener"' if external else ""
        return f'<a href="{html.escape(href)}"{attrs}>{m.group(1)}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", make_link, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def table(rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], cells[2:]
    out = ['<div class="tablewrap"><table>']
    if any(head):
        out.append("<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead>")
    out.append("<tbody>")
    for r in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def lists(lines):
    """Render a run of list lines (one nesting level, '-' or '1.')."""
    out, stack = [], []  # stack of (indent, tag)
    for line in lines:
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        indent, tag = len(m.group(1)), "ol" if m.group(2)[0].isdigit() else "ul"
        while stack and indent < stack[-1][0]:
            out.append(f"</li></{stack.pop()[1]}>")
        if not stack or indent > stack[-1][0]:
            out.append(f"<{tag}>")
            stack.append((indent, tag))
        else:
            out.append("</li>")
        out.append("<li>" + inline(m.group(3)))
    while stack:
        out.append(f"</li></{stack.pop()[1]}>")
    return "".join(out)


def convert(md):
    lines, out, toc, i = md.splitlines(), [], [], 0
    title = ""
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif line.startswith("```"):
            j = i + 1
            while not lines[j].startswith("```"):
                j += 1
            out.append("<pre><code>" + html.escape("\n".join(lines[i + 1:j])) + "</code></pre>")
            i = j + 1
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            text = inline(line[level:].strip())
            if level == 1:
                title = text
            else:
                hid = slug(text)
                if level == 2:
                    toc.append((hid, re.sub(r"<[^>]+>", "", text)))
                out.append(f'<h{level} id="{hid}">{text}</h{level}>')
            i += 1
        elif line.startswith(">"):
            j = i
            while j < len(lines) and lines[j].startswith(">"):
                j += 1
            paras = "".join(f"<p>{inline(l.lstrip('> ').strip())}</p>" for l in lines[i:j])
            out.append(f'<aside class="note">{paras}</aside>')
            i = j
        elif line.startswith("|"):
            j = i
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            out.append(table(lines[i:j]))
            i = j
        elif re.match(r"^\s*([-*]|\d+\.)\s+", line):
            j = i
            while j < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[j]):
                j += 1
            out.append(lists(lines[i:j]))
            i = j
        else:
            j = i
            while j < len(lines) and lines[j].strip() and not re.match(r"^(#|>|\||```|\s*([-*]|\d+\.)\s)", lines[j]):
                j += 1
            text = " ".join(l.strip() for l in lines[i:j])
            cls = ' class="fine"' if text.startswith("*") and text.endswith("*") else ""
            out.append(f"<p{cls}>{inline(text)}</p>")
            i = j
    return title, toc, "\n".join(out)


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{page_title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Nunito:wght@500;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root{{--bg:#FFF6E5;--surface:#FFFFFF;--surface2:#FFF0CC;--text:#1F1A33;--text2:#5B5470;--outline:#1F1A33;--gold:#FFC531;--mint:#22C997;--pink:#FF5C8A;--link:#5B4BD6;--codebg:#1F1A33;--codefg:#FFE29A;color-scheme:light}}
@media (prefers-color-scheme: dark){{:root{{--bg:#14112A;--surface:#221D40;--surface2:#2C2652;--text:#FFF6E5;--text2:#B9B2D9;--outline:#05040C;--link:#A99CFF;--codebg:#0B0920;color-scheme:dark}}}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth;scroll-padding-top:130px}}
@media (min-width:760px){{html{{scroll-padding-top:84px}}}}
body{{margin:0;background:var(--bg);color:var(--text);font:600 16px/1.65 "Nunito",system-ui,sans-serif}}
a{{color:var(--link);font-weight:800}}
.top{{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:3px solid var(--outline)}}
.top .in{{max-width:1120px;margin:0 auto;padding:10px 16px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.brand{{font:800 22px "Baloo 2",sans-serif;color:var(--text);text-decoration:none;margin-right:auto}}
.seg{{display:flex;border:3px solid var(--outline);border-radius:999px;overflow:hidden}}
.seg a{{padding:6px 14px;text-decoration:none;color:var(--text);font-size:14px}}
.seg a[aria-current]{{background:var(--outline);color:var(--gold)}}
.btn{{display:inline-flex;align-items:center;gap:6px;border:3px solid var(--outline);border-radius:999px;padding:6px 12px;background:var(--gold);color:#1F1A33;font:800 14px "Nunito",sans-serif;text-decoration:none;box-shadow:0 3px 0 var(--outline);cursor:pointer}}
.btn.sec{{background:var(--surface);color:var(--text)}}
.btn:active{{transform:translateY(2px);box-shadow:0 1px 0 var(--outline)}}
.wrap{{max-width:1120px;margin:0 auto;padding:24px 16px 64px;display:grid;grid-template-columns:minmax(0,1fr);gap:32px}}
@media (min-width:1000px){{.wrap{{grid-template-columns:230px minmax(0,1fr)}}}}
.toc{{align-self:start}}
@media (min-width:1000px){{.toc{{position:sticky;top:84px;max-height:calc(100vh - 100px);overflow:auto}}}}
.toc details{{border:3px solid var(--outline);border-radius:18px;background:var(--surface);padding:10px 14px}}
.toc summary{{font-weight:900;cursor:pointer}}
.toc ol{{margin:8px 0 0;padding-left:20px;font-size:14px;line-height:1.5}}
.toc li{{margin:4px 0}}
.toc a{{color:var(--text);font-weight:700;text-decoration:none}}
.toc a:hover{{text-decoration:underline}}
article{{max-width:760px;min-width:0}}
.hero h1{{font:800 clamp(34px,6vw,52px)/1.05 "Baloo 2",sans-serif;margin:0 0 10px}}
.chips{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}}
.chip{{border:3px solid var(--outline);border-radius:999px;padding:3px 10px;font-weight:900;font-size:12px;background:var(--surface)}}
.chip.draft{{background:var(--outline);color:var(--gold);letter-spacing:1px}}
h2{{font:800 28px/1.15 "Baloo 2",sans-serif;margin:40px 0 10px;padding-top:6px;border-top:3px dashed var(--outline)}}
h3{{font:800 20px/1.2 "Baloo 2",sans-serif;margin:24px 0 6px}}
p{{margin:10px 0}}
ul,ol{{padding-left:24px;margin:10px 0}}
li{{margin:5px 0}}
li > ul,li > ol{{margin:4px 0}}
strong{{font-weight:900}}
.note{{border:3px dashed var(--outline);border-radius:18px;background:var(--surface2);padding:4px 16px;margin:16px 0}}
.note p{{margin:10px 0}}
.tablewrap{{overflow-x:auto;margin:14px 0;border:3px solid var(--outline);border-radius:18px;background:var(--surface);box-shadow:0 4px 0 var(--outline)}}
table{{border-collapse:collapse;width:100%;font-size:14.5px;line-height:1.45}}
th,td{{text-align:left;vertical-align:top;padding:9px 12px;border-bottom:1px solid color-mix(in srgb,var(--text) 14%,transparent)}}
th{{background:var(--surface2);font-weight:900;white-space:nowrap}}
tbody tr:last-child td{{border-bottom:0}}
td:first-child{{font-weight:700}}
code{{font:600 .9em ui-monospace,SFMono-Regular,Consolas,monospace;background:var(--surface2);border-radius:6px;padding:1px 5px}}
pre{{background:var(--codebg);color:var(--codefg);border:3px solid var(--outline);border-radius:18px;padding:14px 16px;overflow-x:auto;font-size:13.5px;line-height:1.55}}
pre code{{background:none;padding:0;color:inherit}}
.fine{{color:var(--text2);font-size:14px;border-top:3px dashed var(--outline);padding-top:14px;margin-top:36px}}
.foot{{color:var(--text2);font-size:13px;margin-top:28px}}
@media print{{
  :root{{--bg:#fff;--surface:#fff;--surface2:#f4f1ea;--text:#111;--text2:#444;--outline:#222;--link:#222;--codebg:#f4f1ea;--codefg:#111}}
  .top,.toc,.foot{{display:none}}
  .wrap{{display:block;padding:0}}
  article{{max-width:none}}
  .tablewrap{{box-shadow:none;overflow:visible}}
  tr,pre,.note{{break-inside:avoid}}
  h2{{break-after:avoid}}
  a{{color:inherit;text-decoration:none}}
}}
</style>
</head>
<body>
<header class="top"><div class="in">
  <a class="brand" href="./">🐕 MuchWalk</a>
  <nav class="seg" aria-label="Documents">{nav}</nav>
  <a class="btn sec" href="./">▶ Open the app</a>
  <button class="btn" type="button" onclick="window.print()">⎙ Save as PDF</button>
</div></header>
<div class="wrap">
  <nav class="toc" aria-label="Contents"><details open><summary>Contents</summary><ol>{toc}</ol></details></nav>
  <article>
    <div class="hero"><h1>{title}</h1>
      <div class="chips"><span class="chip draft">DRAFT v0.2</span><span class="chip">October 2026</span><span class="chip">For discussion</span></div></div>
{body}
    <p class="foot">Source: <a href="{source}" target="_blank" rel="noopener">docs/{md}</a> on GitHub · <a href="./">Back to the prototype</a></p>
  </article>
</div>
<script>
// Keep the contents list compact on small screens
if (matchMedia('(max-width: 999px)').matches) document.querySelector('.toc details').removeAttribute('open');
</script>
</body>
</html>
"""


def main():
    for md, out, label, page_title, desc in PAGES:
        title, toc, body = convert((ROOT / "docs" / md).read_text(encoding="utf-8"))
        current = ' aria-current="page"'
        nav = "".join(f'<a href="{o}"{current if o == out else ""}>{l}</a>' for _, o, l, _, _ in PAGES)
        page = TEMPLATE.format(
            page_title=page_title, desc=html.escape(desc), nav=nav, title=title, body=body, md=md,
            source=REPO + md, toc="".join(f'<li><a href="#{h}">{t}</a></li>' for h, t in toc),
        )
        (ROOT / "prototype" / out).write_text(page, encoding="utf-8")
        print(f"wrote prototype/{out} ({len(page):,} bytes, {len(toc)} sections)")


if __name__ == "__main__":
    main()
