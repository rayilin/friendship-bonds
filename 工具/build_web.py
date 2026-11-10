# -*- coding: utf-8 -*-
"""把 教學網頁/index.html 從「網路不沉迷」第一課版改寫成「友誼維繫」第二課版。
每個替換都 assert 恰好發生一次；來源 index.html 必須是第一課完成版。
"""
import sys, os, json, shutil, re, io
sys.path.insert(0, os.path.dirname(__file__))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from content import QUIZ, VIDEOS, FLOW, OBJECTIVES, MISCONCEPTIONS, CURRICULUM

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, "教學網頁")
PATH = os.path.join(WEB, "index.html")

html = open(PATH, encoding="utf-8").read()

def rep(old, new, count=1):
    global html
    assert html.count(old) == count, f"pattern not unique ({html.count(old)}): {old[:60]}"
    html = html.replace(old, new)

# ---------- 1. title / brand ----------
rep("<title>網路不沉迷｜康軒版六上健體・教學專欄</title>",
    "<title>友誼維繫｜康軒版六上健體・教學專欄</title>")
rep('<div class="brand">網路不沉迷<span>。</span><span class="full" style="color:var(--muted);font-weight:400;font-size:13px"> 六上健體</span></div>',
    '<div class="brand">友誼維繫<span>。</span><span class="full" style="color:var(--muted);font-weight:400;font-size:13px"> 六上健體</span></div>')

# ---------- 2. hero ----------
rep('<div class="eyebrow">康軒版・健康與體育・六年級上學期・單元一「健康用網路」第 1 課</div>',
    '<div class="eyebrow">康軒版・健康與體育・六年級上學期・單元一「健康用網路」第 2 課</div>')
rep("<h1>網路不沉迷</h1>", "<h1>友誼維繫</h1>")
rep("<p class=\"lead\">用網路是工具，失控才是問題。三節課的完整教學資源：教案、22 頁簡報（4 段旁白動畫）、10 題互動測驗、抽籤與計時器，以及最下方兩人對戰的「網路不沉迷對戰」。</p>",
    "<p class=\"lead\">螢幕連結距離，真誠維繫友誼。兩節課的完整教學資源：教案、21 頁簡報（4 段旁白動畫）、10 題互動測驗、抽籤與計時器，以及最下方兩人對戰的「友誼維繫對戰」。</p>")
rep('<span class="chip g">正向使用</span><span class="chip g">自我篩檢</span><span class="chip g">遠離沉迷</span>',
    '<span class="chip g">通訊禮儀</span><span class="chip g">分享查證</span><span class="chip g">破除迷思</span>')
rep('<span class="chip o">我訊息</span><span class="chip o">自我管理</span><span class="chip o">親子規範</span>',
    '<span class="chip o">自我肯定</span><span class="chip o">合宜表達</span><span class="chip o">友誼行動</span>')
rep('<span class="chip">120 分鐘</span><span class="chip">3 節課</span>',
    '<span class="chip">80 分鐘</span><span class="chip">2 節課</span>')

# ---------- 3. 教案區（整段換） ----------
perf_codes = "、".join(c for c, _ in CURRICULUM["學習表現"])
content_codes = "、".join(c for c, _ in CURRICULUM["學習內容"]) + "｜議題：" + "、".join(c for c, _ in CURRICULUM["議題"])

def lesson_block(f, first=False):
    rows = "".join(
        f'<tr><td class="time">{m} 分</td><td>{name}</td><td>{desc}</td></tr>'
        for name, m, desc in f["activities"])
    return (
        f'<details class="acc{" open" if first else ""}">\n'
        f'      <summary>{f["lesson"]}｜{f["title"]}（{f["minutes"]} 分鐘）</summary>\n'
        f'      <div class="body">\n        <div class="tbl-wrap">\n          <table>\n'
        f'            <thead><tr><th>時間</th><th>活動</th><th>教學說明</th></tr></thead>\n'
        f'            <tbody>\n              {rows}\n            </tbody>\n'
        f'          </table>\n        </div>\n      </div>\n    </details>')

myth_rows = "".join(f"<tr><td>{m}</td><td>{fix}</td></tr>" for m, fix in MISCONCEPTIONS)
obj_lis = "".join(f"<li>{o}</li>" for o in OBJECTIVES)

