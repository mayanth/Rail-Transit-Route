RED_SRC = "https://www.srtet.co.th/en/fare-information"
RED_CHECKED = "2026-11-06 00:04"
RED_ST = ["ตลิ่งชัน", "บางบำหรุ", "บางซ่อน", "กรุงเทพอภิวัฒน์", "จตุจักร", "วัดเสมียนนารี", "บางเขน",
          "ทุ่งสองห้อง", "หลักสี่", "การเคหะฯ", "ดอนเมือง", "หลักหก", "รังสิต"]
_A = """12 18 29 35 38 41 42 42 42 42 42 42 42
18 12 23 29 32 35 37 39 42 42 42 42 42
29 23 12 18 22 25 26 29 33 36 39 42 42
35 29 18 12 16 19 20 23 27 30 33 42 42
38 32 22 16 12 15 17 19 23 26 29 38 42
41 35 25 19 15 12 14 16 20 23 26 35 40
42 37 26 20 17 14 12 14 19 22 25 34 38
42 39 29 23 19 16 14 12 17 20 23 32 36
42 42 33 27 23 20 19 17 12 15 18 27 32
42 42 36 30 26 23 22 20 15 12 15 24 29
42 42 39 33 29 26 25 23 18 15 12 21 26
42 42 42 42 38 35 34 32 27 24 21 12 17
42 42 42 42 42 40 38 36 32 29 26 17 12"""
_S = """11 16 26 31 34 37 38 38 38 38 38 38 38
16 11 20 26 29 32 33 35 38 38 38 38 38
26 20 11 16 20 22 24 26 30 32 35 38 38
31 26 16 11 14 17 18 20 24 27 30 38 38
34 29 20 14 11 14 15 17 21 24 26 34 38
37 32 22 17 14 11 12 14 18 21 24 32 36
38 33 24 18 15 12 11 13 17 20 22 30 34
38 35 26 20 17 14 13 11 15 18 20 28 32
38 38 30 24 21 18 17 15 11 14 16 24 28
38 38 32 27 24 21 20 18 14 11 14 22 26
38 38 35 30 26 24 22 20 16 14 11 19 23
38 38 38 38 34 32 30 28 24 22 19 11 15
38 38 38 38 38 36 34 32 28 26 23 15 11"""
_E = """6 9 14 17 19 21 21 21 21 21 21 21 21
9 6 11 14 16 18 18 20 21 21 21 21 21
14 11 6 9 11 12 13 14 17 18 20 21 21
17 14 9 6 8 9 10 11 14 15 17 21 21
19 16 11 8 6 8 8 9 12 13 15 19 21
21 18 12 9 8 6 7 8 10 12 13 18 20
21 18 13 10 8 7 6 7 9 11 12 17 19
21 20 14 11 9 8 7 6 8 10 11 16 18
21 21 17 14 12 10 9 8 6 8 9 14 16
21 21 18 15 13 12 11 10 8 6 8 12 14
21 21 20 17 15 13 12 11 9 8 6 11 13
21 21 21 21 19 18 17 16 14 12 11 6 8
21 21 21 21 21 20 19 18 16 14 13 8 6"""
M = lambda t: [list(map(int, r.split())) for r in t.splitlines()]
RED_TABLES = [("ผู้ใหญ่ (Adult)", M(_A)), ("นักเรียน / นักศึกษา (Student)", M(_S)), ("ผู้สูงอายุ (Senior)", M(_E))]
for _, m in RED_TABLES:  # sanity: 13x13 and symmetric
    assert len(m) == 13 and all(len(r) == 13 for r in m)
    assert all(m[i][j] == m[j][i] for i in range(13) for j in range(13)), _


def red_html(XL, badge, e):
    head = "<tr><th style='font-size:6.5pt'>ต้นทาง \\ ปลายทาง</th>" + "".join(
        f"<th style='font-size:6.5pt;padding:3px 1px'>{s}</th>" for s in RED_ST) + "</tr>"
    out = []
    for title, m in RED_TABLES:
        rows = "".join(
            f"<tr><th style='font-size:6.5pt;text-align:left;padding:3px'>{RED_ST[i]}</th>" + "".join(
                f"<td class=c style='font-size:7.5pt;padding:3px 1px;background:{'#fff' if i == j else XL['row_bg']}'>{v}</td>"
                for j, v in enumerate(r)) + "</tr>" for i, r in enumerate(m))
        lo = min(min(r) for r in m); hi = max(max(r) for r in m)
        out.append(f"<div style='break-inside:avoid;margin-top:8px'><h3 style='font-size:10pt;margin:0;background:{XL['group_bg']};padding:4px 8px;border:1px solid #000;border-bottom:none'>"
                   f"{e(title)} — {lo}–{hi} บาท {badge('verified')}</h3><table><thead>{head}</thead><tbody>{rows}</tbody></table></div>")
    adult, stu, sen = (RED_TABLES[k][1] for k in range(3))
    summ = (f"<table><thead><tr><th>ประเภทผู้โดยสาร</th><th>ต่ำสุด</th><th>สูงสุด</th><th>กรุงเทพอภิวัฒน์ → รังสิต</th><th>กรุงเทพอภิวัฒน์ → ตลิ่งชัน</th><th>สถานะ</th></tr></thead><tbody>"
            + "".join(f"<tr><td><b>{e(t)}</b></td><td class=c>{min(min(r) for r in m)}</td><td class=c>{max(max(r) for r in m)}</td>"
                      f"<td class=c>{m[3][12]}</td><td class=c>{m[3][0]}</td><td class=c>{badge('verified')}</td></tr>" for t, m in RED_TABLES)
            + "</tbody></table>")
    return f"""<h2>3. อัตราค่าโดยสาร รถไฟฟ้าสายสีแดง (SRT Red Line)</h2>
<div class=sum style="background:#fff">แหล่งข้อมูล: <a href="{RED_SRC}">SRTET — Fare Information</a> (เว็บไซต์ทางการของ บจก. รถไฟฟ้า ร.ฟ.ท. — แหล่งระดับ 1) — ตรวจเมื่อ {RED_CHECKED} น. (UTC+7)<br>
{badge('verified')} ตัวเลขทั้งหมดเป็นข้อความในตาราง HTML (ไม่ใช่รูปภาพ) คัดลอกตรงตามหน้าเว็บ · ตรวจแล้วตารางสมมาตร (A→B = B→A) ทั้ง 3 ตาราง · หน่วย: บาท ต่อเที่ยว<br>
<b>หมายเหตุ:</b> หน้านี้เป็นค่าโดยสาร <u>สายสีแดง</u> เท่านั้น ไม่ใช่ Airport Rail Link · หน้าเว็บไม่ระบุค่าโดยสารเด็ก ผู้พิการ พระภิกษุ และไม่ได้กล่าวถึงนโยบาย 20 บาท</div>
{summ}
<p class=s>แถว = สถานีต้นทาง, คอลัมน์ = สถานีปลายทาง · สายสีแดงอ่อน: ตลิ่งชัน–บางบำหรุ–บางซ่อน–กรุงเทพอภิวัฒน์ · สายสีแดงเข้ม: กรุงเทพอภิวัฒน์–…–รังสิต</p>
{''.join(out)}"""
