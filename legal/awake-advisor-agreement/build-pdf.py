#!/usr/bin/env python3
"""Build a fixed-layout PDF from the Advisor Agreement's canonical Markdown."""
import re
import hashlib
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, PageBreak, Spacer
from reportlab.pdfbase import pdfdoc

# ReportLab 4 passes a Python 3.9+ keyword that this project's Python 3.8 lacks.
pdfdoc.md5 = lambda *args, **kwargs: hashlib.md5(*args)

HERE = Path(__file__).resolve().parent
STEM = "awake-advisor-agreement"
blocks = (HERE / f"{STEM}.md").read_text().strip().split("\n\n")
output = HERE / f"{STEM}.pdf"
ink = colors.HexColor("#161411")
red = colors.HexColor("#B83A2E")
styles = {
    "title": ParagraphStyle("Title", fontName="Helvetica-Bold", fontSize=22, leading=27, textColor=ink, spaceAfter=12),
    "subtitle": ParagraphStyle("Subtitle", fontName="Helvetica", fontSize=8.5, leading=12, textColor=colors.HexColor("#555555"), spaceAfter=8),
    "h2": ParagraphStyle("Section", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=red, spaceBefore=15, spaceAfter=8, keepWithNext=True),
    "body": ParagraphStyle("Body", fontName="Helvetica", fontSize=9.3, leading=14, textColor=ink, spaceAfter=7, splitLongWords=False),
}


def marked(value):
    value = escape(value)
    return re.sub(r"\[([^\]]+)\]", r'<font backColor="#F6EBC8">[\1]</font>', value)


def page_decoration(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(0.85 * inch, 10.48 * inch, "AWAKE ADVISOR AGREEMENT  |  VERSION 1.0")
    canvas.drawRightString(7.65 * inch, 0.52 * inch, f"cofounder.community  |  CC BY 4.0  |  {doc.page}")
    canvas.restoreState()


doc = BaseDocTemplate(str(output), pagesize=letter, leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                      topMargin=0.95 * inch, bottomMargin=0.82 * inch,
                      title="Awake Advisor Agreement", author="Amit Rathore and AwakeVC")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, leftPadding=0, rightPadding=0,
              topPadding=0, bottomPadding=0)
doc.addPageTemplates(PageTemplate(id="agreement", frames=[frame], onPage=page_decoration))
story = []
for i, block in enumerate(blocks):
    if block.startswith("# "):
        story.append(Paragraph(escape(block[2:]), styles["title"]))
    elif block.startswith("## "):
        title = block[3:]
        if title == "1. Engagement and services":
            story.append(PageBreak())
        story.append(Paragraph(escape(title), styles["h2"]))
    else:
        if "\n" in block:
            raise ValueError("Unsupported multiline Markdown block: " + block[:80])
        story.append(Paragraph(marked(block), styles["subtitle"] if i == 1 else styles["body"]))
doc.build(story)
print(f"Built {output.name} from canonical Markdown.")
