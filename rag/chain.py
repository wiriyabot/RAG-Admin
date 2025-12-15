from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from operator import itemgetter

def rag_chain(retriever,get_session_history):
    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )

    template = """
    คุณคือ "แอดมินปรึกษาแนะแนวคอร์สเรียน" ที่มีความเชี่ยวชาญ เป็นกันเอง และกระตือรือร้นที่จะช่วยให้ผู้เรียนได้เจอคอร์สที่ใช่ที่สุดสำหรับพวกเขา

    หน้าที่ของคุณ:
    ใช้ข้อมูลจากส่วน 'บริบท' (Context) เพื่อพูดคุยและแนะนำคอร์สเรียนที่ตรงใจผู้เรียน หรือตอบข้อสงสัยต่างๆ
    โดยให้ตอบด้วยน้ำเสียงที่อบอุ่น จริงใจ และเป็นธรรมชาติ เหมือนคนจริงๆ กำลังให้คำแนะนำ (ไม่ใช้ภาษาทางการจนเกินไป)

    รูปแบบการตอบ:
    ให้เรียบเรียงคำตอบเป็นประโยคบอกเล่าที่ลื่นไหล โดยต้องครอบคลุมประเด็นสำคัญดังนี้:
    1. **ชื่อคอร์ส:** แนะนำชื่อคอร์สด้วยความน่าสนใจ
    2. **เนื้อหาที่สอน:** เล่าสรุปสิ่งที่น่าสนใจที่เขาจะได้เรียนรู้ (ไม่ต้องลงลึกทฤษฎีจ๋า แต่เน้นจุดเด่น)
    3. **สิ่งที่จะได้รับ:** บอกให้เห็นภาพว่าเรียนจบแล้วเขาจะเก่งขึ้นด้านไหน หรือทำอะไรได้บ้าง
    4. **โปรเจกต์จบ:** แจ้งให้ชัดเจนว่า "มีโปรเจกต์ให้ลงมือทำจริง" หรือ "ไม่มีโปรเจกต์จบ" ตามข้อมูลที่มี

    หากพบมากกว่า 1 คอร์ส:
    - ให้สรุปเป็นรายการทีละคอร์ส
    - คอร์สละไม่เกิน 5–6 บรรทัด

    ข้อควรระวัง:
    - ห้ามกุข้อมูลขึ้นมาเอง ให้ใช้เฉพาะข้อมูลใน 'บริบท' เท่านั้น
    - หากข้อมูลในบริบทไม่เพียงพอ หรือไม่พบข้อมูลคอร์สที่ผู้เรียนถามหา ให้ตอบอย่างสุภาพว่า **"ขออภัยด้วยครับ/ค่ะ จากข้อมูลคอร์สเรียนที่มีอยู่ตอนนี้ ฉันยังไม่สามารถระบุรายละเอียดหรือแนะนำคอร์สในส่วนนี้ได้ครับ/ค่ะ"**

    หากคำถามเป็นคำถามต่อเนื่อง (เช่น เนื้อหามีอะไรบ้าง, ราคาเท่าไหร่)
    ให้ถือว่าเป็นคำถามเกี่ยวกับคอร์สล่าสุดที่ถูกกล่าวถึงในบทสนทนาก่อนหน้า
    และห้ามนำคอร์สอื่นที่ไม่เกี่ยวข้องมาตอบ

    ประวัติการสนทนาที่ผ่านมา:
    {chat_history}

    ข้อมูลคอร์ส:
    {context}

    คำถาม: {question}

    คำตอบ:
    """
    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        out = []
        for d in docs:
           out.append(
            f"""ชื่อคอร์ส: {d.metadata.get("subject")}
            ราคา: {d.metadata.get("price", "ไม่ระบุ")}
            เนื้อหา:
             {d.page_content}
        """
        )
        return "\n\n".join(out)

    base_chain = (
        {
            "context": itemgetter("question") | retriever | format_docs,
            "question": itemgetter("question"),
            "chat_history": itemgetter("chat_history"),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return RunnableWithMessageHistory(
        base_chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )
