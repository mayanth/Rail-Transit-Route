"""ตัวอย่างการค้นหาเส้นทาง ครอบคลุม Requirements 1–10"""
BTS_FARE = "https://www.bts.co.th/routemap.html"
MRT_FARE = "https://metro.bemplc.co.th/Fare-Calculation"
ARL_FARE = "https://www.srtet.co.th/en/fare-information"
RED_FARE = "https://www.srtet.co.th/en/fare-information"
EST = "ประมาณการ ~2 นาที/สถานี + เวลารอ/เดินเปลี่ยนระบบ"

# leg: (สาย, ทิศทาง, ขึ้น, ลง, จำนวนสถานี, [ (ชื่อลิงก์ค่าโดยสาร, url) ])
ROUTES = [
 {"id": "R1", "origin": "อโศก (Asok) — BTS สายสุขุมวิท", "dest": "หมอชิต (Mo Chit) — BTS สายสุขุมวิท",
  "options": [
   {"label": "⭐ แนะนำ — เปลี่ยนน้อยที่สุด / เร็วที่สุด", "rec": True, "transfers": 0, "stations": 11, "time": "~25–30 นาที",
    "path": "อโศก → หมอชิต",
    "legs": [("BTS สายสุขุมวิท (เขียวอ่อน)", "คูคต", "อโศก", "หมอชิต", 11)],
    "transfer_notes": ["ไม่ต้องเปลี่ยนสาย / ไม่ต้องเปลี่ยนระบบ"],
    "fares": [("BTS", BTS_FARE)], "fare_note": "ระบบเดียว จ่ายครั้งเดียว"},
   {"label": "ทางเลือก — ใช้ MRT", "rec": False, "transfers": 0, "stations": 9, "time": "~30–35 นาที (รวมเดิน 2 ช่วง)",
    "path": "BTS อโศก ⇢ MRT สุขุมวิท → MRT สวนจตุจักร ⇢ BTS หมอชิต",
    "legs": [("MRT สายสีน้ำเงิน", "ลาดพร้าว / บางซื่อ (ตรวจป้ายปลายทางที่ชานชาลา)", "สุขุมวิท", "สวนจตุจักร", 9)],
    "transfer_notes": ["⚠️ เดินเชื่อม BTS อโศก → MRT สุขุมวิท ก่อนขึ้นรถ", "⚠️ ลงที่ MRT สวนจตุจักร แล้วเดินเชื่อมไปสถานี BTS หมอชิต (ไม่ต้องขึ้น BTS)"],
    "fares": [("MRT", MRT_FARE)], "fare_note": "ใช้ระบบ MRT ระบบเดียว แต่ต้องเดินเชื่อมทั้งต้นทางและปลายทาง"},
  ]},
 {"id": "R2", "origin": "พระราม 9 (Phra Ram 9) — MRT สายสีน้ำเงิน", "dest": "สยาม (Siam) — BTS สายสุขุมวิท/สีลม",
  "options": [
   {"label": "⭐ แนะนำ — เร็วที่สุด / เปลี่ยนน้อยที่สุด", "rec": True, "transfers": 1, "stations": 6, "time": "~25–30 นาที",
    "path": "พระราม 9 → สุขุมวิท ⇄ อโศก → สยาม",
    "legs": [("MRT สายสีน้ำเงิน", "สุขุมวิท / สีลม (ตรวจป้ายปลายทางที่ชานชาลา)", "พระราม 9", "สุขุมวิท", 2),
             ("BTS สายสุขุมวิท (เขียวอ่อน)", "คูคต", "อโศก", "สยาม", 4)],
    "transfer_notes": ["⚠️ เปลี่ยนระบบ MRT → BTS ที่ MRT สุขุมวิท ⇄ BTS อโศก: แตะบัตรออกจาก MRT → เดินทางเชื่อม → ซื้อตั๋ว/แตะบัตร BTS ใหม่"],
    "fares": [("MRT", MRT_FARE), ("BTS", BTS_FARE)], "fare_note": "ข้ามระบบ — ค่าโดยสารคิดแยก MRT + BTS"},
   {"label": "ทางเลือก 2 — เปลี่ยนที่สีลม", "rec": False, "transfers": 1, "stations": 8, "time": "~30–35 นาที",
    "path": "พระราม 9 → สีลม ⇄ ศาลาแดง → สยาม",
    "legs": [("MRT สายสีน้ำเงิน", "สุขุมวิท / สีลม (ตรวจป้ายปลายทางที่ชานชาลา)", "พระราม 9", "สีลม", 6),
             ("BTS สายสีลม (เขียวเข้ม)", "สนามกีฬาแห่งชาติ", "ศาลาแดง", "สยาม", 2)],
    "transfer_notes": ["⚠️ เปลี่ยนระบบ MRT → BTS ที่ MRT สีลม ⇄ BTS ศาลาแดง: แตะบัตรออก → เดินเชื่อม → แตะบัตร BTS ใหม่"],
    "fares": [("MRT", MRT_FARE), ("BTS", BTS_FARE)], "fare_note": "ข้ามระบบ — ค่าโดยสารคิดแยก MRT + BTS"},
   {"label": "ทางเลือก 3 — ผ่าน Airport Rail Link", "rec": False, "transfers": 2, "stations": 5, "time": "~30–40 นาที (เปลี่ยน 2 ครั้ง)",
    "path": "พระราม 9 → เพชรบุรี ⇄ มักกะสัน → พญาไท ⇄ พญาไท → สยาม",
    "legs": [("MRT สายสีน้ำเงิน", "สุขุมวิท / สีลม (ตรวจป้ายปลายทางที่ชานชาลา)", "พระราม 9", "เพชรบุรี", 1),
             ("Airport Rail Link", "พญาไท", "มักกะสัน", "พญาไท", 2),
             ("BTS สายสุขุมวิท (เขียวอ่อน)", "เคหะฯ", "พญาไท", "สยาม", 2)],
    "transfer_notes": ["⚠️ เปลี่ยนระบบครั้งที่ 1: MRT เพชรบุรี ⇄ ARL มักกะสัน (เดินเชื่อม + แตะบัตรใหม่)",
                       "⚠️ เปลี่ยนระบบครั้งที่ 2: ARL พญาไท ⇄ BTS พญาไท (เดินเชื่อม + แตะบัตรใหม่)"],
    "fares": [("MRT", MRT_FARE), ("ARL", ARL_FARE), ("BTS", BTS_FARE)], "fare_note": "ข้าม 3 ระบบ — ค่าโดยสารคิดแยก 3 ครั้ง (ไม่แนะนำ)"},
  ]},
 {"id": "R3", "origin": "กรุงเทพอภิวัฒน์ (Krung Thep Aphiwat) — สายสีแดงเข้ม", "dest": "ดอนเมือง (Don Mueang) — สายสีแดงเข้ม",
  "options": [
   {"label": "⭐ แนะนำ — เส้นทางเดียว ไม่ต้องเปลี่ยนสาย", "rec": True, "transfers": 0, "stations": 7, "time": "~20–25 นาที",
    "path": "กรุงเทพอภิวัฒน์ → ดอนเมือง",
    "legs": [("SRT สายสีแดงเข้ม", "รังสิต", "กรุงเทพอภิวัฒน์", "ดอนเมือง", 7)],
    "transfer_notes": ["ไม่ต้องเปลี่ยนสาย / ไม่ต้องเปลี่ยนระบบ"],
    "fares": [("SRT Red", RED_FARE)], "fare_note": "ผู้ใหญ่ 33 บาท · นักเรียน/นักศึกษา 30 บาท · ผู้สูงอายุ 17 บาท (ตารางค่าโดยสาร SRTET ตรวจ 2026-11-06 00:04 น.)",
    "fare_verified_numbers": True},
  ]},
]

