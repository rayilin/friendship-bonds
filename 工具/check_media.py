# -*- coding: utf-8 -*-
import json, subprocess, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
MEDIA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "教學網頁", "media")
for p in ["p09", "p12", "p16", "p18"]:
    f = os.path.join(MEDIA, p + ".mp4")
    if not os.path.exists(f):
        print(p, "MISSING"); continue
    out = subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", f],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    d = json.loads(out)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    a = [s for s in d["streams"] if s["codec_type"] == "audio"]
    print(f"{p}: {v['width']}x{v['height']} {float(d['format']['duration']):.1f}s audio={'yes' if a else 'NO'} {os.path.getsize(f)/1e6:.1f}MB")
