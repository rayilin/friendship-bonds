# -*- coding: utf-8 -*-
"""產生 教學網頁/media/ 概念圖庫：img/*.jpg（600x400）＋ thumb/*.jpg（240 寬）＋ images.js
不需要 AI 生圖 key，純 Pillow 繪製，配色與簡報一致。
"""
import sys, os, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA = os.path.join(ROOT, "教學網頁", "media")
IMG = os.path.join(MEDIA, "img")
THUMB = os.path.join(MEDIA, "thumb")
os.makedirs(IMG, exist_ok=True); os.makedirs(THUMB, exist_ok=True)

F_BOLD = r"C:\Windows\Fonts\msjhbd.ttc"
F_REG = r"C:\Windows\Fonts\msjh.ttc"

GROUPS = {"01": ("概念", (31, 110, 84)), "02": ("禮儀與原則", (232, 100, 27)), "03": ("表達與肯定", (142, 68, 19))}
CARDS = [
    ("01", "c01", "通訊軟體溝通禮儀", "先打招呼・說話清楚"),
    ("01", "c02", "照片分享的底線", "經過同意才上傳"),
    ("01", "c03", "貼文要節制", "重質不重量"),
    ("01", "c04", "轉傳與查證", "確認真假再分享"),
    ("01", "c05", "按讚數的迷思", "讚數≠友誼深淺"),
    ("01", "c06", "線上與真實互動", "兩者平衡最健康"),
    ("01", "c07", "自我肯定", "我的價值不由讚數決定"),
    ("02", "p01", "原則 1", "同意：先問過對方"),
    ("02", "p02", "原則 2", "節制：想清楚再發文"),
    ("02", "p03", "原則 3", "查證：看來源找證據"),
    ("02", "s01", "停", "不急著轉傳，先停三秒"),
    ("02", "s02", "看", "誰發布的？有根據嗎？"),
    ("02", "s03", "問", "不確定就查證或問大人"),
    ("02", "s04", "假訊息的特徵", "恐嚇轉傳、聳動標題"),
    ("02", "s05", "資訊倫理", "遵守網路的規範"),
    ("02", "s06", "禮貌文字", "當面也敢說才傳出去"),
    ("02", "s07", "尊重隱私", "私人對話不公開"),
    ("03", "e01", "隱藏想法", "忍住不說，委屈累積"),
    ("03", "e02", "不顧對方", "只顧自己，傷了友誼"),
    ("03", "e03", "兼顧雙方", "說出自己，尊重對方"),
    ("03", "e04", "表達句型", "我覺得→因為→我希望"),
    ("03", "e05", "友誼行動", "線上聯繫＋真實相處"),
]

W, H = 600, 400
def font(path, size):
    return ImageFont.truetype(path, size)

entries = []
for g, code, title, sub in CARDS:
    gname, (r, gr, b) = GROUPS[g]
    img = Image.new("RGB", (W, H), (r, gr, b))
    d = ImageDraw.Draw(img)
    # 半透明深色條（用實色近似）
    d.rectangle([0, 0, W, 64], fill=(int(r*0.8), int(gr*0.8), int(b*0.8)))
    d.text((24, 14), f"友誼維繫・{gname}", font=font(F_REG, 26), fill=(247, 243, 233))
    # 標題置中
    tf = font(F_BOLD, 56)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 150), title, font=tf, fill=(255, 255, 255))
    ts = font(F_REG, 30)
    tw2 = d.textlength(sub, font=ts)
    d.text(((W - tw2) / 2, 240), sub, font=ts, fill=(255, 240, 220))
    # 底部裝飾線
    d.rectangle([60, 330, W - 60, 336], fill=(255, 255, 255))
    p = os.path.join(IMG, code + ".jpg")
    img.save(p, quality=88)
    img.thumbnail((240, 160))
    img.save(os.path.join(THUMB, code + ".jpg"), quality=85)
    entries.append({"code": code, "group": g, "title": f"{title}｜{sub}",
                    "img": f"media/img/{code}.jpg", "thumb": f"media/thumb/{code}.jpg"})

js = "const GALLERY = " + json.dumps(entries, ensure_ascii=False, indent=2).replace('"code": ', '"code":') + ";\n"
open(os.path.join(MEDIA, "images.js"), "w", encoding="utf-8").write(js)
print("OK 圖庫", len(entries), "張 →", MEDIA)