REQS = [
 ("1", "รับสถานีต้นทางและปลายทาง", "หัวแต่ละตัวอย่าง R1–R3 (ต้นทาง / ปลายทาง)"),
 ("2", "ตรวจสอบเส้นทางที่เดินทางได้", "ทุกเส้นทางใช้เฉพาะสายที่เปิดให้บริการ (ส่วนที่ 1)"),
 ("3", "ระบุรถไฟฟ้าสายใด", "คอลัมน์ \"สาย\" ในตารางช่วงการเดินทาง"),
 ("4", "ระบุสถานีเปลี่ยนสาย / เปลี่ยนขบวน", "สัญลักษณ์ ⇄ ในเส้นทาง + คอลัมน์ขึ้นที่/ลงที่"),
 ("5", "ระบุจำนวนครั้งที่เปลี่ยนสาย", "คอลัมน์ \"เปลี่ยนสาย\" ในตารางเปรียบเทียบ"),
 ("6", "ระบุต้นทางและปลายทางชัดเจน", "ชื่อไทย + อังกฤษ + สาย ที่หัวตัวอย่าง"),
 ("7", "ระบุค่าโดยสารโดยประมาณ (ปัจจุบัน)", "ลิงก์ค่าโดยสารทุกช่วง · R3 มีตัวเลขจริงแยกประเภทบัตร"),
 ("8", "หลายเส้นทาง → แสดงเส้นทางที่เหมาะสม", "R1 (2 ทางเลือก), R2 (3 ทางเลือก) + ไฮไลต์ ⭐ แนะนำ"),
 ("9", "แจ้งการเดินเชื่อม / เปลี่ยนระบบ", "กล่อง ⚠️ ใต้แต่ละเส้นทาง (แตะบัตรออก / เดินเชื่อม / ค่าโดยสารแยก)"),
 ("10", "อ้างอิงข้อมูลปัจจุบัน", "ลิงก์ค่าโดยสารทางการ + เวลาที่ตรวจ · ข้อมูลที่ตรวจไม่ได้ติดสถานะชัดเจน"),
]


