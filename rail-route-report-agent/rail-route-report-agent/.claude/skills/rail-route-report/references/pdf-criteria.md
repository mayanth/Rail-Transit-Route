# เกณฑ์ไฟล์ PDF (Checklist ก่อนส่ง)

| # | เกณฑ์ | วิธีที่ `build_pdf.py` จัดการ | ตรวจด้วยตา |
|---|---|---|---|
| 1 | หัวรายงาน: ชื่อโจทย์, Input ที่ค้นหา, วันที่, เวลาที่ตรวจสอบ | Header block จาก `title`, `origin`, `destination`, `checked_at` | ☐ |
| 2 | ไทย + อังกฤษ ครบ ไม่มีตัวหายหรือกล่องสี่เหลี่ยม | เรนเดอร์ด้วย Chromium + ฟอนต์ไทย (Noto Sans Thai → Sarabun → Loma) | ☐ วรรณยุกต์/สระลอยถูกตำแหน่ง |
| 3 | ตารางมีหัวตาราง ไม่ถูกตัดกลางแถว | `thead` ซ้ำทุกหน้า + `tr { break-inside: avoid }` | ☐ |
| 4 | สถานะใช้สีแยกเหมือนเกณฑ์ Excel + ไฮไลต์ผลที่แนะนำ | ใช้ชุดสีจาก `Template excel.xlsx` (ตารางด้านล่าง) | ☐ |
| 5 | สรุปผลชัดเจน + ลิงก์กดได้จริง | Summary box + ตาราง Data Progress (เลียนแบบ Test Progress) ; `<a href>` ฝังเป็นลิงก์ | ☐ คลิกทดสอบ 1 ลิงก์ |
| 6 | แหล่งที่มาท้ายเอกสาร + เลขหน้า | Section "แหล่งที่มา" + footer `หน้า X / Y` | ☐ |
| 7 | ชื่อไฟล์มีวันที่ | ค่าเริ่มต้น `rail_route_YYYY-MM-DD.pdf` | ☐ |

## ชุดสีตาม Template excel.xlsx

### โครงตาราง (ดึงจากไฟล์ Template โดยตรง)
| ส่วนใน PDF | ตำแหน่งใน Template | สีพื้น | ตัวอักษร |
|---|---|---|---|
| หัวตาราง | แถว 5 (TC No … Note) | `#000000` ดำ | `#FFFFFF` ขาว ตัวหนา |
| ป้ายหัวข้อ / หัว Section | A2:A4 (API Doc, Defect Link, TEST RESULT) | `#CCCCCC` เทา | ดำ ตัวหนา |
| สรุปผล + หัวตาราง Data Progress | L1:V2 (Test Progress) | `#FFF2CC` เหลืองอ่อน | ดำ ตัวหนา |
| หัวข้อเส้นทาง / แถวแนะนำ | แถว 7 (แถวกลุ่ม) | `#A6C9EB` ฟ้า | ดำ ตัวหนา |
| แถวข้อมูล | แถว 8+ | `#FCFBD4` ครีม | ดำ |
| เส้นขอบ | ทุกเซลล์ | thin `#000000` | — |

### สีสถานะ
Template **ไม่มี Conditional Formatting** สำหรับคอลัมน์ Test result จึงใช้ Cell Styles มาตรฐานของ Excel (Good / Neutral / Bad) และจับคู่กับสถานะใน Template:

| สถานะรายงานรถไฟฟ้า | เทียบกับ Template | ตัวอักษร | พื้น | Excel Style |
|---|---|---|---|---|
| ยืนยันแล้ว | PASSED | `#006100` | `#C6EFCE` | Good |
| ไม่สามารถยืนยันได้ | Need confirmation | `#9C5700` | `#FFEB9C` | Neutral |
| ไม่พบข้อมูล | SKIPPED | `#404040` | `#D9D9D9` | — |
| ไม่มีบริการ | BLOCKED | `#9C0006` | `#FFC7CE` | Bad |

> ถ้าทีมกำหนดรหัสสีสถานะเองภายหลัง ให้แก้ที่ `XL` และ `STATUS` ใน `scripts/build_pdf.py` และอัปเดตตารางนี้ให้ตรงกัน