PLAN = f'''<section id="plan">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <div class="kicker">LESSON PLAN</div>
        <h2>教案</h2>
        <p>兩節課 80 分鐘。第一節通訊軟體與網路分享禮儀；第二節互動迷思、自我肯定與情感合宜表達。</p>
      </div>
      <a class="btn dark small" href="downloads/教案_友誼維繫.docx" download>下載 Word 教案</a>
    </div>

    <div class="grid2" style="margin-bottom:16px">
      <div class="info-card">
        <h3><span class="num">i</span>課程資訊</h3>
        <dl class="kv">
          <dt>領域／科目</dt><dd>健康與體育（健康課）</dd>
          <dt>版本／單元</dt><dd>康軒版 六上 單元一「健康用網路」第 2 課</dd>
          <dt>教學年級</dt><dd>國小六年級（第三學習階段）</dd>
          <dt>節數</dt><dd>2 節（80 分鐘）</dd>
          <dt>課綱對照</dt><dd>{perf_codes}<br>學習內容：{content_codes}</dd>
        </dl>
      </div>
      <div class="info-card">
        <h3><span class="num">◎</span>學習目標</h3>
        <ul class="clean">
          {obj_lis}
        </ul>
      </div>
    </div>

    {lesson_block(FLOW[0], first=True)}

    {lesson_block(FLOW[1])}

    <details class="acc">
      <summary>常見迷思與澄清</summary>
      <div class="body">
        <div class="tbl-wrap">
          <table>
            <thead><tr><th>學生常見想法</th><th>教學澄清</th></tr></thead>
            <tbody>
              {myth_rows}
            </tbody>
          </table>
        </div>
      </div>
    </details>

    <details class="acc">
      <summary>評量設計與差異化</summary>
      <div class="body">
        <p><strong>評量方式：</strong>口頭發表（出糗照、貼文、轉傳三情境的討論）、網路互動禮儀自我檢核的完成與討論（第一節）、訊息查證練習與「兼顧雙方感受」句型演練（實作評量）、隨堂測驗 10 題（第二節末，答對 7 題以上通過）。</p>
        <p><strong>需要協助的學生：</strong>提供「我覺得…因為…我希望…」句型提示卡，先完成一個情境的合宜表達即可；行動學習單可改與導師或同學互相演練。</p>
        <p><strong>學有餘力的學生：</strong>設計一份給全校的「網路分享三原則」宣導海報或短劇，比較不同做法的長期效果。</p>
        <p style="margin-bottom:0"><strong>課後延伸：</strong>一週網路友誼觀察（記錄線上互動與真實相處）、和家人分享「同意、節制、查證」三原則並檢查家中群組訊息。</p>
      </div>
    </details>
  </div>
</section>'''

html, n = re.subn(r'<section id="plan">.*?</section>', lambda m: PLAN, html, count=1, flags=re.S)
assert n == 1, "plan section"

# ---------- 4. 簡報區 ----------
rep("SLIDES · 22 PAGES", "SLIDES · 21 PAGES")
rep('href="downloads/網路不沉迷_教學簡報.pptx"', 'href="downloads/友誼維繫_教學簡報.pptx"', count=2)
rep('<span class="counter" id="counter">1 / 22</span>', '<span class="counter" id="counter">1 / 21</span>')

# ---------- 5. 測驗區 ----------
rep("<p>每題答完立刻看解析。10 題滿分 100 分，答對 7 題以上就過關，成為「網路小達人」。</p>",
    "<p>每題答完立刻看解析。10 題滿分 100 分，答對 7 題以上就過關，成為「友誼小達人」。</p>")

# ---------- 6. 影片區 ----------
rep("<p style=\"color:var(--muted); font-size:13px; margin-top:20px\">建議順序：藍光人（覺察）→ 我的第二人生（影響）→ 毒不添下（方法）→ 我訊息（溝通）→ 新北市宣導（總結）。可作為課前預習或課後複習。</p>",
    "<p style=\"color:var(--muted); font-size:13px; margin-top:20px\">建議順序：毒不添下（健康使用）→ 小安的雙胞胎事件簿（分享禮儀）→ 媒體識讀（查證）→ 識讀加油站（微查核）→ 我是溝通小高手（合宜表達）。可作為課前預習或課後複習。</p>")

# ---------- 7. 對戰區 ----------
rep("<h2>網路不沉迷對戰</h2>", "<h2>友誼維繫對戰</h2>")
rep('title="網路不沉迷對戰" loading="lazy"', 'title="友誼維繫對戰" loading="lazy"')

# ---------- 8. footer ----------
rep("<div><b>網路不沉迷</b>｜康軒版六上健體・教學專欄</div>\n    <div>教案 Word ・ 簡報 22 頁 ・ 4 段旁白動畫 ・ 10 題測驗</div>",
    "<div><b>友誼維繫</b>｜康軒版六上健體・教學專欄</div>\n    <div>教案 Word ・ 簡報 21 頁 ・ 4 段旁白動畫 ・ 10 題測驗</div>")

# ---------- 9. 測驗結果文案 ----------
rep("{ msg = '網路小達人！'; sub = '方法＋規範＋溝通，你全都掌握了。'; }",
    "{ msg = '友誼小達人！'; sub = '同意・節制・查證＋合宜表達，你全都掌握了。'; }")
rep("{ msg = '不錯，再加油！'; sub = '回到簡報看看「遠離迷「網」五招」，再挑戰一次。'; }",
    "{ msg = '不錯，再加油！'; sub = '回到簡報看看「網路分享三原則」，再挑戰一次。'; }")
rep("{ msg = '再來一次！'; sub = '先看一遍簡報 p3–p22，你會發現簡單很多。'; }",
    "{ msg = '再來一次！'; sub = '先看一遍簡報 p3–p21，你會發現簡單很多。'; }")

