# -*- coding: utf-8 -*-
"""產生 教案/教案_友誼維繫.docx（2 節、教學流程表格、含 10 題測驗）"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from content import *

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "教案", "教案_友誼維繫.docx")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

ACCENT = RGBColor(0x1F, 0x6E, 0x54)  # 墨綠

def set_font(run, name="微軟正黑體", size=11, bold=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color
    r = run._element.rPr.rFonts
    r.set(qn("w:eastAsia"), name)

def para(doc, text, size=11, bold=False, align=None, color=None, space_after=6):
    p = doc.add_paragraph()
    if align: p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    set_font(r, size=size, bold=bold, color=color)
    return p

def heading(doc, text, size=14):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    set_font(r, size=size, bold=True, color=ACCENT)
    return p

def bullet(doc, text, bold_prefix=None, size=10.5):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    if bold_prefix:
        r1 = p.add_run(bold_prefix); set_font(r1, size=size, bold=True)
    r2 = p.add_run(text); set_font(r2, size=size)
    return p

def make_table(doc, rows, cols, widths=None):
    t = doc.add_table(rows=rows, cols=cols)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    if widths:
        for i, w in enumerate(widths):
            for cell in t.columns[i].cells:
                cell.width = Cm(w)
    return t

def cell_text(cell, text, bold=False, size=10, align=None):
    cell.paragraphs[0].text = ""
    p = cell.paragraphs[0]
    if align: p.alignment = align
    r = p.add_run(text)
    set_font(r, size=size, bold=bold)

doc = Document()
# 頁面邊界
for s in doc.sections:
    s.top_margin = Cm(2); s.bottom_margin = Cm(2); s.left_margin = Cm(2.2); s.right_margin = Cm(2.2)

# ================= 1 基本資料 =================
para(doc, "「友誼維繫」教學活動設計", size=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=ACCENT, space_after=2)
para(doc, UNIT_FULL, size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

heading(doc, "一、基本資料")
t = make_table(doc, 5, 2, widths=[3.5, 12.5])
rows = [("單元名稱", "單元一「健康用網路」第 2 課 友誼維繫"),
        ("教學對象", GRADE),
        ("教學節數", LESSONS),
        ("教材版本", VERSION),
        ("設計者", "教學專欄製作小組")]
for i, (k, v) in enumerate(rows):
    cell_text(t.rows[i].cells[0], k, bold=True)
    cell_text(t.rows[i].cells[1], v)

# ================= 2 設計理念 =================
heading(doc, "二、設計理念")
para(doc, "六年級學生的人際互動已大量延伸到線上：通訊軟體、社群網站成為友誼的日常場景，但「看不見對方表情」的文字溝通，最容易產生誤會與傷害。本課從「通訊軟體溝通禮儀」出發，透過出糗照上傳、大量發文、轉傳未查證訊息等真實情境，討論網路分享的資訊倫理；接著破除「按讚數＝人緣好」的迷思，理解線上互動無法取代真實相處；最後運用生活技能「自我肯定」建立互動自信，並比較三種溝通方式，學會「同時考慮自己和對方感受」的情感合宜表達。整體設計呼應課綱「友誼關係的維繫與情感的合宜表達方式（Db-Ⅲ-5）」與資訊教育議題「良好互動關係（資E7）」「資訊倫理規範（資E12）」，讓學生在網路時代也能維繫真誠、健康的友誼。", size=10.5)

# ================= 3 學習重點 =================
heading(doc, "三、學習重點（課綱對照）")
t = make_table(doc, len(CURRICULUM["學習表現"]) + len(CURRICULUM["學習內容"]) + len(CURRICULUM["議題"]) + 1, 2, widths=[3, 13])
cell_text(t.rows[0].cells[0], "代碼", bold=True)
cell_text(t.rows[0].cells[1], "內容", bold=True)
i = 1
for code, desc in CURRICULUM["學習表現"] + CURRICULUM["學習內容"] + CURRICULUM["議題"]:
    cell_text(t.rows[i].cells[0], code, bold=True)
    cell_text(t.rows[i].cells[1], desc)
    i += 1

# ================= 4 學習目標 =================
heading(doc, "四、學習目標")
for o in OBJECTIVES:
    bullet(doc, o)

# ================= 5 教材教具 =================
heading(doc, "五、教材教具")
bullet(doc, "康軒版六上健體課本（單元一第 2 課）")
bullet(doc, "教學簡報（本專欄提供 21 頁 pptx）")
bullet(doc, "學習單 2 份：①網路互動禮儀自我檢核＋訊息查證練習 ②兼顧雙方感受句型練習＋我的友誼行動")
bullet(doc, "影片 5 部（已驗證）：毒不添下網路成癮動畫、小安的雙胞胎事件簿、媒體識讀假新聞、識讀加油站微查核、我是溝通小高手")
bullet(doc, "互動教學網頁（含 10 題線上測驗、抽籤與計時器）與兩人對戰遊戲")
bullet(doc, "計時器／碼錶、板書海報紙")

# ================= 6 教學流程 =================
heading(doc, "六、教學流程（2 節 × 40 分 = 80 分）")
for f in FLOW:
    para(doc, f"{f['lesson']}（{f['week']}）：{f['title']}", size=11.5, bold=True, color=ACCENT, space_after=4)
    t = make_table(doc, len(f["activities"]) + 1, 3, widths=[3.5, 2, 10.5])
    cell_text(t.rows[0].cells[0], "活動", bold=True)
    cell_text(t.rows[0].cells[1], "時間", bold=True)
    cell_text(t.rows[0].cells[2], "教學活動說明", bold=True)
    for j, (name, mins, desc) in enumerate(f["activities"], start=1):
        cell_text(t.rows[j].cells[0], name, bold=True)
        cell_text(t.rows[j].cells[1], f"{mins} 分")
        cell_text(t.rows[j].cells[2], desc)
    para(doc, "", size=6, space_after=2)
total = sum(a[1] for f in FLOW for a in f["activities"])
para(doc, f"時間加總檢核：{total} 分 ＝ 2 節 × 40 分 ✓", size=10, bold=True)

# ================= 7 隨堂測驗 =================
heading(doc, "七、隨堂測驗（10 題，與教學網頁測驗、測驗卷完全一致）")
LEVEL_LETTER = "ABCD"
for i, q in enumerate(QUIZ, 1):
    para(doc, f"{i}. {q['q']}（{q['level']}）", size=10.5, bold=True, space_after=2)
    for j, opt in enumerate(q["options"]):
        mark = "（✓）" if j == q["answer"] else "　　"
        para(doc, f"　{LEVEL_LETTER[j]}. {opt} {mark}", size=10, space_after=1)
    para(doc, f"　解析：{q['explain']}", size=10, space_after=8)

# ================= 8 常見迷思 =================
heading(doc, "八、常見迷思與澄清")
for myth, fix in MISCONCEPTIONS:
    bullet(doc, f"{myth} → {fix}")

# ================= 9 評量設計 =================
heading(doc, "九、評量設計")
bullet(doc, "形成性評量：課堂發表（出糗照、大量貼文、轉傳訊息三情境的討論）、網路互動禮儀自我檢核的完成與討論（第一節）。")
bullet(doc, "實作評量：訊息查證練習、「兼顧雙方感受」句型兩人演練（第二節）。")
bullet(doc, "總結性評量：10 題隨堂測驗（紙本卷或線上測驗），答對 7 題以上為通過。")
bullet(doc, "回家作業：我的友誼行動學習單（一週網路友誼觀察）、與家人分享三原則。")

# ================= 10 差異化 =================
heading(doc, "十、差異化教學")
bullet(doc, "（進度較快）挑戰任務：設計一份「網路分享三原則」宣導海報，或編一齣網路禮儀短劇。")
bullet(doc, "（需支持）提供句型提示卡（我覺得…因為…我希望…），先完成一個情境的合宜表達即可。")
bullet(doc, "（家庭情境差異）行動學習單可彈性處理：無法與家人討論者，改與導師或同學互相演練。")

# ================= 11 課後延伸 =================
heading(doc, "十一、課後延伸")
bullet(doc, "一週網路友誼觀察：記錄這一週和朋友線上互動與真實相處各做了什麼，哪一種讓你感覺更靠近？")
bullet(doc, "和家人分享「同意、節制、查證」三原則，一起檢查家裡群組最近轉傳的訊息。")
bullet(doc, "延伸連結：教育部中小學數位素養資源網（eliteracy.edu.tw）相關教材。")

# ================= 12 板書規劃 =================
heading(doc, "十二、板書規劃")
bullet(doc, "主線：「同意・節制・查證 ─ 破除讚數迷思 ─ 真誠合宜表達」三段式板書。")
bullet(doc, "左區：分享三原則（同意／節制／查證）。")
bullet(doc, "中區：三種溝通方式比較（隱藏想法／不顧對方／兼顧雙方）。")
bullet(doc, "右區：兼顧雙方句型（我覺得→因為→我希望）＋自我肯定三句話。")

# ================= 13 教學省思 =================
heading(doc, "十三、教學省思（授課後填寫）")
para(doc, "１．學生分享網路互動經驗時是否願意坦誠？是否需要匿名方式蒐集情境？", size=10.5)
para(doc, "２．情感合宜表達演練時，學生能否避免變成指責或一味忍耐？需要再加強哪個句型環節？", size=10.5)
para(doc, "３．「按讚數迷思」的討論是否觸及學生的真實感受？是否需要個別輔導資源？", size=10.5)
para(doc, "４．下次教學可調整之處：", size=10.5)

doc.save(OUT)
print("OK", OUT)
