# -*- coding: utf-8 -*-
"""產生 4 段旁白動畫專案：影片/p09 分享三原則、p12 轉傳三步驟、p16 溝通三方式、p18 自我肯定三句話
用法：python build_anim.py gen   （產 VO + HTML）
      之後用 hyperframes check / snapshot / render
"""
import sys, os, subprocess, math, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VID = os.path.join(ROOT, "影片")
MEDIA = os.path.join(ROOT, "教學網頁", "media")
os.makedirs(MEDIA, exist_ok=True)

VOICE = "zh-TW-HsiaoChenNeural"

PAGES = {
    "p09": {
        "title": "網路分享三原則",
        "vo": "在網路分享東西之前，要記住三個原則：同意，先問過照片裡的朋友；節制，發文想清楚，不要洗版；查證，確認訊息是真的才分享。三關都通過，才按下分享！",
        "steps": [("同意", "先問過對方才分享"), ("節制", "重質不重量"), ("查證", "確認真假再轉傳")],
        "end": "三關都通過，才按下「分享」",
        "color_seq": ["#1F6E54", "#E8641B", "#8E4413"],
    },
    "p12": {
        "title": "轉傳訊息三步驟：停・看・問",
        "vo": "收到不確定的訊息，記住三步驟：停，先不要急著轉傳；看，看看來源是誰、有沒有根據；問，查新聞或問大人。轉傳前先查證，不做假訊息的幫手！",
        "steps": [("1", "停：不急著轉傳，先停三秒"), ("2", "看：來源是誰？有根據嗎？"), ("3", "問：查新聞或問大人")],
        "end": "轉傳前先查證，不做假訊息的幫手",
        "color_seq": ["#1F6E54", "#E8641B", "#8E4413"],
    },
    "p16": {
        "title": "情感表達的三種方式",
        "vo": "表達想法有三種方式：隱藏想法，委屈會越積越多；不顧對方感受，會傷了友誼；最好的方式是兼顧雙方，說出自己的感受，也尊重對方。例如：我覺得很難過，因為你沒有來，我希望下次我們再約好。",
        "steps": [("隱藏想法", "忍住不說，委屈累積"), ("不顧對方", "只顧自己，傷了友誼"), ("兼顧雙方", "說出自己，尊重對方")],
        "end": "兼顧雙方：既能表達自己，也維繫關係",
        "color_seq": ["#C0392B", "#8E4413", "#1F6E54"],
    },
    "p18": {
        "title": "自我肯定三句話",
        "vo": "每天對自己說三句話：我有我的優點，我喜歡自己；讚數不代表我的價值；真實的朋友，在乎的是我這個人。有自信的你，友誼會更穩固！",
        "steps": [("1", "我有我的優點，我喜歡自己"), ("2", "讚數不代表我的價值"), ("3", "真實的朋友，在乎的是我")],
        "end": "有自信的你，友誼會更穩固！",
        "color_seq": ["#1F6E54", "#E8641B", "#8E4413"],
    },
}

