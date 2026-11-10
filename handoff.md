# 交接檔（handoff.md）

> 換機器、換設備或換人之前**必讀**！下方只交接**最需要的簡要資訊**。

## 目前專案
友誼維繫（康軒國小健體六上 單元一「健康用網路」第 2 課）教學網頁專案。

## 目前狀態（2026-11-10）
| 項目 | 狀態 |
|------|------|
| 教案 docx | ✅ 完成（officecli validate 0 錯誤） |
| 教學簡報 pptx | ✅ 完成（21 頁，PowerPoint COM 匯出 21 張 JPG） |
| 學習單 | ✅ 2 份＋測驗卷 docx＋PDF |
| 動畫 | ✅ 4 段（p09 16.1s／p12 15.2s／p16 19.0s／p18 13.2s，1920×1080，有音訊） |
| 教學網頁 | ✅ index.html 10 區塊＋語音朗讀＋圖庫 22 張 |
| 對戰 | ✅ 30 題題庫（答案分布 8/8/7/7） |
| 驗收 | ✅ verify_site.js 36/36 全過、本機 console 0 error |
| GitHub Pages | ✅ https://rayilin.github.io/friendship-bonds/（run 42780218036 success） |
| Render 後端 | ⬜ 未部署（對戰走區網 start-battle.bat 即可） |

## 關鍵資訊
- Repo：https://github.com/rayilin/friendship-bonds（公開、main 分支）
- 節數：2 節 × 40 分（第 5、6 週）；課綱 3b-Ⅲ-2、3b-Ⅲ-4、Db-Ⅲ-5＋資E7、資E12
- 影片 5 部（已驗證）：毒不添下、小安的雙胞胎事件簿、媒體識讀(2)、識讀加油站微查核、我是溝通小高手
- questions.json／server.js／start-battle.bat 已被 .gitignore 排除，**不上公開網站**（答案檔隱私要求）
- 產生器在 工具/（content.py 是單一共用內容檔；改內容→重跑 build_*.py→重匯 slides→重渲染動畫→重跑 build_web.py）

## 下次接續
1. 若要修改內容：改 工具/content.py → 重跑對應 build_*.py
2. 若要部署對戰後端：Render 藍圖已備妥（battle-server.js／render.yaml）
3. 下一課：單元二「打造健康消費心法」屬單元二範圍，待使用者指示
