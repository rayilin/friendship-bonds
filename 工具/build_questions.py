# -*- coding: utf-8 -*-
"""產生 教學網頁/questions.json（30 題對戰題庫，伺服器專用，不得上公開網站）"""
import sys, os, json, io
sys.path.insert(0, os.path.dirname(__file__))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from content import BATTLE_QUESTIONS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "教學網頁", "questions.json")

data = [{"q": q["q"], "o": q["options"], "a": q["answer"], "e": q["explain"]} for q in BATTLE_QUESTIONS]
assert len(data) == 30
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("OK", OUT, len(data), "題")
