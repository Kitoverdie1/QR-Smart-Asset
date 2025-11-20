# Home.py — หน้า Login หลัก MEM System

import streamlit as st

st.set_page_config(
    page_title="MEM System - Login",
    page_icon="🔐",
    layout="wide"
)

# ==========================
# ฟังก์ชันเปลี่ยนหน้าไป 1_หน้าหลัก.py
# ==========================
def go_to_dashboard():
    """เปลี่ยนไปหน้า 1_หน้าหลัก.py ในโฟลเดอร์ pages"""
    try:
        # ต้องให้ path ตรงกับไฟล์ในโฟลเดอร์ pages
        st.switch_page("pages/1_หน้าหลัก.py")
    except Exception as e:
        # ถ้าเด้งไม่ได้ ให้บอกสาเหตุ + วิธีแก้ชั่วคราว
        st.error(
            "ไม่สามารถสลับหน้าไปยัง **1_หน้าหลัก.py** ได้โดยอัตโนมัติ 😥\n\n"
            "กรุณาตรวจสอบว่าไฟล์อยู่ที่โฟลเดอร์ `pages/` "
            "และชื่อไฟล์สะกดว่า `1_หน้าหลัก.py` ตรงทุกตัว (รวมทั้งตัวพิมพ์ใหญ่/เล็ก)\n\n"
            f"รายละเอียดทางเทคนิค: `{e}`\n\n"
            "ระหว่างนี้คุณยังสามารถคลิกเมนู **1_หน้าหลัก** ที่แถบด้านซ้าย "
            "เพื่อเข้า Smart Asset Lab Dashboard ได้ตามปกติครับ ✅"
        )


# ==========================
# จัดการ session user
# ==========================
if "user" not in st.session_state:
    st.session_state["user"] = None

# ==========================
# CSS: พื้นหลัง + การจัดกลาง + กรอบเดียว
# ==========================
st.markdown(
    """
    <style>
    body, .stApp {
        margin: 0;
        padding: 0;
        background: radial-gradient(circle at top, #7ab8ff 0, #6c8fff 40%, #4b3fb3 80%, #2c1d7a 100%);
        font-family: "Sarabun", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    /* ครอบทั้งหน้าให้จัดกลางจอ */
    .page-wrapper {
        min-height: 100vh;
        display: flex;
        justify-content: center;   /* แนวนอน */
        align-items: center;       /* แนวตั้ง */
        padding: 24px;
    }

    /* กรอบ login อันเดียวที่เก็บทุกอย่าง */
    .login-card {
        width: 100%;
        max-width: 1000px;
        background: rgba(255, 255, 255, 0.10);
        border-radius: 24px;
        padding: 32px 40px 28px 40px;
        box-shadow: 0 24px 50px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.25);
    }

    @media (max-width: 900px) {
        .login-card {
            padding: 24px 20px 20px 20px;
        }
    }

    .mem-title {
        text-align: center;
        font-size: 32px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 4px;
    }
    .mem-subtitle {
        text-align: center;
        font-size: 14px;
        color: #374151;
        margin: 0;
    }
    .mem-subsubtitle {
        text-align: center;
        font-size: 13px;
        color: #e5e7eb;
        margin-top: 2px;
        margin-bottom: 24px;
    }
    .login-footer {
        margin-top: 24px;
        text-align: center;
        font-size: 12px;
        color: #e5e7eb;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================
# Layout: ทุกอย่างอยู่ในกรอบเดียวกลางจอ
# ==========================
st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="login-card">', unsafe_allow_html=True)

# หัวข้อในกรอบ
st.markdown('<div class="mem-title">MEM System</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="mem-subtitle">Medical Equipment Management System</p>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="mem-subsubtitle">โรงพยาบาลมหาวิทยาลัยพะเยา</p>',
    unsafe_allow_html=True
)

# ==========================
# ฟอร์มล็อกอิน — ใช้ st.form เพื่อให้กด Enter ได้
# ==========================
with st.form("login_form", clear_on_submit=False):
    username = st.text_input("ชื่อผู้ใช้", placeholder="เช่น admin")
    password = st.text_input("รหัสผ่าน", placeholder="เช่น admin123", type="password")
    submitted = st.form_submit_button("เข้าสู่ระบบ")  # กด Enter -> submit ได้

# ==========================
# ตรวจสอบ Login
# ==========================
if submitted:
    if username == "admin" and password == "admin123":
        st.session_state["user"] = {
            "username": username,
            "display_name": "ผู้ดูแลระบบครุภัณฑ์"
        }
        st.success("เข้าสู่ระบบสำเร็จ! กำลังนำทางไปยังหน้าแรก ...")
        go_to_dashboard()
    else:
        st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

# ข้อความล่างในกรอบเดียวกัน
st.markdown(
    '<div class="login-footer">สำหรับเจ้าหน้าที่ภายในเท่านั้น</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)   # ปิด login-card
st.markdown('</div>', unsafe_allow_html=True)   # ปิด page-wrapper
