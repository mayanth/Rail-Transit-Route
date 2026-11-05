"""รายงาน Source list + ตัวอย่างเส้นทาง (ตาม Requirements 1–10)
Usage: python build_report.py rail_route_YYYY-MM-DD.pdf
แก้ข้อมูลที่ LINES / AGENCIES / UPCOMING / FARES (ไฟล์นี้) และ ROUTES (routes.py)
"""
import html, sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pdf import XL, STATUS

OUT_PDF = sys.argv[1] if len(sys.argv) > 1 else "rail_route_YYYY-MM-DD.pdf"
CHECKED = "2026-11-05 21:41"
V, U = "verified", "unverifiable"
NOTE_BTS = "ผู้ใช้ตรวจยืนยันลิงก์ด้วยตนเองเมื่อ 2026-11-06 (เว็บไซต์ปฏิเสธการตรวจอัตโนมัติ)"

LINES = [  # สาย, ปลายสาย, ผู้ให้บริการ, เว็บ, หน้าค่าโดยสาร, สถานะ, หมายเหตุ
 ("BTS สายสุขุมวิท (Sukhumvit Line) — เขียวอ่อน", "คูคต ↔ เคหะฯ", "บริษัท ระบบขนส่งมวลชนกรุงเทพ จำกัด (มหาชน) — BTSC", "https://www.bts.co.th", "https://www.bts.co.th/routemap.html", V, NOTE_BTS),
 ("BTS สายสีลม (Silom Line) — เขียวเข้ม", "สนามกีฬาแห่งชาติ ↔ บางหว้า", "BTSC", "https://www.bts.co.th", "https://www.bts.co.th/routemap.html", V, NOTE_BTS),
 ("BTS สายสีทอง (Gold Line)", "กรุงธนบุรี ↔ คลองสาน", "BTSC (เดินรถ)", "https://www.bts.co.th", "https://www.bts.co.th/routemap.html", V, NOTE_BTS),
 ("MRT สายสีน้ำเงิน (Blue Line) — สายเฉลิมรัชมงคล", "วงรอบ เตาปูน–ท่าพระ–หลักสอง", "บริษัท ทางด่วนและรถไฟฟ้ากรุงเทพ จำกัด (มหาชน) — BEM", "https://metro.bemplc.co.th", "https://metro.bemplc.co.th/Fare-Rate", V, "มีเครื่องคำนวณค่าโดยสาร: metro.bemplc.co.th/Fare-Calculation"),
 ("MRT สายสีม่วง (Purple Line) — สายฉลองรัชธรรม", "คลองบางไผ่ ↔ เตาปูน", "BEM", "https://metro.bemplc.co.th", "https://metro.bemplc.co.th/Fare-Rate", V, "ส่วนต่อขยาย เตาปูน–ราษฎร์บูรณะ อยู่ระหว่างก่อสร้าง (ตาม รฟม.)"),
 ("MRT สายสีเหลือง (Yellow Line) — สายนัคราพิพัฒน์", "ลาดพร้าว ↔ สำโรง", "EBM (Eastern Bangkok Monorail)", "https://ebm.co.th/", "https://ebm.co.th/th/routemap/", V, "ลิงก์จากเว็บไซต์ รฟม."),
 ("MRT สายสีชมพู (Pink Line) — สายวิวัฒน์นคร", "ศูนย์ราชการนนทบุรี (แคราย) ↔ มีนบุรี + ส่วนต่อขยาย ศรีรัช–เมืองทองธานี", "NBM (Northern Bangkok Monorail)", "https://www.nbm.co.th/", "https://www.nbm.co.th/th/routemap/", V, "ลิงก์จากเว็บไซต์ รฟม."),
 ("Airport Rail Link (ARL)", "พญาไท ↔ สุวรรณภูมิ", "บริษัท เอเชีย เอรา วัน จำกัด", "https://www.asiaeraone.co.th", "https://www.srtet.co.th/en/fare-information", V, "ผู้ใช้ตรวจยืนยันลิงก์ด้วยตนเองเมื่อ 2026-11-06 · ลิงก์ค่าโดยสารเป็นหน้าของ SRTET"),
 ("SRT สายสีแดงเข้ม (Dark Red Line)", "กรุงเทพอภิวัฒน์ ↔ รังสิต", "บริษัท รถไฟฟ้า ร.ฟ.ท. จำกัด — SRTET", "https://www.srtet.co.th", "https://www.srtet.co.th/th/fare-information", V, "เครื่องคำนวณ: srtet.co.th/th/fare-calculator"),
 ("SRT สายสีแดงอ่อน (Light Red Line)", "กรุงเทพอภิวัฒน์ ↔ ตลิ่งชัน", "SRTET", "https://www.srtet.co.th", "https://www.srtet.co.th/th/fare-information", V, ""),
]
AGENCIES = [
 ("การรถไฟฟ้าขนส่งมวลชนแห่งประเทศไทย (รฟม. / MRTA)", "เจ้าของโครงการ MRT, สถานะสายใหม่", "https://www.mrta.co.th", V),
 ("การรถไฟแห่งประเทศไทย (รฟท. / SRT)", "เจ้าของสายสีแดงและ ARL", "https://www.railway.co.th", V),
 ("กรมการขนส่งทางราง (ขร. / DRT)", "หน่วยงานกำกับ นโยบายค่าโดยสาร", "https://www.drt.go.th", V),
]
UPCOMING = [
 ("MRT สายสีส้ม (Orange Line)", "บางขุนนนท์ ↔ มีนบุรี (สุวินทวงศ์)", "อยู่ระหว่างก่อสร้าง", "https://www.mrta.co.th/th/orange-line"),
 ("MRT สายสีม่วง ส่วนต่อขยายใต้", "เตาปูน ↔ ราษฎร์บูรณะ", "อยู่ระหว่างก่อสร้าง", "https://www.mrta.co.th/th/mrt-chalong-ratchadham"),
 ("โครงการระบบขนส่งภูมิภาค (ภูเก็ต, โคราช, พิษณุโลก, เชียงใหม่)", "—", "อยู่ในแผน (ตาม รฟม.)", "https://www.mrta.co.th"),
]


