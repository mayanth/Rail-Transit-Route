#!/usr/bin/env python3
"""สร้างรายงาน PDF เส้นทางรถไฟฟ้าจากไฟล์ JSON

Usage:
    python build_pdf.py route.json [--out rail_route_YYYY-MM-DD.pdf]

ต้องมี: pip install playwright && playwright install chromium
(Chromium จัดการสระ/วรรณยุกต์ไทยถูกต้อง และฝังลิงก์ที่กดได้)

JSON schema:
{
  "title": "ระบบค้นหาเส้นทางเดินทางด้วยรถไฟฟ้า",
  "origin": "อโศก (Asok)", "destination": "หมอชิต (Mo Chit)",
  "checked_at": "2026-11-05 14:30",
  "summary": "ข้อความสรุป 1-3 บรรทัด",
  "routes": [
    {"label": "เร็วที่สุด / เปลี่ยนน้อยที่สุด", "recommended": true,
     "path": "อโศก → หมอชิต", "transfers": 0, "stations": "10",
     "fare": "XX บาท", "fare_status": "verified", "time": "~20 นาที",
     "legs": [{"line": "BTS สายสุขุมวิท", "direction": "คูคต",
               "board": "อโศก", "alight": "หมอชิต", "stations": "10",
               "transfer_note": ""}],
     "card_note": "ราคาเที่ยวเดียวผู้ใหญ่ ..."}
  ],
  "notes": ["..."],
  "sources": [{"name": "BTS — Fare", "url": "https://...", "checked_at": "...", "level": 1}]
}
fare_status: verified | unverifiable | not_found | no_service
"""
import argparse, datetime, html, json, sys
from pathlib import Path

# ---- สีตาม "Template excel.xlsx" ของทีม -------------------------------------
# โครงตาราง (ดึงจากไฟล์ Template โดยตรง)
XL = {
    "header_bg": "#000000", "header_fg": "#FFFFFF",  # แถวหัวตาราง (A5:AF5) ดำ/ตัวขาวหนา
    "progress_bg": "#FFF2CC",                         # กล่อง Test Progress (L1:V2)
    "label_bg": "#CCCCCC",                            # ป้ายหัวข้อ REF DOCUMENT / TEST RESULT (A2:A4)
    "group_bg": "#A6C9EB",                            # แถวกลุ่ม/หัวข้อย่อย (แถว 7)
    "row_bg": "#FCFBD4",                              # แถวข้อมูล (แถว 8+)
    "border": "#000000",                              # เส้นขอบ thin
}
# สีสถานะ: Template ไม่มี Conditional Formatting สำหรับสถานะ จึงใช้ Cell Styles มาตรฐานของ Excel
# (Good / Neutral / Bad) + เทาสำหรับไม่พบข้อมูล  — แก้ที่นี่ถ้าทีมกำหนดรหัสสีเอง
STATUS = {  # key: (label, fg, bg, คู่สถานะใน Template)
    "verified":     ("ยืนยันแล้ว",          "#006100", "#C6EFCE", "PASSED"),
    "unverifiable": ("ไม่สามารถยืนยันได้",   "#9C5700", "#FFEB9C", "Need confirmation"),
    "not_found":    ("ไม่พบข้อมูล",          "#404040", "#D9D9D9", "SKIPPED"),
    "no_service":   ("ไม่มีบริการ",          "#9C0006", "#FFC7CE", "BLOCKED"),
}
e = lambda s: html.escape(str(s if s is not None else "-"))


def badge(key):
    label, fg, bg, _ = STATUS.get(key, STATUS["not_found"])
    return f'<span class="badge" style="color:{fg};background:{bg}">{label}</span>'


