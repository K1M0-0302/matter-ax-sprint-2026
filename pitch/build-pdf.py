#!/usr/bin/env python3
"""본선-발표대본-10분.md → .html → .pdf (A4, chromium headless). 사용: python3 build-pdf.py"""
import re, subprocess, pathlib, markdown

here = pathlib.Path(__file__).parent
src = here / "본선-발표대본-10분.md"
html_path, pdf_path = src.with_suffix(".html"), src.with_suffix(".pdf")

md = src.read_text()
# 지문 줄(▶ 조작/확인)을 회색 박스로 쓰도록 표시
def cue(m):
    return '<p class="cue">▶ ' + re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", m.group(1)) + "</p>"
md = re.sub(r"^▶ (.+)$", cue, md, flags=re.M)
# 문단 바로 뒤에 붙은 목록은 빈 줄을 넣어야 목록으로 읽힌다
md = re.sub(r"^(?!\s*[-|>]|\s*$)(.+)\n(?=- )", r"\1\n\n", md, flags=re.M)
# 대본은 한 줄 = 한 문장이라 줄바꿈을 살린다(nl2br)
body = markdown.markdown(md, extensions=["tables", "sane_lists", "nl2br"])
# *(화면: …)* 단독 문단 → 화면 지문
body = re.sub(r"<p><em>\((?:화면: )?(.+?)\)</em></p>", r'<p class="screen">\1</p>', body)
# 파트·부록 제목마다 새 쪽 (첫 제목 제외)
body = body.replace("<hr />\n", "")

css = """
@page { size: A4; margin: 16mm 16mm 18mm; }
:root { --ink:#1b1f24; --muted:#5b636e; --line:#d9dde3; --accent:#0a66b8; --cue:#f2f4f7; }
* { box-sizing: border-box; }
body { font-family: "Noto Sans CJK KR", sans-serif; font-size: 11pt; line-height: 1.7;
       color: var(--ink); background: #fff; margin: 0; word-break: keep-all; }
h1 { font-size: 17pt; line-height: 1.35; margin: 0 0 10pt; padding-bottom: 6pt;
     border-bottom: 2px solid var(--ink); }
h1 ~ h1 { break-before: page; }
h2 { font-size: 13pt; margin: 18pt 0 6pt; color: var(--accent); break-after: avoid; }
p { margin: 0 0 6pt; }
strong { font-weight: 700; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 9.5pt; line-height: 1.5; }
th, td { border-bottom: 1px solid var(--line); padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { border-bottom: 1.5px solid var(--ink); font-weight: 700; }
tr { break-inside: avoid; }
code { font-family: "Noto Sans Mono CJK KR", monospace; font-size: 9.5pt; background: var(--cue);
       padding: 0 3pt; border-radius: 3px; }
blockquote { margin: 8pt 0; padding: 6pt 10pt; border-left: 3px solid var(--accent);
             background: #f5f8fc; font-size: 10pt; break-inside: avoid; }
blockquote p:last-child { margin-bottom: 0; }
ul, ol { margin: 0 0 8pt; padding-left: 18pt; }
li { margin-bottom: 2pt; }
.screen { color: var(--muted); font-size: 9.5pt; margin: 0 0 8pt; }
.screen::before { content: "화면  "; font-weight: 700; color: var(--accent); }
.cue { background: var(--cue); color: var(--muted); font-size: 9.5pt; padding: 4pt 8pt;
       border-radius: 4px; margin: 6pt 0 8pt; }
/* Q&A: 질문 문단과 답 문단을 한 덩어리로 */
p:has(> strong:only-child) { margin-top: 10pt; break-after: avoid; }
"""

html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>본선 발표대본 10분</title><style>{css}</style></head><body>{body}</body></html>"""
html_path.write_text(html)
subprocess.run(["chromium", "--headless=new", "--disable-gpu", "--no-sandbox",
                "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}",
                html_path.resolve().as_uri()], check=True, capture_output=True)
print(pdf_path)