FARE_CHECKED = "2026-11-05 21:52"
FARE_PAGE = "https://www.mrta.co.th/th/fares"
FARES = [  # สาย, ข้อบังคับ, URL เอกสาร
 ("MRT สายสีน้ำเงิน (BL)", "ข้อบังคับค่าโดยสาร พ.ศ. 2569 (ราชกิจจาฯ)", "https://www.mrta.co.th/storage/content/uploads/1782462764BL%202569%20%E0%B8%82%E0%B9%89%E0%B8%AD%E0%B8%9A%E0%B8%B1%E0%B8%87%E0%B8%84%E0%B8%B1%E0%B8%9A%20%28%E0%B8%A3%E0%B8%B2%E0%B8%8A%E0%B8%81%E0%B8%B4%E0%B8%88%E0%B8%88%E0%B8%B2%29.pdf"),
 ("MRT สายสีม่วง (PP)", "ข้อบังคับค่าโดยสาร พ.ศ. 2569 (ราชกิจจาฯ)", "https://www.mrta.co.th/storage/content/uploads/1783048822PP%202569%20%E0%B8%82%E0%B8%B1%E0%B8%AD%E0%B8%9A%E0%B8%B1%E0%B8%87%E0%B8%84%E0%B8%B1%E0%B8%9A%E0%B8%84%E0%B9%88%E0%B8%B2%E0%B9%82%E0%B8%94%E0%B8%A2%E0%B8%AA%E0%B8%B2%E0%B8%A3%20%28%E0%B8%A3%E0%B8%B2%E0%B8%8A%E0%B8%81%E0%B8%B4%E0%B8%88%E0%B8%88%E0%B8%B2%29.pdf"),
 ("MRT สายสีเหลือง (YL)", "ข้อบังคับค่าโดยสาร พ.ศ. 2566 (ราชกิจจาฯ)", "https://www.mrta.co.th/storage/content/uploads/1695002417YL%202566%20%E0%B8%82%E0%B8%B1%E0%B8%AD%E0%B8%9A%E0%B8%B1%E0%B8%87%E0%B8%84%E0%B8%B1%E0%B8%9A%E0%B8%84%E0%B9%88%E0%B8%B2%E0%B9%82%E0%B8%94%E0%B8%A2%E0%B8%AA%E0%B8%B2%E0%B8%A3%20%28%E0%B8%A3%E0%B8%B2%E0%B8%8A%E0%B8%81%E0%B8%B4%E0%B8%88%E0%B8%88%E0%B8%B2%29.pdf"),
 ("MRT สายสีชมพู (PK)", "ข้อบังคับค่าโดยสาร พ.ศ. 2566 (ราชกิจจาฯ)", "https://www.mrta.co.th/storage/content/uploads/1783048992PK%202566%20%E0%B8%82%E0%B8%B1%E0%B8%AD%E0%B8%9A%E0%B8%B1%E0%B8%87%E0%B8%84%E0%B8%B1%E0%B8%9A%E0%B8%84%E0%B9%88%E0%B8%B2%E0%B9%82%E0%B8%94%E0%B8%A2%E0%B8%AA%E0%B8%B2%E0%B8%A3%20%28%E0%B8%A3%E0%B8%B2%E0%B8%8A%E0%B8%81%E0%B8%B4%E0%B8%88%E0%B8%88%E0%B8%B2%29.pdf"),
]
TRANSFER = [("ม่วง ↔ น้ำเงิน (PL–BL)", "เตาปูน"), ("น้ำเงิน ↔ เหลือง (BL–YL)", "ลาดพร้าว"), ("ม่วง ↔ ชมพู (PL–PK)", "ศูนย์ราชการนนทบุรี")]