# ---------- 10. 下載區（整段 dl-grid 換） ----------
DLGRID = '''<div class="dl-grid">
      <a class="dl-card" href="downloads/教案_友誼維繫.docx" download>
        <em>DOCX</em><b>教案（2 節）</b><span>含教學流程、評量、差異化與省思欄</span>
      </a>
      <a class="dl-card" href="downloads/友誼維繫_教學簡報.pptx" download>
        <em>PPTX</em><b>教學簡報</b><span>21 頁，16:9，可直接投影</span>
      </a>
      <a class="dl-card" href="downloads/學習單1_網路互動禮儀檢核.docx" download>
        <em>DOCX</em><b>學習單 ①</b><span>互動禮儀檢核表＋訊息查證練習</span>
      </a>
      <a class="dl-card" href="downloads/學習單2_合宜表達與友誼行動.docx" download>
        <em>DOCX</em><b>學習單 ②</b><span>自我肯定＋兼顧雙方句型練習</span>
      </a>
      <a class="dl-card" href="downloads/測驗卷_友誼維繫.pdf" download>
        <em>PDF</em><b>測驗卷</b><span>10 題，附答案與解析</span>
      </a>
      <a class="dl-card" href="downloads/測驗卷_友誼維繫.docx" download>
        <em>DOCX</em><b>測驗卷（可編輯）</b><span>想改題目就用這份</span>
      </a>
    </div>'''
html, n = re.subn(r'<div class="dl-grid">.*?</div>\s*</div>\s*</section>',
                  lambda m: DLGRID + "\n  </div>\n</section>", html, count=1, flags=re.S)
assert n == 1, "dl-grid"

# ---------- 11. 資料陣列 ----------
ANIM = {9: "p09", 12: "p12", 16: "p16", 18: "p18"}
slides_js = "const SLIDES = [\n" + ",\n".join(
    '  { img:"slides/slide%02d.jpg"%s }' % (i, ', video:"media/%s.mp4"' % ANIM[i] if i in ANIM else "")
    for i in range(1, 22)) + "\n];"

def jstr(s):
    return json.dumps(s, ensure_ascii=False)

quiz_js = "const QUIZ = [\n" + ",\n".join(
    "  { q:%s, o:[%s], a:%d,\n    e:%s }" % (
        jstr(q["q"]), ",".join(jstr(o) for o in q["options"]), q["answer"], jstr(q["explain"]))
    for q in QUIZ) + "\n];"

videos_js = "const VIDEOS = [\n" + ",\n".join(
    "  { t:%s, d:%s, u:%s, id:%s, s:%s }" % (
        jstr(v["title"]), jstr(v["source"] + "｜" + v["use"]),
        jstr("https://www.youtube.com/watch?v=" + v["id"]), jstr(v["id"]), jstr("YouTube"))
    for v in VIDEOS) + "\n];"

html, n = re.subn(r"const SLIDES = \[.*?\n\];", lambda m: slides_js, html, count=1, flags=re.S)
assert n == 1, "SLIDES"
html, n = re.subn(r"const QUIZ = \[.*?\n\];", lambda m: quiz_js, html, count=1, flags=re.S)
assert n == 1, "QUIZ"
html, n = re.subn(r"const VIDEOS = \[.*?\n\];", lambda m: videos_js, html, count=1, flags=re.S)
assert n == 1, "VIDEOS"

# ---------- 12. 殘留檢查 ----------
left = html.count("網路不沉迷")
assert left == 0, f"還有 {left} 處「網路不沉迷」未改"

open(PATH, "w", encoding="utf-8", newline="").write(html)

# ---------- 13. battle.html 標題 ----------
BPATH = os.path.join(WEB, "battle.html")
b = open(BPATH, encoding="utf-8").read()
b = b.replace("網路不沉迷", "友誼維繫")
open(BPATH, "w", encoding="utf-8", newline="").write(b)

# ---------- 14. 複製可下載檔 ----------
dl = os.path.join(WEB, "downloads")
os.makedirs(dl, exist_ok=True)
pairs = [
    ("教案/教案_友誼維繫.docx", "教案_友誼維繫.docx"),
    ("簡報/友誼維繫_教學簡報.pptx", "友誼維繫_教學簡報.pptx"),
    ("學習單/學習單1_網路互動禮儀檢核.docx", "學習單1_網路互動禮儀檢核.docx"),
    ("學習單/學習單2_合宜表達與友誼行動.docx", "學習單2_合宜表達與友誼行動.docx"),
    ("學習單/測驗卷_友誼維繫.docx", "測驗卷_友誼維繫.docx"),
    ("學習單/測驗卷_友誼維繫.pdf", "測驗卷_友誼維繫.pdf"),
]
for src, dst in pairs:
    s = os.path.join(ROOT, src.replace("/", os.sep))
    assert os.path.exists(s), "missing " + s
    shutil.copy2(s, os.path.join(dl, dst))
print("OK index.html 改寫完成 + battle.html 標題 + downloads", len(pairs), "檔")