HTML = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<title>{pid} {title}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
  @font-face {{ font-family:"Microsoft JhengHei"; src: local("Microsoft JhengHei"); }}
  @font-face {{ font-family:"PingFang TC"; src: local("PingFang TC"); }}
  body {{ margin:0; background:#F7F3E9; }}
  #root {{ position:relative; width:100%; height:100%; overflow:hidden;
          font-family:"Microsoft JhengHei","PingFang TC",sans-serif; }}
  .clip {{ position:absolute; inset:0; }}
  .bar {{ position:absolute; left:0; top:0; width:100%; height:150px;
        background:#1F6E54; display:flex; align-items:center; padding-left:70px; }}
  .bar h1 {{ color:#F7F3E9; font-size:64px; margin:0; }}
  .stage {{ position:absolute; inset:0; }}
  .card {{ position:absolute; box-sizing:border-box; border-radius:28px; padding:24px 28px;
          color:#fff; text-align:center; }}
  .card .big {{ font-size:44px; font-weight:700; }}
  .card .sub {{ font-size:28px; margin-top:12px; }}
  .card.row {{ display:flex; align-items:center; gap:30px; text-align:left; }}
  .card.row .num {{ background:rgba(255,255,255,.25); border-radius:50%; width:88px; height:88px;
                   display:flex; align-items:center; justify-content:center; font-size:44px; font-weight:700; flex:none; }}
  .card.row .txt {{ font-size:38px; font-weight:600; }}
  .sub1 {{ position:absolute; color:#F7F3E9; background:#1F6E54; width:1840px;
          left:40px; top:930px; height:100px; border-radius:20px;
          display:flex; align-items:center; justify-content:center;
          font-size:36px; font-weight:600; }}
</style>
</head>
<body>
<div id="root" data-composition-id="{pid}" data-start="0" data-width="1920" data-height="1080" data-duration="{dur}">
  <section class="clip" id="scene" data-start="0" data-duration="{dur}">
    <div class="bar"><h1 id="t">{title}</h1></div>
    <div class="stage" id="stage">{cards}</div>
    <div class="sub1" id="endline">{end}</div>
    <audio id="vo" src="vo.mp3" data-start="0"></audio>
  </section>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.from("#t", {{ y:-60, opacity:0, duration:0.7, ease:"power3.out" }}, 0.2);
{tweens}
tl.fromTo("#endline", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.6, ease:"power2.out" }}, {endt});
window.__timelines["{pid}"] = tl;
</script>
</body>
</html>"""

def probe(path):
    out = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", str(path)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    return float(json.loads(out)["format"]["duration"])

def gen(pid, cfg):
    d = os.path.join(VID, pid)
    os.makedirs(d, exist_ok=True)
    vo = os.path.join(d, "vo.mp3")
    if not os.path.exists(vo):
        subprocess.run(["edge-tts", "--voice", VOICE, "--rate=+10%", "--text", cfg["vo"], "--write-media", vo], check=True)
    dur = probe(vo)
    n = len(cfg["steps"])
    cardw = 560 if n == 4 else 620
    # 卡片布局
    cards, tweens = [], []
    if n == 5:  # 直列（數字＋文字一行）
        pos = [(140, 175 + i * 148) for i in range(5)]
        sizes = [(1500, 125)] * 5
    elif n == 4:  # 菱形
        pos = [(680, 180), (1230, 420), (680, 660), (130, 420)]
        sizes = [(560, 190)] * 4
    else:  # 3 橫排
        pos = [(150, 400), (703, 400), (1256, 400)]
        sizes = [(500, 260)] * 3
    times = [round(1.4 + i * ((dur - 3.2) / max(n, 1)), 2) for i in range(n)]
    for i, ((t1, t2), c) in enumerate(zip(cfg["steps"], cfg["color_seq"])):
        x, y = pos[i]
        w, h = sizes[i]
        if n == 5:
            inner = f'<div class="num">{t1}</div><div class="txt">{t2}</div>'
            cards.append(f'<div class="card row" id="c{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c};">{inner}</div>')
        else:
            inner = f'<div class="big">{t1}</div><div class="sub">{t2}</div>'
            cards.append(f'<div class="card" id="c{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c};">{inner}</div>')
        tweens.append(f'tl.fromTo("#c{i}", {{ opacity:0, y:50, scale:0.92 }}, {{ opacity:1, y:0, scale:1, duration:0.6, ease:"back.out(1.6)" }}, {times[i]});')
    endt = round(dur - 1.2, 2)
    html = HTML.format(pid=pid, title=cfg["title"], dur=round(dur + 0.8, 2), cardw=cardw,
                       cards="".join(cards), tweens="\n".join(tweens), end=cfg["end"], endt=endt)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return round(dur + 0.8, 2)

if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    for pid, cfg in PAGES.items():
        d = gen(pid, cfg)
        print(pid, "duration", d, "s")