ARL_SRC = "https://www.siammandarinahotel.com/th/blog/airport-link-info/"
ARL_CHECKED = "2026-11-05 23:49"
ARL_SRC2 = "https://bkkairportlink.com/fare"
ARL_CHECKED2 = "2026-11-05 23:57"
ARL_FARE = [("ผู้ใหญ่ (ทั่วไป)", "15 – 45 บาท", "ตามจำนวนสถานี — ทั้ง 2 แหล่งตรงกัน"),
            ("เด็ก สูงไม่เกิน 90 ซม.", "ฟรี", "bkkairportlink.com"),
            ("เด็ก สูงเกิน 90 ซม.", "ราคาเท่าผู้ใหญ่", "bkkairportlink.com"),
            ("นักเรียน / นักศึกษา", "ลด 20% จากราคาทั่วไป", "Siam Mandarina เท่านั้น (อีกแหล่งไม่ระบุ)"),
            ("ผู้สูงอายุ", "ลด 50% จากราคาทั่วไป", "Siam Mandarina เท่านั้น (อีกแหล่งไม่ระบุ)"),
            ("ผู้พิการ", "—", "ทั้ง 2 แหล่งไม่ระบุ")]
ARL_BYSTOP = [(1, 15), (2, 20), (3, 25), (4, 30), (5, 35), (6, 40), (7, 45)]  # bkkairportlink.com
ARL_ST = ["พญาไท", "ราชปรารภ", "มักกะสัน", "รามคำแหง", "หัวหมาก", "บ้านทับช้าง", "ลาดกระบัง", "สุวรรณภูมิ"]
ARL_TIME = [("พญาไท","ราชปรารภ",1),("ราชปรารภ","มักกะสัน",3),("มักกะสัน","รามคำแหง",4),("รามคำแหง","หัวหมาก",4),
            ("หัวหมาก","บ้านทับช้าง",4),("บ้านทับช้าง","ลาดกระบัง",5),("ลาดกระบัง","สุวรรณภูมิ",5)]

from redline import red_html, RED_SRC, RED_CHECKED
from routes import routes_html, ROUTES
e = html.escape
def badge(k):
    l, fg, bg, _ = STATUS[k]
    return f'<span class="badge" style="color:{fg};background:{bg}">{l}</span>'
def a(u): return f'<a href="{e(u)}">{e(u.replace("https://",""))}</a>' if u else badge("not_found")