def routes_html(XL, badge, e):
    def link(name, u): return f'<a href="{e(u)}">{e(name)}</a>'
    out = [f"""<h2>5. ตัวอย่างการค้นหาเส้นทาง (ตาม Requirements)</h2>
<div class=sum style="background:#fff">
<b>สถานะข้อมูลในส่วนนี้</b><br>
• ค่าโดยสาร: ลิงก์หน้าค่าโดยสารทางการ {badge('verified')} · R3 มีตัวเลขจากตาราง SRTET {badge('verified')}<br>
• เส้นทาง / จำนวนสถานี: ตามผังเส้นทางของผู้ให้บริการ — ระบบเปิดผังของ BTS/MRT อัตโนมัติไม่ได้ {badge('unverifiable')} ตรวจได้ที่ {link('bts.co.th/routemap', BTS_FARE)}<br>
• เวลาเดินทาง: {e(EST)} {badge('unverifiable')}<br>
• จำนวนสถานี = จำนวนสถานีที่ผ่านจนถึงสถานีปลายทาง (ไม่นับสถานีต้นทาง) · ทิศทาง = ชื่อสถานีปลายสายบนป้าย</div>"""]
    for r in ROUTES:
        cmp_rows = ""
        for k, o in enumerate(r["options"], 1):
            cls = " class='rec'" if o["rec"] else ""
            fl = "<br>".join(link(n, u) for n, u in o["fares"])
            fb = badge('verified')
            cmp_rows += (f"<tr{cls}><td class=c>{k}</td><td>{e(o['label'])}</td><td>{e(o['path'])}</td>"
                         f"<td class=c>{o['transfers']}</td><td class=c>{o['stations']}</td><td>{fl}<br>{fb}</td><td>{e(o['time'])}</td></tr>")
        details = ""
        for k, o in enumerate(r["options"], 1):
            legs = "".join(f"<tr><td class=c>{j}</td><td>{e(l[0])}</td><td>{e(l[1])}</td><td>{e(l[2])}</td><td>{e(l[3])}</td><td class=c>{l[4]}</td></tr>"
                           for j, l in enumerate(o["legs"], 1))
            notes = "<br>".join(e(n) for n in o["transfer_notes"])
            fare_line = e(o["fare_note"])
            details += (f"<div style='break-inside:avoid;margin-top:6px'><h3 style='font-size:9.5pt;margin:0;background:{XL['group_bg']};padding:3px 8px;border:1px solid #000;border-bottom:none;{'border-left:6px solid #000;' if o['rec'] else ''}'>"
                        f"{r['id']}.{k} {e(o['label'])} — เปลี่ยนสาย {o['transfers']} ครั้ง</h3>"
                        f"<table><thead><tr><th>ช่วง</th><th>สาย</th><th>ทิศทาง (ปลายสาย)</th><th>ขึ้นที่</th><th>ลงที่</th><th>สถานี</th></tr></thead><tbody>{legs}</tbody></table>"
                        f"<div class=s style='border:1px solid #000;border-top:none;padding:4px 8px;background:#fff'><b>การเปลี่ยนสาย/ระบบ:</b> {notes}<br>"
                        f"<b>ค่าโดยสาร:</b> {fare_line} · " + " · ".join(link(n, u) for n, u in o["fares"]) +
                        " · ราคาอาจต่างตามประเภทบัตร (นักเรียน / ผู้สูงอายุ / บัตรเติมเงิน) — ตรวจที่ลิงก์</div></div>")
        out.append(f"""<div style='break-inside:avoid'><h3 style='font-size:10.5pt;margin:10px 0 0;background:{XL['progress_bg']};padding:5px 8px;border:1px solid #000;border-bottom:none'>
{r['id']} · ต้นทาง: {e(r['origin'])} &nbsp;→&nbsp; ปลายทาง: {e(r['dest'])}</h3>
<table><thead><tr><th>#</th><th>เกณฑ์</th><th>เส้นทาง</th><th>เปลี่ยนสาย</th><th>สถานี</th><th>ค่าโดยสาร</th><th>เวลา (ประมาณ)</th></tr></thead><tbody>{cmp_rows}</tbody></table></div>
{details}""")
    req = "".join(f"<tr><td class=c>{n}</td><td>{e(t)}</td><td>{e(w)}</td><td class=c>✔</td></tr>" for n, t, w in REQS)
    out.append(f"""<div style='break-inside:avoid'><h3 style='font-size:10.5pt;margin:10px 0 0;background:{XL['label_bg']};padding:5px 8px;border:1px solid #000;border-bottom:none'>ตรวจสอบความครบถ้วนตาม Requirements</h3>
<table><thead><tr><th>#</th><th>Requirement</th><th>อยู่ตรงไหนในเอกสาร</th><th>ครบ</th></tr></thead><tbody>{req}</tbody></table></div>""")
    return "\n".join(out)