def render(d):
    routes_rows, legs_html = [], []
    for i, r in enumerate(d.get("routes", []), 1):
        cls = ' class="rec"' if r.get("recommended") else ""
        star = "⭐ แนะนำ<br>" if r.get("recommended") else ""
        routes_rows.append(
            f"<tr{cls}><td>{i}</td><td>{star}{e(r.get('label'))}</td><td>{e(r.get('path'))}</td>"
            f"<td class='c'>{e(r.get('transfers'))}</td><td class='c'>{e(r.get('stations'))}</td>"
            f"<td>{e(r.get('fare'))}<br>{badge(r.get('fare_status'))}</td><td>{e(r.get('time'))}</td></tr>")
        rows = "".join(
            f"<tr><td>{j}</td><td>{e(l.get('line'))}</td><td>{e(l.get('direction'))}</td>"
            f"<td>{e(l.get('board'))}</td><td>{e(l.get('alight'))}</td><td class='c'>{e(l.get('stations'))}</td>"
            f"<td>{e(l.get('transfer_note') or '-')}</td></tr>"
            for j, l in enumerate(r.get("legs", []), 1))
        legs_html.append(
            f"<div class='leg{' recbox' if r.get('recommended') else ''}'><h3>เส้นทางที่ {i}: {e(r.get('label'))}</h3>"
            f"<table><thead><tr><th>ช่วง</th><th>สาย</th><th>ทิศทาง (ปลายสาย)</th><th>ขึ้นที่</th>"
            f"<th>ลงที่</th><th>สถานี</th><th>การเปลี่ยนสาย / ระบบ</th></tr></thead><tbody>{rows}</tbody></table>"
            f"<p class='small'>หมายเหตุบัตร: {e(r.get('card_note'))}</p></div>")
    src = "".join(
        f"<tr><td>{i}</td><td><a href='{e(s.get('url'))}'>{e(s.get('name'))}</a><br>"
        f"<span class='small'>{e(s.get('url'))}</span></td><td>{e(s.get('checked_at'))}</td>"
        f"<td class='c'>{e(s.get('level'))}</td></tr>"
        for i, s in enumerate(d.get("sources", []), 1))
    notes = "".join(f"<li>{e(n)}</li>" for n in d.get("notes", []))
    legend = " ".join(badge(k) for k in STATUS)
    # กล่องสรุปสถานะ แบบเดียวกับ "Test Progress" ใน Template (Total + นับตามสถานะ + %)
    rs = d.get("routes", [])
    cnt = {k: sum(1 for r in rs if r.get("fare_status") == k) for k in STATUS}
    pct = f"{cnt['verified'] / len(rs) * 100:.0f}%" if rs else "-"
    progress = ("<table class='progress'><thead><tr><th>Total</th>"
                + "".join(f"<th>{STATUS[k][0]}</th>" for k in STATUS)
                + "<th>ยืนยันแล้ว (%)</th></tr></thead><tbody><tr>"
                f"<td class='c'>{len(rs)}</td>"
                + "".join(f"<td class='c'>{cnt[k]}</td>" for k in STATUS)
                + f"<td class='c'><b>{pct}</b></td></tr></tbody></table>")
    return f"""<!doctype html><html lang="th"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;700&display=swap" rel="stylesheet">
<style>
@page {{ size: A4; margin: 16mm 14mm 18mm; }}
body {{ font-family: 'Montserrat','Noto Sans Thai','Sarabun','Loma','Tahoma',sans-serif; font-size: 10pt; color:#000; }}
h1 {{ font-size: 16pt; margin:0 0 6px; }}
h2 {{ font-size:11pt; margin:16px 0 4px; background:{XL['label_bg']}; padding:4px 8px; border:1px solid {XL['border']}; }}
h3 {{ font-size:10.5pt; margin:0; background:{XL['group_bg']}; padding:4px 8px; border:1px solid {XL['border']}; border-bottom:none; }}
.head {{ border:1px solid {XL['border']}; padding:8px 10px; }}
.meta td {{ border:1px solid {XL['border']}; background:#fff; padding:4px 8px; }}
.meta td.k {{ background:{XL['label_bg']}; font-weight:700; width:22%; }}
table {{ width:100%; border-collapse:collapse; margin:0 0 4px; }}
th {{ background:{XL['header_bg']}; color:{XL['header_fg']}; text-align:center; padding:5px; font-weight:700; border:1px solid {XL['border']}; }}
td {{ border:1px solid {XL['border']}; padding:5px; vertical-align:top; background:{XL['row_bg']}; }}
thead {{ display: table-header-group; }} tr {{ break-inside: avoid; page-break-inside: avoid; }}
tr.rec td {{ background:{XL['group_bg']}; font-weight:700; }}
.progress th {{ background:{XL['progress_bg']}; color:#000; }} .progress td {{ background:#fff; }}
.c {{ text-align:center; }} .small {{ font-size:8pt; color:#404040; word-break:break-all; }}
.badge {{ display:inline-block; padding:1px 6px; border:1px solid currentColor; font-size:8pt; font-weight:700; }}
.summary {{ border:1px solid {XL['border']}; border-top:none; padding:8px 10px; background:{XL['progress_bg']}; }}
.leg {{ break-inside: avoid; margin:8px 0; }}
.recbox h3 {{ border-left:6px solid #000; }}
a {{ color:#0563C1; }}
</style></head><body>
<div class="head"><h1>{e(d.get('title','ระบบค้นหาเส้นทางเดินทางด้วยรถไฟฟ้า'))}</h1>
<table class="meta"><tr><td class="k">ต้นทาง (Origin)</td><td>{e(d.get('origin'))}</td><td class="k">ปลายทาง (Destination)</td><td>{e(d.get('destination'))}</td></tr>
<tr><td class="k">วันที่รายงาน</td><td>{e(d.get('report_date'))}</td><td class="k">เวลาที่ตรวจสอบ</td><td>{e(d.get('checked_at'))} น. (UTC+7)</td></tr></table></div>
<h2>สรุปผล (Summary)</h2><div class="summary">{e(d.get('summary'))}</div>
<h2>สถานะข้อมูล (Data Progress)</h2>{progress}
<h2>เปรียบเทียบเส้นทาง</h2>
<table><thead><tr><th>#</th><th>เกณฑ์</th><th>เส้นทาง</th><th>เปลี่ยนสาย</th><th>สถานี</th><th>ค่าโดยสาร</th><th>เวลา</th></tr></thead>
<tbody>{''.join(routes_rows)}</tbody></table>
<p class="small">สถานะข้อมูล: {legend}</p>
<h2>รายละเอียดแต่ละเส้นทาง</h2>{''.join(legs_html)}
{f'<h2>หมายเหตุ</h2><ul>{notes}</ul>' if notes else ''}
<h2>แหล่งที่มา (Sources)</h2>
<table><thead><tr><th>#</th><th>แหล่งข้อมูล</th><th>ตรวจเมื่อ</th><th>ระดับ</th></tr></thead><tbody>{src}</tbody></table>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_file")
    ap.add_argument("--out")
    a = ap.parse_args()
    d = json.loads(Path(a.json_file).read_text(encoding="utf-8"))
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).date().isoformat()
    d.setdefault("report_date", today)
    out = Path(a.out or f"rail_route_{d['report_date']}.pdf")
    from playwright.sync_api import sync_playwright
    footer = ('<div style="font-size:8pt;width:100%;text-align:center;color:#6b7280;">'
              'หน้า <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.set_content(render(d), wait_until="networkidle", timeout=30000)
        pg.pdf(path=str(out), format="A4", print_background=True, display_header_footer=True,
               header_template="<div></div>", footer_template=footer,
               margin={"top": "16mm", "bottom": "18mm", "left": "14mm", "right": "14mm"})
        b.close()
    print(f"saved: {out}")


if __name__ == "__main__":
    sys.exit(main())