def pdf():
    rows = "".join(f"<tr><td class=c>{i}</td><td><b>{e(n)}</b><br><span class=s>{e(t)}</span></td><td>{e(o)}</td>"
                   f"<td><b>เว็บไซต์:</b> {a(w)}<br><b>ค่าโดยสาร:</b> {a(f)}</td><td class=c>{badge(st)}</td></tr>"
                   + (f"<tr><td></td><td colspan=4 class=s>หมายเหตุ: {e(nt)}</td></tr>" if nt else "")
                   for i, (n, t, o, w, f, st, nt) in enumerate(LINES, 1))
    ag = "".join(f"<tr><td class=c>{i}</td><td><b>{e(n)}</b></td><td>{e(r)}</td><td>{a(u)}</td><td class=c>{badge(s)}</td></tr>"
                 for i, (n, r, u, s) in enumerate(AGENCIES, 1))
    up = "".join(f"<tr><td class=c>{i}</td><td><b>{e(n)}</b></td><td>{e(t)}</td><td class=c>{badge('no_service')}<br><span class=s>{e(s)}</span></td><td>{a(u)}</td></tr>"
                 for i, (n, t, s, u) in enumerate(UPCOMING, 1))
    fr = "".join(f"<tr><td class=c>{i}</td><td><b>{e(n)}</b></td><td class=c><a href=\"https://metro.bemplc.co.th/Fare-Calculation\">metro.bemplc.co.th/Fare-Calculation</a></td><td>{e(d)}<br><a href=\"{u}\">เปิดเอกสารข้อบังคับ (PDF)</a></td></tr>" for i,(n,d,u) in enumerate(FARES,1))
    tr = "".join(f"<tr><td class=c>{i}</td><td><b>{e(n)}</b></td><td>{e(st)}</td><td class=c>{badge('unverifiable')}</td></tr>" for i,(n,st) in enumerate(TRANSFER,1))
    arf = "".join(f"<tr><td class=c>{i}</td><td><b>{e(a_)}</b></td><td class=c><b>{e(b_)}</b><br>{badge('unverifiable')}</td><td class=s>{e(c_)}</td></tr>" for i,(a_,b_,c_) in enumerate(ARL_FARE,1))
    fare_of = dict(ARL_BYSTOP)
    bys = "".join(f"<td class=c>{n}</td>" for n, _ in ARL_BYSTOP)
    byf = "".join(f"<td class=c><b>{f}</b></td>" for _, f in ARL_BYSTOP)
    mx = "<tr><th></th>" + "".join(f"<th style='font-size:7.5pt'>{s_}</th>" for s_ in ARL_ST) + "</tr>"
    for i, a1 in enumerate(ARL_ST):
        mx += f"<tr><th style='font-size:7.5pt;text-align:left'>{a1}</th>" + "".join(
            f"<td class=c style='background:{'#fff' if i == j else XL['row_bg']}'>{15 if i == j else fare_of[abs(i - j)]}</td>"
            for j in range(len(ARL_ST))) + "</tr>"
    art = "".join(f"<tr><td>{e(x)} → {e(y)}</td><td class=c>{m} นาที</td></tr>" for x,y,m in ARL_TIME)
    art += f"<tr><td><b>รวม พญาไท → สุวรรณภูมิ (ไม่รวมเวลาจอด)</b></td><td class=c><b>{sum(m for *_,m in ARL_TIME)} นาที</b></td></tr>"
    red = red_html(XL, badge, e)
    nv = sum(1 for x in LINES if x[5] == V); nu = len(LINES) - nv
    ops = len({x[3] for x in LINES})
    rt = routes_html(XL, badge, e)
    nf = sum(1 for x in LINES if x[4])
    by_op = {}
    for x in LINES: by_op.setdefault(x[3], []).append(x[0].split(" —")[0].split(" (")[0])
    oprow = "".join(f"<tr><td><a href='{e(w)}'>{e(w.replace('https://',''))}</a></td><td>{e(', '.join(v))}</td><td class=c>{len(v)}</td></tr>" for w, v in by_op.items())
    final = f"""<h2>6. สรุปผลภาพรวม (Overall Summary)</h2>
<table><thead><tr><th style="width:34%">หัวข้อ</th><th>ผลลัพธ์</th><th style="width:16%">สถานะ</th></tr></thead><tbody>
<tr><td><b>1. สายที่เปิดให้บริการ</b></td><td>{len(LINES)} สาย จาก {ops} เว็บไซต์ผู้ให้บริการ (BTS 3 · MRT 4 · ARL 1 · สายสีแดง 2)</td><td class=c>{badge(V)}<br>{nv}/{len(LINES)}</td></tr>
<tr><td><b>ลิงก์เว็บไซต์ผู้ให้บริการ</b></td><td>ครบ {len(LINES)}/{len(LINES)} สาย · ระบบตรวจเอง 6 สาย · ผู้ใช้ยืนยันด้วยตนเอง 4 สาย (BTS 3, ARL)</td><td class=c>{badge(V)}</td></tr>
<tr><td><b>ลิงก์หน้าค่าโดยสาร</b></td><td>ครบ {nf}/{len(LINES)} สาย · ARL ใช้ลิงก์หน้าของ SRTET</td><td class=c>{badge(V)}</td></tr>
<tr><td><b>2. ตัวเลขอัตราค่าโดยสาร (รฟม.)</b></td><td>ยังไม่มีตัวเลข — มีลิงก์ข้อบังคับค่าโดยสาร {len(FARES)} สาย และส่วนลดเปลี่ยนถ่าย {len(TRANSFER)} คู่ แต่ตัวเลขอยู่ในรูปภาพ/PDF ที่ระบบอ่านไม่ได้</td><td class=c>{badge(U)}</td></tr>
<tr><td><b>3. หน่วยงานรัฐที่เกี่ยวข้อง</b></td><td>{len(AGENCIES)} หน่วยงาน (รฟม., รฟท., ขร.)</td><td class=c>{badge(V)}</td></tr>
<tr><td><b>4. สายที่ยังไม่เปิดให้บริการ</b></td><td>{len(UPCOMING)} รายการ (สายสีส้ม, ส่วนต่อขยายสายสีม่วงใต้, โครงการภูมิภาค)</td><td class=c>{badge('no_service')}</td></tr>
<tr><td><b>5. ตัวอย่างการค้นหาเส้นทาง</b></td><td>{len(ROUTES)} เส้นทาง / {sum(len(r["options"]) for r in ROUTES)} ทางเลือก — ไม่เปลี่ยนสาย (R1, R3), ข้ามระบบ MRT↔BTS (R2), เปลี่ยน 2 ครั้งผ่าน ARL (R2.3) · ครบ Requirements 10/10 · ค่าโดยสาร: ลิงก์ทางการทุกช่วง, R3 มีตัวเลขจริง</td><td class=c>{badge(V)}<br><span class=s>เวลา/จำนวนสถานี: {badge(U)}</span></td></tr>
</tbody></table>
<table style="margin-top:6px"><thead><tr><th>เว็บไซต์ผู้ให้บริการ</th><th>สายที่ดูแล</th><th>จำนวนสาย</th></tr></thead><tbody>{oprow}</tbody></table>
<div class=sum style="margin-top:6px"><b>ข้อสรุป</b><br>
• เอกสารนี้พร้อมใช้เป็น <b>รายการแหล่งข้อมูล (Source list)</b> ของ Rail Route Agent — ลิงก์ผู้ให้บริการและหน้าค่าโดยสารครบทุกสาย<br>
• <b>ยังใช้ตอบค่าโดยสารเป็นตัวเลขไม่ได้</b> — ต้องเปิดหน้าค่าโดยสารของแต่ละสายและตรวจซ้ำทุกครั้ง ตามกฎ "ห้ามเดาข้อมูล"<br>
• <b>สิ่งที่ควรทำต่อ:</b> ① เติมตัวเลขค่าโดยสาร MRT จากข้อบังคับ รฟม. ② หาหน้าค่าโดยสาร ARL ของผู้ให้บริการโดยตรง แทนหน้าของ SRTET ③ ตรวจสถานะและลิงก์ซ้ำทุก 30 วัน</div>"""
    doc = f"""<!doctype html><html lang=th><head><meta charset=utf-8><style>
@page{{size:A4;margin:16mm 14mm 18mm}}
body{{font-family:'Montserrat','Noto Sans Thai','Loma',sans-serif;font-size:9.5pt;color:#000}}
h1{{font-size:15pt;margin:0 0 6px}}
h2{{font-size:10.5pt;margin:14px 0 0;background:{XL['label_bg']};padding:4px 8px;border:1px solid #000;border-bottom:none}}
table{{width:100%;border-collapse:collapse}} thead{{display:table-header-group}} tr{{break-inside:avoid}}
th{{background:#000;color:#fff;padding:5px;border:1px solid #000}}
td{{border:1px solid #000;padding:5px;vertical-align:top;background:{XL['row_bg']}}}
.meta td{{background:#fff}} .meta td.k{{background:{XL['label_bg']};font-weight:700;width:18%}}
.sum{{border:1px solid #000;padding:7px 9px;background:{XL['progress_bg']}}}
.c{{text-align:center}} .s{{font-size:7.8pt;color:#333}}
.badge{{display:inline-block;padding:1px 5px;border:1px solid currentColor;font-size:7.8pt;font-weight:700;white-space:nowrap}}
a{{color:#0563C1;word-break:break-all}}
</style></head><body>
<div style='border:1px solid #000;padding:8px 10px'><h1>รายชื่อผู้ให้บริการรถไฟฟ้าในประเทศไทย และลิงก์เว็บไซต์ทางการ</h1>
<table class=meta><tr><td class=k>โจทย์</td><td>ระบบค้นหาเส้นทางเดินทางด้วยรถไฟฟ้า (Source list)</td><td class=k>Input</td><td>ลิงก์บริษัทรถไฟฟ้าในประเทศไทย</td></tr>
<tr><td class=k>วันที่</td><td>2026-11-05</td><td class=k>เวลาที่ตรวจสอบ</td><td>{CHECKED} น. (UTC+7)</td></tr></table></div>
<h2>สรุปผล (Summary)</h2><div class=sum>สายที่เปิดให้บริการ {len(LINES)} สาย จากผู้ให้บริการ {ops} เว็บไซต์ · {badge(V)} {nv} สาย (BTS 3 สาย และ ARL ผู้ใช้ตรวจยืนยันด้วยตนเองเมื่อ 2026-11-06) · ทุกลิงก์ในเอกสารกดได้</div>
<h2>สถานะข้อมูล (Data Progress)</h2>
<table><thead><tr><th style="background:{XL['progress_bg']};color:#000">Total</th>{''.join(f"<th style='background:{XL['progress_bg']};color:#000'>{STATUS[k][0]}</th>" for k in STATUS)}<th style="background:{XL['progress_bg']};color:#000">ยืนยันแล้ว (%)</th></tr></thead>
<tbody><tr><td class=c style="background:#fff">{len(LINES)}</td>{''.join(f"<td class=c style='background:#fff'>{sum(1 for x in LINES if x[5]==k)}</td>" for k in STATUS)}<td class=c style="background:#fff"><b>{nv*100//len(LINES)}%</b></td></tr></tbody></table>
<p class=s>สถานะข้อมูล: {' '.join(badge(k) for k in STATUS)}</p>
<h2>1. สายที่เปิดให้บริการ</h2>
<table><thead><tr><th>#</th><th>สาย / ปลายสาย</th><th>ผู้ให้บริการ</th><th>ลิงก์</th><th>สถานะลิงก์</th></tr></thead><tbody>{rows}</tbody></table>
<h2>2. อัตราค่าโดยสาร (ตามเว็บไซต์ รฟม.)</h2>
<div class=sum style="background:#fff">แหล่งข้อมูล: <a href="{FARE_PAGE}">{FARE_PAGE}</a> — ตรวจเมื่อ {FARE_CHECKED} น. (UTC+7)<br>
{badge('unverifiable')} <b>ยังไม่ใส่ตัวเลขค่าโดยสาร</b> — หน้าเว็บ รฟม. แสดงตารางค่าโดยสารเป็น <u>รูปภาพ</u> และ <u>ไฟล์ PDF ข้อบังคับ</u> ซึ่งเว็บไซต์ไม่อนุญาตให้ระบบอ่านอัตโนมัติ (robots) จึงอ่านตัวเลขไม่ได้ ตามกฎ "ห้ามเดาข้อมูล" จึงไม่ใส่ตัวเลขจากความจำ · กดลิงก์ด้านล่างเพื่อเปิดอัตราทางการ หรือใช้ <a href="https://metro.bemplc.co.th/Fare-Calculation">เครื่องคำนวณค่าโดยสาร BEM</a></div>
<table><thead><tr><th>#</th><th>สาย</th><th>อัตราค่าโดยสาร (บาท)</th><th>เอกสารทางการ (กดได้)</th></tr></thead><tbody>{fr}</tbody></table>
<p class=s><b>ส่วนลดการเปลี่ยนถ่ายระบบ</b> (มีตารางบนหน้า รฟม. เป็นรูปภาพ — อ่านไม่ได้)</p>
<table><thead><tr><th>#</th><th>คู่สาย</th><th>สถานีเปลี่ยนถ่าย</th><th>ส่วนลด</th></tr></thead><tbody>{tr}</tbody></table>
<h2>3. หน่วยงานรัฐที่เกี่ยวข้อง</h2>
<table><thead><tr><th>#</th><th>หน่วยงาน</th><th>บทบาท</th><th>เว็บไซต์</th><th>สถานะลิงก์</th></tr></thead><tbody>{ag}</tbody></table>
<h2>4. สายที่ยังไม่เปิดให้บริการ</h2>
<table><thead><tr><th>#</th><th>สาย</th><th>ช่วง</th><th>สถานะ</th><th>ข้อมูลโครงการ</th></tr></thead><tbody>{up}</tbody></table>
{rt}
{final}
<h2>หมายเหตุและแหล่งที่มา</h2><div class=sum style="background:#fff">
• "ยืนยันแล้ว" = ระบบเปิดหน้าเว็บได้และหน้าเว็บระบุว่าเป็นของผู้ให้บริการสายนั้น ณ {CHECKED} น.<br>
• "ยืนยันแล้ว" ของ BTS 3 สาย และ ARL = ผู้ใช้ตรวจยืนยันด้วยตนเองเมื่อ 2026-11-06 (เว็บไซต์ไม่อนุญาตให้ระบบตรวจอัตโนมัติ)<br>• "ไม่สามารถยืนยันได้" ในส่วนที่ 2 = ตัวเลขค่าโดยสารอยู่ในรูปภาพ/PDF ที่ระบบอ่านไม่ได้<br>
• ลิงก์ EBM / NBM อ้างอิงจากหน้าแรก <a href="https://www.mrta.co.th/th/">mrta.co.th</a> · ลิงก์ รฟท./ขร. อ้างอิงจาก <a href="https://www.drt.go.th">drt.go.th</a> และ <a href="https://www.srtet.co.th">srtet.co.th</a><br>
• อัตราค่าโดยสาร: <a href="https://www.mrta.co.th/th/fares">mrta.co.th/th/fares</a> (ตรวจ {FARE_CHECKED} น.) — ตัวเลขอยู่ในรูปภาพ/PDF ที่อ่านอัตโนมัติไม่ได้</div>
</body></html>"""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); pg.set_content(doc)
        pg.pdf(path=OUT_PDF, format="A4", 
               print_background=True, display_header_footer=True, header_template="<div></div>",
               footer_template='<div style="font-size:8pt;width:100%;text-align:center">หน้า <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
               margin={"top": "16mm", "bottom": "18mm", "left": "14mm", "right": "14mm"})
        b.close()

