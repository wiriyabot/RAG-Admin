# RAG-Admin: Intelligent Course Assistant

โปรเจกต์นี้เป็นระบบ **Retrieval-Augmented Generation (RAG)** สำหรับ **ผู้ดูแลคอร์สเรียน (Admin)**  
ช่วยให้สามารถตอบคำถามเกี่ยวกับคอร์สเรียนของคุณได้อย่างแม่นยำ โดยระบบจะค้นหาข้อมูลจาก **ฐานข้อมูลคอร์ส** และใช้ AI สร้างคำตอบที่ตรงกับความต้องการของผู้เรียน

---

## ฟีเจอร์หลัก (Features)
* **Course Data Ingestion:** รองรับการนำเข้าข้อมูลคอร์ส เช่น รายละเอียด, ราคา, ระยะเวลา, ผู้สอน (`build.py`)
* **Vector Search:** ค้นหาคอร์สที่ตรงกับความสนใจหรือคำถามของผู้เรียนได้อย่างรวดเร็ว
* **Context-Aware Chat:** ระบบจดจำประวัติการสนทนา ช่วยให้ตอบคำถามต่อเนื่องและเหมาะสม
* **Modular Design:** แยกส่วนการทำงานชัดเจน (Loader, Splitter, Retriever, Chain) ทำให้ปรับแต่งระบบง่าย

---

## Tech Stack
* Core: Python, LangChain
* Database: ChromaDB (Vector Store)
* Model: OpenAI gpt-4.1-mini (สามารถปรับเปลี่ยนได้)
* Interface: Streamlit

---

## โครงสร้างโปรเจกต์ (Structure)
```text
├── notebook/         # Jupyter Notebook สำหรับทดลองโมเดลและกระบวนการ RAG
├── rag/              # Source code หลักของระบบ RAG
│   ├── chain.py      # Logic การเชื่อมต่อกับ LLM และสร้าง Prompt
│   ├── history.py    # จัดการ Chat History ของผู้เรียน
│   ├── loader.py     # โหลดข้อมูลคอร์สจากไฟล์ต่างๆ (CSV, JSON, etc.)
│   ├── retriever.py  # ค้นหาข้อมูลคอร์สจาก Vector DB
│   └── vectordb.py   # จัดการการเชื่อมต่อกับ ChromaDB
├── raw_data/         # โฟลเดอร์วางไฟล์ข้อมูลคอร์สต้นฉบับ
├── app.py            # ไฟล์หลักสำหรับรัน Streamlit
├── build.py          # สร้าง Vector Database ของคอร์ส
└── requirements.txt
```

---

## การติดตั้งและใช้งาน (Installation & Usage)
1. Clone & Setup Environment:
```bash
git clone https://github.com/wiriyabot/RAG-Admin.git
cd RAG-Admin
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
pip install -r requirements.txt
```

---

2. Configuration:
สร้างไฟล์ .env ที่ root folder และใส่ API Key:
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxx
```

---

3. Build Course Database:
```bash
python build.py
```

---

4. Run Admin App:
```bash
streamlit run app.py
```

---

## หมายเหตุ
* วางข้อมูลคอร์สต้นฉบับใน raw_data/ ก่อนรัน build.py
* สามารถแก้ไขไฟล์ใน rag/ เพื่อปรับ Prompt ของ AI ให้ตอบคำถามคอร์สได้ตรงตามสไตล์ของคุณ
* รองรับการเพิ่มคอร์สใหม่และอัปเดตฐานข้อมูลโดยไม่กระทบระบบหลัก

---

## ตัวอย่างการใช้งาน
<img width="914" height="595" alt="image" src="https://github.com/user-attachments/assets/ac65c363-d725-40d9-b6de-73134ff517aa" />

* มีระบบจดจำประวัติการสนทนา

<img width="903" height="564" alt="image" src="https://github.com/user-attachments/assets/e30425e4-ff54-4b0f-b1b7-ae0d0fd7451d" />

---
