# 📚 RAG Knowledge Base Assistant

โปรเจกต์นี้เป็นระบบ **Retrieval-Augmented Generation (RAG)** ที่ช่วยให้ผู้ใช้สามารถสอบถามข้อมูลจากเอกสารเฉพาะทางได้ โดยระบบจะค้นหาข้อมูลที่เกี่ยวข้องจาก Vector Database และนำไปให้ AI ประมวลผลเพื่อตอบคำถามอย่างแม่นยำ

## 🚀 ฟีเจอร์หลัก (Features)
* **Document Ingestion:** รองรับการนำเข้าข้อมูลดิบและแปลงเป็น Vector (ผ่าน `build.py` หรือ Notebook)
* **Vector Search:** ค้นหาข้อมูลที่ใกล้เคียงที่สุดอย่างรวดเร็วด้วย **ChromaDB**
* **Context-Aware Chat:** ระบบจดจำประวัติการสนทนา (History Aware) ช่วยให้คุยต่อเนื่องได้ไหลลื่น
* **Modular Design:** แยกส่วนการทำงานชัดเจน (Loader, Splitter, Retriever, Chain) ง่ายต่อการพัฒนาต่อ

## 📂 โครงสร้างโปรเจกต์ (Structure)
```text
├── chroma_db/      # โฟลเดอร์เก็บข้อมูล Vector Database (ห้ามลบ)
├── notebook/       # Jupyter Notebook สำหรับทดลองโมเดลและกระบวนการ RAG
├── rag/            # Source code หลักของระบบ RAG
│   ├── chain.py    # Logic การเชื่อมต่อกับ LLM และสร้าง Prompt
│   ├── history.py  # จัดการ Chat History
│   ├── loader.py   # โหลดเอกสารจากไฟล์ต่างๆ (PDF, TXT, etc.)
│   ├── retriever.py# ค้นหาข้อมูลจาก Vector DB
│   └── vectordb.py # จัดการการเชื่อมต่อกับ ChromaDB
├── raw_data/       # โฟลเดอร์วางไฟล์เอกสารต้นฉบับที่ต้องการนำเข้า
├── app.py          # ไฟล์หลักสำหรับรัน Web Interface (Streamlit/Flask)
├── build.py        # สคริปต์สำหรับสร้าง Vector Database ครั้งแรก
└── requirements.txt

