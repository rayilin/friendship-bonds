# -*- coding: utf-8 -*-
"""產生 簡報/友誼維繫_教學簡報.pptx（21 頁 16:9）
字型：微軟正黑體（補 a:ea，避免中文掉字型）
配色：米白 #F7F3E9／墨綠 #1F6E54／橙 #E8641B
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from content import *

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.enum.shapes import MSO_SHAPE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "簡報", "友誼維繫_教學簡報.pptx")

INK = RGBColor(0x1F, 0x6E, 0x54)      # 墨綠
ORANGE = RGBColor(0xE8, 0x64, 0x1B)   # 橙
CREAM = RGBColor(0xF7, 0xF3, 0xE9)    # 米白
DARK = RGBColor(0x33, 0x33, 0x33)
RED = RGBColor(0xC0, 0x39, 0x2B)

def _set_ea(run):
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = rPr.makeelement(qn("a:ea"), {})
        rPr.append(ea)
    ea.set("typeface", "微軟正黑體")

def add_text(slide, x, y, w, h, text, size=20, bold=False, color=DARK,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="微軟正黑體"):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.name = font
    r.font.color.rgb = color
    _set_ea(r)
    return tb

def add_bullets(slide, x, y, w, h, items, size=18, gap=1.0, color=DARK):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(10 * gap)
        r = p.add_run(); r.text = "• " + it
        r.font.size = Pt(size); r.font.name = "微軟正黑體"; r.font.color.rgb = color
        _set_ea(r)
    return tb

def bg(slide, color=CREAM):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color

def band(slide, y=6.6, color=INK, h=0.9, text=None, tcolor=CREAM):
    from pptx.util import Inches as I
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, I(0), I(y), I(13.333), I(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = color; shp.line.fill.background()
    if text:
        tf = shp.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
        r = p.add_run(); r.text = text
        r.font.size = Pt(14); r.font.name = "微軟正黑體"; r.font.color.rgb = tcolor
        _set_ea(r)

def page_title(slide, text, color=INK):
    add_text(slide, 0.6, 0.35, 12.1, 1.0, text, size=30, bold=True, color=color)

def new_slide(prs, color=CREAM):
    s = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    bg(s, color)
    return s

def chip(slide, x, y, w, h, text, fill_color=INK, tcolor=CREAM, size=16, bold=True):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill_color
    shp.line.fill.background()
    tf = shp.text_frame; tf.word_wrap = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    r = tf.paragraphs[0].add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.name = "微軟正黑體"; r.font.color.rgb = tcolor
    _set_ea(r)
    return shp

prs = Presentation()
prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)

# ---------- p1 封面 ----------
s = new_slide(prs, INK)
add_text(s, 1, 2.2, 11.3, 1.6, "友誼維繫", size=66, bold=True, color=CREAM, align=PP_ALIGN.CENTER)
add_text(s, 1, 3.9, 11.3, 0.8, "康軒國小健體六上・單元一「健康用網路」第 2 課", size=22, color=CREAM, align=PP_ALIGN.CENTER)
add_text(s, 1, 4.7, 11.3, 0.6, "2 節課｜同意・節制・查證・真誠表達", size=18, color=RGBColor(0xFF, 0xC8, 0x96), align=PP_ALIGN.CENTER)
band(s, y=6.6, text="健康與體育　教學簡報")

# ---------- p2 學習目標 ----------
s = new_slide(prs)
page_title(s, "這兩節課，我們要學會……")
add_bullets(s, 0.9, 1.7, 11.5, 4.6, OBJECTIVES, size=19, gap=1.2)
band(s, text="學習目標｜對應課綱 3b-Ⅲ-2、3b-Ⅲ-4、Db-Ⅲ-5、資E7、資E12")

# ---------- p3 暖身 ----------
s = new_slide(prs)
page_title(s, "暖身：訊息大調查", ORANGE)
add_text(s, 0.9, 1.8, 11.5, 1.2, "今天你用通訊軟體傳了幾則訊息？傳給誰？", size=24, bold=True)
add_bullets(s, 0.9, 3.0, 11.5, 3.0, [
    "和朋友在線上聊天時，有沒有遇過「被誤會」「被洗版」的經驗？",
    "有沒有收到過「快轉傳！」的訊息？你轉傳了嗎？",
], size=20)
band(s, text="第一節｜活動 1　通訊軟體溝通禮儀")

# ---------- p4 通訊禮儀四原則 ----------
s = new_slide(prs)
page_title(s, "通訊軟體溝通禮儀四原則")
cards = [("先打招呼", "有話好好說，先問候再談事"), ("說話清楚", "文字沒有語氣，避免誤會"), ("不洗版", "連環轟炸訊息很失禮"), ("不打擾作息", "深夜傳訊吵醒同學不應該")]
for i, (t1, t2) in enumerate(cards):
    x = 0.75 + (i % 2) * 6.1; y = 1.8 + (i // 2) * 2.2
    chip(s, x, y, 5.6, 1.7, f"{t1}｜{t2}", fill_color=(INK if i % 2 == 0 else ORANGE), size=20)
band(s, text="看不見對方的表情，更需要把禮貌寫進文字裡")

# ---------- p5 迷思破解 ----------
s = new_slide(prs)
page_title(s, "迷思破解：網路上不用講禮貌？", RED)
chip(s, 0.9, 1.9, 11.5, 1.3, "✗ 迷思：反正看不到對方，說話不用客氣", fill_color=RED, size=22)
chip(s, 0.9, 3.5, 11.5, 1.3, "✓ 事實：文字沒有表情和語氣，更容易造成誤會與傷害", fill_color=INK, size=22)
add_text(s, 0.9, 5.2, 11.5, 1.0, "重點：打字前先想三秒——這句話，當面你也敢說嗎？", size=20, bold=True, color=ORANGE)
band(s, text="第一節｜概念澄清")

# ---------- p6 出糗照 ----------
s = new_slide(prs)
page_title(s, "朋友出糗的照片，可以上傳嗎？", ORANGE)
add_bullets(s, 0.9, 1.8, 11.5, 4.2, [
    "情境：同學跌倒的糗照被放上社群網站，全班都在笑",
    "想一想：照片裡的人是什麼心情？",
    "上傳前該做什麼？——先徵得對方的「同意」",
    "照片有別人入鏡，就要尊重對方的感受與意願",
], size=20, gap=1.1)
band(s, text="第一節｜活動 2　網路訊息分享禮儀（一）")

# ---------- p7 貼文節制 ----------
s = new_slide(prs)
page_title(s, "每天發幾十篇貼文，適當嗎？")
add_bullets(s, 0.9, 1.8, 11.5, 4.2, [
    "大量發文會「洗版」：朋友的重要訊息被淹沒",
    "分享重質不重量：想清楚「別人需要看嗎？」",
    "發文前自問：內容適合公開嗎？有無他人入鏡？",
    "兼顧生活：發文不是生活的全部，放下手機也有好事等著你",
], size=20, gap=1.1)
band(s, text="第一節｜活動 2　分享要「節制」")

# ---------- p8 影片頁 ----------
s = new_slide(prs, INK)
page_title(s, "影片：小安的雙胞胎事件簿", CREAM)
add_text(s, 0.9, 2.2, 11.5, 1.2, "看完想一想：", size=26, bold=True, color=CREAM)
add_bullets(s, 0.9, 3.2, 11.5, 2.8, [
    "同學未經同意上傳小安的表演影片，小安受到什麼影響？",
    "如果旁觀的同學願意出聲，事情會不會不一樣？",
], size=20, color=CREAM)
band(s, text="第一節｜影片討論（影片清單見教學網頁 #videos）")

# ---------- p9 分享三原則（動畫頁） ----------
s = new_slide(prs)
page_title(s, "網路分享三原則")
parts = [("同意", "經過同意才分享", INK), ("節制", "重質不重量", ORANGE), ("查證", "確認真假再轉傳", RGBColor(0x8E, 0x44, 0x13))]
for i, (t1, t2, c) in enumerate(parts):
    chip(s, 0.9 + i * 4.1, 2.2, 3.7, 1.6, f"{t1}\n{t2}", fill_color=c, size=18)
add_text(s, 0.9, 4.6, 11.5, 0.8, "同意・節制・查證——三個關卡都通過，才按下「分享」！", size=19, bold=True, color=INK)
band(s, text="第一節｜（此頁附旁白動畫 p09）")

# ---------- p10 轉傳陷阱 ----------
s = new_slide(prs)
page_title(s, "轉傳訊息的陷阱", ORANGE)
add_bullets(s, 0.9, 1.8, 11.5, 4.2, [
    "「不轉傳會倒楣」——用恐嚇要你轉傳的，幾乎都是假訊息",
    "「大家都在傳，應該是真的」——轉傳次數多 ≠ 真實",
    "轉傳未經證實的訊息，可能變成假訊息的幫手",
    "資訊倫理：了解並遵守網路世界的規範，從「不亂轉傳」開始",
], size=20, gap=1.1)
band(s, text="第一節｜活動 3　社群訊息分享禮儀（二）")

# ---------- p11 轉傳三步驟（動畫頁） ----------
s = new_slide(prs)
page_title(s, "轉傳訊息三步驟：停・看・問")
steps = [("1", "停：不急著轉傳，先停三秒"), ("2", "看：看來源——誰發布的？有根據嗎？"), ("3", "問：查新聞或官方網站，不確定就問大人")]
for i, (n, t1) in enumerate(steps):
    chip(s, 0.9 + i * 4.1, 2.2, 3.7, 1.6, f"{n}\n{t1}", fill_color=[INK, ORANGE, RGBColor(0x8E, 0x44, 0x13)][i], size=17)
add_text(s, 0.9, 4.6, 11.5, 0.8, "轉傳前先查證，不做假訊息的幫手。", size=19, bold=True, color=ORANGE)
band(s, text="第一節｜（此頁附旁白動畫 p12）")

# ---------- p12 影片頁 2 ----------
s = new_slide(prs, INK)
page_title(s, "影片：媒體識讀與生活中的微查核", CREAM)
add_bullets(s, 0.9, 2.2, 11.5, 3.4, [
    "假訊息最喜歡什麼樣的標題？（很誇張、很緊急的）",
    "今天起，家裡群組的長輩圖和連鎖信，你可以怎麼幫忙？",
], size=22, color=CREAM)
band(s, text="第一節｜影片討論")

# ---------- p13 按讚迷思 ----------
s = new_slide(prs)
page_title(s, "按讚數的迷思（第二節開場）", ORANGE)
chip(s, 0.9, 1.9, 11.5, 1.3, "✗ 迷思：按讚多＝人緣好＝被大家喜歡", fill_color=RED, size=22)
chip(s, 0.9, 3.5, 11.5, 1.3, "✓ 事實：讚數只是表面數字，真實的友誼建立在相處與關心", fill_color=INK, size=22)
add_text(s, 0.9, 5.2, 11.5, 1.0, "討論：貼文沒有人按讚，你會有什麼反應？那代表朋友不在乎你嗎？", size=19, bold=True, color=ORANGE)
band(s, text="第二節｜活動 4　網路上互動的迷思")

# ---------- p14 線上 vs 真實 ----------
s = new_slide(prs)
page_title(s, "線上互動 vs 真實互動")
cards = [("線上互動", "方便快速、跨越距離｜傳訊息、視訊、遊戲組隊", INK),
         ("真實互動", "一起活動、看見表情語氣｜累積了解與信任", ORANGE),
         ("最好的友誼", "兩種平衡：線上聯繫感情，見面深化感情", RGBColor(0x8E, 0x44, 0x13))]
for i, (t1, t2, c) in enumerate(cards):
    chip(s, 0.9, 1.8 + i * 1.6, 11.5, 1.25, f"{t1}｜{t2}", fill_color=c, size=20)
band(s, text="網路互動無法完全取代面對面相處")

# ---------- p15 自我肯定 ----------
s = new_slide(prs)
page_title(s, "自我肯定：我的三個優點")
add_bullets(s, 0.9, 1.7, 11.5, 4.4, [
    "拿出學習單，寫下自己的三個優點",
    "例如：很會畫畫、跑步很快、對朋友很守信",
    "別人沒按讚，不代表你不夠好",
    "你的價值，不由別人的滑鼠決定",
], size=20, gap=1.1)
band(s, text="第二節｜活動 5　自我肯定（學習單 2）")

# ---------- p16 溝通三方式（動畫頁） ----------
s = new_slide(prs)
page_title(s, "情感表達的三種方式")
ways = [("隱藏想法", "忍住不說，委屈累積", RED), ("不顧對方", "只顧自己說，傷了友誼", RGBColor(0x8E, 0x44, 0x13)), ("兼顧雙方", "說出自己，也尊重對方", INK)]
for i, (t1, t2, c) in enumerate(ways):
    chip(s, 0.9 + i * 4.1, 2.0, 3.7, 1.6, f"{t1}\n{t2}", fill_color=c, size=17)
add_text(s, 0.9, 4.3, 11.5, 0.9, "例：「你上次說好要來，我等了很久有點難過，是不是遇到什麼事？下次我們再約好嗎？」", size=18, bold=True, color=DARK)
add_text(s, 0.9, 5.5, 11.5, 0.7, "「兼顧雙方」既能表達自己，也維繫關係。", size=18, bold=True, color=ORANGE)
band(s, text="第二節｜活動 6（此頁附旁白動畫 p16）")

# ---------- p17 演練 ----------
s = new_slide(prs)
page_title(s, "上臺演練：兼顧雙方的表達", ORANGE)
add_bullets(s, 0.9, 1.8, 11.5, 4.2, [
    "兩人一組，抽出情境卡（借遊戲不還／訊息洗版／放鴿子）",
    "用句型回應：「我覺得……因為……我希望……」",
    "先說出感受，也聽聽對方的立場",
    "交換角色再練一次；請 2 組上臺發表",
], size=20, gap=1.1)
band(s, text="第二節｜活動 6 演練")

# ---------- p18 自我肯定三句話（動畫頁） ----------
s = new_slide(prs)
page_title(s, "自我肯定三句話")
lines = [("1", "我有我的優點，我喜歡自己"), ("2", "讚數不代表我的價值"), ("3", "真實的朋友，在乎的是我這個人")]
for i, (n, t1) in enumerate(lines):
    chip(s, 0.9, 1.7 + i * 1.5, 1.0, 1.0, n, fill_color=ORANGE, size=20)
    add_text(s, 2.1, 1.82 + i * 1.5, 10.4, 0.9, t1, size=21, bold=True)
band(s, text="第二節｜（此頁附旁白動畫 p18）")

# ---------- p19 概念圖 ----------
s = new_slide(prs)
page_title(s, "總複習：一張圖記住這一課")
chip(s, 5.2, 1.6, 3.0, 1.0, "網路是友誼的橋", fill_color=INK, size=20)
chip(s, 5.2, 3.0, 3.0, 1.0, "禮貌與倫理不能少", fill_color=RED, size=20)
chip(s, 0.9, 4.5, 3.6, 1.3, "分享三原則\n同意・節制・查證", fill_color=ORANGE, size=16)
chip(s, 4.9, 4.5, 3.6, 1.3, "破除迷思\n讚數≠友誼", fill_color=RGBColor(0x8E, 0x44, 0x13), size=16)
chip(s, 8.9, 4.5, 3.6, 1.3, "合宜表達\n兼顧雙方感受", fill_color=RGBColor(0x4A, 0x8F, 0x3C), size=16)
band(s, text="同意・節制・查證＋真誠表達＝網路時代的好友誼")

# ---------- p20 測驗 ----------
s = new_slide(prs)
page_title(s, "隨堂測驗：10 題挑戰", ORANGE)
add_bullets(s, 0.9, 1.8, 11.5, 4.0, [
    "紙本測驗卷或線上測驗（教學網頁 #quiz）",
    "10 題選擇題，答對 7 題以上過關",
    "線上版每題都有解析，答錯記得看「錯在哪裡」",
    "挑戰：和同學玩「友誼維繫對戰」，10 題搶答！",
], size=20, gap=1.1)
band(s, text="評量｜了解自己的學習成果")

# ---------- p21 總結 ----------
s = new_slide(prs, INK)
add_text(s, 1, 2.0, 11.3, 1.2, "記得這句話", size=30, bold=True, color=CREAM, align=PP_ALIGN.CENTER)
add_text(s, 1, 3.0, 11.3, 1.4, "螢幕連結距離，真誠維繫友誼。", size=38, bold=True, color=RGBColor(0xFF, 0xC8, 0x96), align=PP_ALIGN.CENTER)
add_text(s, 1, 4.6, 11.3, 0.8, "同意・節制・查證・兼顧雙方，做網路上的好朋友！", size=24, color=CREAM, align=PP_ALIGN.CENTER)
band(s, text="友誼維繫｜康軒國小健體六上 單元一 第 2 課")

prs.save(OUT)
print("OK", OUT, "slides:", len(prs.slides._sldIdLst))
