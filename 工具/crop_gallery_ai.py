# -*- coding: utf-8 -*-
"""把 圖庫原始/ 裡 draw-gemini 產出的 {code}_時間戳.jpg 裁成 600x400 並建縮圖。
不重新生圖，只做後處理。
"""
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from PIL import Image

ROOT = r"C:\Users\rayi\Documents\健康與體育教學專欄\友誼維繫"
MEDIA = os.path.join(ROOT, "教學網頁", "media")
IMG = os.path.join(MEDIA, "img")
THUMB = os.path.join(MEDIA, "thumb")
GEN = os.path.join(ROOT, "圖庫原始")
os.makedirs(IMG, exist_ok=True); os.makedirs(THUMB, exist_ok=True)

CODES = ["c01","c02","c03","c04","c05","c06","c07",
         "p01","p02","p03",
         "s01","s02","s03","s04","s05","s06","s07",
         "e01","e02","e03","e04","e05"]

ok, miss = 0, []
for code in CODES:
    cands = [f for f in glob.glob(os.path.join(GEN, code + "_*.jpg"))
             + glob.glob(os.path.join(GEN, code + "_*.png"))
             + glob.glob(os.path.join(GEN, code + ".jpg"))
             + glob.glob(os.path.join(GEN, code + ".png"))]
    if not cands:
        miss.append(code); continue
    src = max(cands, key=os.path.getmtime)
    im = Image.open(src).convert("RGB")
    w, h = im.size
    target = 3 / 2
    if w / h > target:
        nw = int(h * target); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w / target); y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
    im = im.resize((600, 400), Image.LANCZOS)
    im.save(os.path.join(IMG, code + ".jpg"), quality=90)
    th = im.copy(); th.thumbnail((240, 160), Image.LANCZOS)
    th.save(os.path.join(THUMB, code + ".jpg"), quality=85)
    print(f"[{code}] OK  <- {os.path.basename(src)}  {w}x{h}")
    ok += 1

print(f"DONE: {ok}/22 processed")
if miss:
    print("MISSING:", " ".join(miss))
