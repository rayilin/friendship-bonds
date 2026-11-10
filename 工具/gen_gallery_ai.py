# -*- coding: utf-8 -*-
"""用 draw-gemini 產生 22 張概念圖庫插圖，裁切 600x400 並重建縮圖。
卡片清單與 code 必須和 build_gallery.py 的 CARDS 一致。
"""
import io, sys, os, subprocess, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from PIL import Image

ROOT = r"C:\Users\rayi\Documents\健康與體育教學專欄\友誼維繫"
MEDIA = os.path.join(ROOT, "教學網頁", "media")
IMG = os.path.join(MEDIA, "img")
THUMB = os.path.join(MEDIA, "thumb")
GEN = os.path.join(ROOT, "圖庫原始")
os.makedirs(IMG, exist_ok=True); os.makedirs(THUMB, exist_ok=True); os.makedirs(GEN, exist_ok=True)

PS = os.path.expanduser(r"~\.config\opencode\skills\draw-gemini\draw-gemini.ps1")

STYLE = ("Flat vector storybook illustration for children, warm cream background, "
         "deep green and warm orange accents, cute Taiwanese elementary school kids, "
         "rounded soft shapes, clean composition, friendly and positive mood. "
         "No text, no letters, no numbers anywhere in the image.")

CARDS = [
    ("c01", "A child holding a smartphone, smiling politely while typing a friendly greeting message, a speech bubble with a simple smiley face floating above the phone."),
    ("c02", "A child showing a tablet to a friend and asking permission before sharing a photo, the friend nodding happily, both sitting side by side."),
    ("c03", "A child calmly posting a single nice photo on a large social media wall, keeping only a few posts, feeling relaxed and balanced."),
    ("c04", "A child with a magnifying glass checking a message on a floating phone screen, a big question mark beside it, detective style."),
    ("c05", "A child standing confidently, with a few small heart icons floating gently around, ignoring a big flashy scoreboard of likes behind them."),
    ("c06", "Two kids chatting happily face to face on a playground in the foreground, and above them a soft cloud showing the same two kids waving on a video call."),
    ("c07", "A child standing tall with arms crossed and a proud warm smile, surrounded by a gentle golden glow and small stars."),
    ("p01", "A child pointing at a camera icon on a phone screen while asking a friend for agreement, the friend giving a thumbs up."),
    ("p02", "A child pausing thoughtfully with a finger on their chin, looking at a phone, with a small clock icon showing patience."),
    ("p03", "A child checking a message against a newspaper and a globe on a desk, looking focused and careful."),
    ("s01", "A child holding up an open palm toward a flood of message bubbles, the bubbles stopping politely in the air."),
    ("s02", "A child examining a message bubble with a big magnifying glass, looking at a small name tag on the bubble."),
    ("s03", "A child asking a friendly teacher who is kneeling down to their eye level, both smiling, a phone in the child's hand."),
    ("s04", "A tricky message bubble wearing sunglasses with sharp arrows around it, and a child looking at it with cautious doubt."),
    ("s05", "A small group of kids and adults holding hands around a large smartphone, protecting it gently, harmony and teamwork."),
    ("s06", "A child typing a kind message on a phone, and the same child shown in a thought bubble saying the same words kindly face to face."),
    ("s07", "A child gently covering a phone screen showing a chat with a shield icon, keeping it private while smiling politely."),
    ("e01", "A child sitting quietly with a puffed-up sad face, a big closed jar beside them filling up with small grey rain clouds inside."),
    ("e02", "A child shouting with a storm cloud above, another kid covering their ears looking hurt, simple and non-violent."),
    ("e03", "Two kids shaking hands warmly and smiling, each with a small open speech bubble facing each other, mutual respect."),
    ("e04", "A child speaking gently with three floating icons in a row above their head: a heart, a lightbulb, and a small flag, showing feelings, reasons and hope."),
    ("e05", "Two kids walking to school together laughing in the morning sun, and a small phone in one kid's pocket showing a chat bubble, both online and real friendship."),
]

only = sys.argv[1:] if len(sys.argv) > 1 else None

for code, scene in CARDS:
    if only and code not in only:
        continue
    final = os.path.join(IMG, code + ".jpg")
    if os.path.exists(final):
        # 已有 PIL 舊卡，允許覆蓋（AI 版要取代它）
        pass
    prompt = scene + " " + STYLE
    print(f"[{code}] generating ...", flush=True)
    r = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", PS, prompt,
         "-Aspect", "3:2", "-Name", code, "-OutDir", GEN],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(f"[{code}] FAILED\n{r.stdout[-500:]}\n{r.stderr[-500:]}", flush=True)
        continue
    # 找產出檔（腳本可能存 png 或 jpg，檔名含 code）
    cands = [f for f in glob.glob(os.path.join(GEN, code + ".*")) if not f.endswith(".json")]
    if not cands:
        print(f"[{code}] NO OUTPUT FILE\n{r.stdout[-300:]}", flush=True)
        continue
    src = max(cands, key=os.path.getmtime)
    im = Image.open(src).convert("RGB")
    # 裁切到 3:2 再縮到 600x400
    w, h = im.size
    target = 3 / 2
    if w / h > target:
        nw = int(h * target); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
    else:
        nh = int(w / target); y = (h - nh) // 2; im = im.crop((0, y, w, y + nh))
    im = im.resize((600, 400), Image.LANCZOS)
    im.save(final, quality=90)
    th = im.copy(); th.thumbnail((240, 160), Image.LANCZOS)
    th.save(os.path.join(THUMB, code + ".jpg"), quality=85)
    print(f"[{code}] OK {src} -> {final}", flush=True)

print("DONE")
