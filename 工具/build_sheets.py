# -*- coding: utf-8 -*-
"""產生 學習單 2 份 + 測驗卷（docx）"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from content import *

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(ROOT, "學習單"), exist_ok=True)
ACCENT = RGBColor(0x1F, 0x6E, 0x54)

def set_font(run, name="微軟正黑體", size=11, bold=False):
    run.font.name = name; run.font.size = Pt(size); run.font.bold = bold
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)

def para(doc, text, size=11, bold=False, align=None, space_after=6, color=None):
    p = doc.add_paragraph()
    if align: p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    set_font(r, size=size, bold=bold)
    if color is not None:
        r.font.color.rgb = color
    return p

def title(doc, text, sub=None):
    para(doc, text, size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=ACCENT, space_after=2)
    if sub:
        para(doc, sub, size=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

def table(doc, rows, cols, widths=None, header=None):
    t = doc.add_table(rows=rows, cols=cols); t.style = "Table Grid"
    if widths:
        for i, w in enumerate(widths):
            for c in t.columns[i].cells: c.width = Cm(w)
    if header:
        for j, h in enumerate(header):
            c = t.rows[0].cells[j]; c.paragraphs[0].text = ""
            set_font(c.paragraphs[0].add_run(h), size=10.5, bold=True)
    return t

def fill(cell, text, bold=False, size=10.5):
    cell.paragraphs[0].text = ""
    set_font(cell.paragraphs[0].add_run(text), size=size, bold=bold)

# ==================== 學習單 1 ====================
doc = Document()
for s in doc.sections:
    s.top_margin = Cm(2); s.bottom_margin = Cm(2); s.left_margin = Cm(2); s.right_margin = Cm(2)
title(doc, "學習單 1：我的網路互動禮儀檢核", "國小健體六上・友誼維繫　班級：______　座號：______")

para(doc, "一、網路互動禮儀自我檢核表", bold=True, size=13)
para(doc, "符合的打「✓」，誠實作答才能幫助自己。", size=9.5)
checks = [
    "我用通訊軟體找人時，會先打招呼再說事情。",
    "我曾經連環傳很多訊息，把朋友的訊息洗掉（洗版）。",
    "我曾在深夜或很晚的時間傳訊息給同學。",
    "上傳照片前，我會先問過照片裡所有的人。",
    "我曾在社群網站發布很多篇貼文，或沒想清楚就發文。",
    "收到「快轉傳！」的訊息，我會先查證再決定要不要轉傳。",
    "我曾經轉傳過沒有查證過的訊息。",
    "我會尊重別人的隱私，不公開朋友的私人對話與照片。",
]
t = table(doc, len(checks) + 1, 3, widths=[1.2, 12, 2.8], header=None)
fill(t.rows[0].cells[0], "題號", bold=True); fill(t.rows[0].cells[1], "檢核項目", bold=True); fill(t.rows[0].cells[2], "符合（✓）", bold=True)
for i, c in enumerate(checks, 1):
    fill(t.rows[i].cells[0], str(i)); fill(t.rows[i].cells[1], c)
para(doc, "計分：✓ 有 0～2 個＝網路禮儀好榜樣　｜　3～5 個＝要注意囉　｜　6 個以上＝請照「分享三原則」調整", size=10, bold=True, space_after=10)

para(doc, "二、訊息查證練習", bold=True, size=13)
para(doc, "下面是一則群組流傳的訊息，用「停・看・問」三步驟完成表格。", size=9.5)
para(doc, "訊息內容：「緊急！明天全校停課，快轉傳給所有家長！」（沒有來源、沒有署名）", size=10.5, bold=True, space_after=6)
t = table(doc, 4, 2, widths=[3, 13])
for j, h in enumerate(["步驟", "我的做法"]):
    fill(t.rows[0].cells[j], h, bold=True)
rows = [("停", "我會急著轉傳嗎？先停幾秒，我的決定：＿＿＿＿"),
        ("看", "這則訊息的來源是誰？有沒有署名或根據？＿＿＿＿"),
        ("問", "我可以查哪裡？（學校網站／問老師或家長）＿＿＿＿")]
for i, (a, b) in enumerate(rows, 1):
    fill(t.rows[i].cells[0], a, bold=True); fill(t.rows[i].cells[1], b)
doc.save(os.path.join(ROOT, "學習單", "學習單1_網路互動禮儀檢核.docx"))

# ==================== 學習單 2 ====================
doc = Document()
for s in doc.sections:
    s.top_margin = Cm(2); s.bottom_margin = Cm(2); s.left_margin = Cm(2); s.right_margin = Cm(2)
title(doc, "學習單 2：兼顧雙方感受的表達練習", "國小健體六上・友誼維繫　班級：______　座號：______")

para(doc, "一、我的三個優點（自我肯定）", bold=True, size=13)
para(doc, "寫下三個你的優點，相信自己值得被喜歡：", size=10.5)
for i in range(3):
    para(doc, f"{i+1}. ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", size=10.5, space_after=8)

para(doc, "二、兼顧雙方感受的表達練習", bold=True, size=13)
para(doc, "句型：我覺得（感受）……，因為（原因）……，我希望（期望）……", size=10.5)
situations = [
    "情境：同學沒有問過你，就把你的糗照上傳到社群網站。",
    "情境：好朋友答應週末一起打球，結果沒來也沒說原因。",
    "情境：同學一直在群組連環傳訊息，功課都沒辦法寫。",
]
for i, s in enumerate(situations, 1):
    para(doc, s, size=10.5, bold=True, space_after=2)
    para(doc, f"我的表達：我覺得＿＿＿＿＿＿，因為＿＿＿＿＿＿，我希望＿＿＿＿＿＿。", size=10.5, space_after=10)
para(doc, "提醒：先說出自己的感受（不隱藏），也別忘了聽聽對方怎麼說（不指責）。", size=10, color=ACCENT)

para(doc, "三、我的友誼行動（一週觀察）", bold=True, size=13)
t = table(doc, 4, 2, widths=[6, 10])
fill(t.rows[0].cells[0], "項目", bold=True); fill(t.rows[0].cells[1], "我的觀察與行動", bold=True)
items = ["這一週，我和朋友的「線上互動」做了什麼？", "這一週，我和朋友的「真實相處」做了什麼？", "哪一種互動讓我感覺和朋友更靠近？為什麼？"]
for i, it in enumerate(items, 1):
    fill(t.rows[i].cells[0], it)
    fill(t.rows[i].cells[1], "")
doc.save(os.path.join(ROOT, "學習單", "學習單2_合宜表達與友誼行動.docx"))

# ==================== 測驗卷 ====================
doc = Document()
for s in doc.sections:
    s.top_margin = Cm(2); s.bottom_margin = Cm(2); s.left_margin = Cm(2); s.right_margin = Cm(2)
title(doc, "「友誼維繫」隨堂測驗", "國小健體六上　班級：______　座號：______　得分：______")
para(doc, "一、選擇題（每題 10 分，共 100 分）", bold=True, size=12)
LETTER = "ABCD"
for i, q in enumerate(QUIZ, 1):
    para(doc, f"（　）{i}. {q['q']}", size=11, bold=False, space_after=2)
    for j, opt in enumerate(q["options"]):
        para(doc, f"　　　{LETTER[j]}. {opt}", size=11, space_after=1)
    para(doc, "", size=4, space_after=2)

doc.add_page_break()
para(doc, "【教師用】答案與解析", size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=ACCENT)
t = table(doc, 2, 11, widths=[2] + [1.3] * 10)
fill(t.rows[0].cells[0], "題號", bold=True)
fill(t.rows[1].cells[0], "答案", bold=True)
for j in range(10):
    fill(t.rows[0].cells[j + 1], str(j + 1), bold=True)
    fill(t.rows[1].cells[j + 1], LETTER[QUIZ[j]["answer"]], bold=True)
para(doc, "", space_after=6)
for i, q in enumerate(QUIZ, 1):
    para(doc, f"{i}. （{q['level']}）{q['explain']}", size=10, space_after=3)
doc.save(os.path.join(ROOT, "學習單", "測驗卷_友誼維繫.docx"))

print("OK 學習單x2 + 測驗卷")