def xlsx():
    from openpyxl import Workbook
    from openpyxl.styles import PatternFill, Font, Border, Side, Alignment
    F = lambda c: PatternFill("solid", fgColor=c.lstrip("#"))
    thin = Side(style="thin"); B = Border(thin, thin, thin, thin)
    wb = Workbook(); ws = wb.active; ws.title = "Rail Operators"
    ws["A1"] = "รายชื่อผู้ให้บริการรถไฟฟ้าในประเทศไทย และลิงก์เว็บไซต์ทางการ"; ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = "ตรวจสอบเมื่อ"; ws["B2"] = f"{CHECKED} น. (UTC+7)"
    ws["A2"].fill = F(XL["label_bg"]); ws["A2"].font = Font(bold=True)
    hdr = ["#", "สาย", "ปลายสาย", "ผู้ให้บริการ", "เว็บไซต์", "หน้าค่าโดยสาร", "สถานะลิงก์", "หมายเหตุ"]
    for c, h in enumerate(hdr, 1):
        x = ws.cell(4, c, h); x.fill = F("#000000"); x.font = Font(bold=True, color="FFFFFF"); x.border = B; x.alignment = Alignment(horizontal="center")
    for i, (n, t, o, w, f, st, nt) in enumerate(LINES, 1):
        r = 4 + i
        for c, v in enumerate([i, n, t, o, w, f or "ไม่พบข้อมูล", STATUS[st][0], nt], 1):
            x = ws.cell(r, c, v); x.fill = F(XL["row_bg"]); x.border = B; x.alignment = Alignment(wrap_text=True, vertical="top")
        for c, u in ((5, w), (6, f)):
            if u: ws.cell(r, c).hyperlink = u; ws.cell(r, c).font = Font(color="0563C1", underline="single")
        s = ws.cell(r, 7); s.fill = F(STATUS[st][2]); s.font = Font(bold=True, color=STATUS[st][1].lstrip("#"))
    for col, wdt in zip("ABCDEFGH", [5, 40, 32, 38, 30, 38, 18, 50]): ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A5"
    wb.save(OUT_PDF.replace(".pdf", ".xlsx"))

pdf(); print("ok")
