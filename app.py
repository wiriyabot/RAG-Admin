import streamlit as st
import time
from rag.retriever import get_retriever
from rag.vectordb import get_vectorstore
from rag.history import get_history, clear_history
from rag.chain import rag_chain
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Course Advisor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stAppHeader {
        background-color: transparent;
    }
    
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    h1 {
        color: #FF4B4B;
        font-family: 'Helvetica', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_rag():
    vectordb = get_vectorstore()
    retriever = get_retriever(vectordb)
    chain = rag_chain(retriever, get_history)
    return chain

try:
    chain = initialize_rag()
except Exception as e:
    st.error(f"Error loading RAG system: {e}")
    st.stop()

if "session_id" not in st.session_state:
    st.session_state.session_id = "user1"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "สวัสดีครับ! ผมเป็น AI ผู้ช่วยแนะนำคอร์สเรียน 🎓 \nมีคอร์สไหนที่คุณสนใจเป็นพิเศษ หรืออยากให้ผมแนะนำด้านไหนบอกได้เลยครับ!"}
    ]

with st.sidebar:
    st.title("⚙️ Control Panel")
    st.markdown("---")
    st.write("ระบบ **RAG Chatbot** สำหรับแนะนำคอร์สเรียน")
    
    if st.button("🗑️ ล้างประวัติการสนทนา", use_container_width=True):
        current_session = st.session_state.session_id
        clear_history(current_session)
        st.session_state.messages = [
            {"role": "assistant", "content": "สวัสดีครับ! เริ่มต้นคุยเรื่องคอร์สเรียนใหม่ได้เลยครับ"}
        ]
        st.rerun()
    
    st.markdown("---")
    st.caption("This project is for educational purposes only.")

st.title("🎓 Admin Sells Courses")
st.caption("🚀 ถาม-ตอบ ข้อมูลคอร์สเรียนด้วย AI อัจฉริยะ")

for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if question := st.chat_input("พิมพ์คำถามเกี่ยวกับคอร์สที่นี่..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="👤"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("กำลังค้นหาข้อมูลคอร์สที่เหมาะสม..."):
            try:
                response = chain.invoke(
                    {"question": question},
                    config={
                        "configurable": {
                            "session_id": st.session_state.session_id
                        }
                    }
                )
                if isinstance(response, dict) and 'answer' in response:
                    final_response = response['answer']
                elif isinstance(response, str):
                    final_response = response
                else:
                    final_response = str(response)

                st.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})
                
            except Exception as e:
                error_msg = f"เกิดข้อผิดพลาดในการประมวลผล: {e}"
                st.error(error_msg)