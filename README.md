# Bio Cards · Slide 07–12

เกมจับคู่และ Flash cards จากคลังข้อสอบ Slide 07–13

เปิดใช้งาน: https://phisanuwatspy.github.io/bio-cards/

## Drug Quiz

คลังยาและข้อสอบสุ่มจากฐานข้อมูลยา (pilot 46 ตัว, 7 หมวด)

เปิดใช้งาน: https://phisanuwatspy.github.io/bio-cards/drug-quiz/

- ฐานข้อมูล: `drug-quiz/src/drugs.json`
- เพิ่มยาใหม่: ใส่ยาใน `drugs` แล้วเพิ่ม id ลงใน tag ของ `adr` / `use` / `ci` ที่เกี่ยวข้อง (`yes` = เกี่ยวข้องชัด, `maybe` = เกี่ยวข้องบ้าง จะไม่ถูกใช้เป็นตัวเลือกหลอก)
- Build: `python3 drug-quiz/src/build.py` (ตรวจข้อมูลแล้วสร้าง `drug-quiz/index.html`)

## v7 — ชีววิทยาอย่างเดียว
- หน้าแรก: แตะ "ทบทวนวันนี้" ครั้งเดียว ระบบเลือกการ์ดที่ใกล้ลืม (spaced repetition) + การ์ดใหม่ให้เอง
- เลือกเอง: ชีววิทยา (Slide 07–13) → ทวนเร็ว / Flash cards / จับคู่
- ข้อมูลยาถูกปิดไว้ (`INCLUDE_DRUGS = False` ใน `src/build5.py`)
- สร้างใหม่: `python3 src/build5.py` (template `src/template6.html`, ข้อมูลยา `src/drug_items.py` จาก `drug-quiz/src/drugs.json`)

## ดนตรี Final

สื่อการสอนแอนิเมชัน 5 บท + ข้อสอบจำลอง (★ = จุดเน้น)

เปิดใช้งาน: https://phisanuwatspy.github.io/bio-cards/music-final/

- แก้เนื้อหาที่ `music-final/index.html` (ไฟล์เดียว) แล้ว bump `VERSION` ใน `music-final/sw.js`
