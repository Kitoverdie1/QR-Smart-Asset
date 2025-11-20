# Home.py — หน้า Login หลัก

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
    """
    พยายามเด้งไปหน้า 1_หน้าหลัก.py
    ถ้าไม่ได้ก็ขึ้นข้อความบอกให้กดเมนูเอง (กันแอปล่ม)
    """
    candidates = [
        "pages/1_หน้าหลัก.py",
        "1_หน้าหลัก.py",
        "1_หน้าหลัก",
    ]
    for p in candidates:
        try:
            st.switch_page(p)
            return
        except Exception:
            continue

    st.success(
        "เข้าสู่ระบบสำเร็จแล้ว ✅ "
        "หากระบบไม่สลับหน้าให้อัตโนมัติ "
        "โปรดคลิกเมนู **1_หน้าหลัก** ที่แถบด้านซ้าย "
        "เพื่อเข้าสู่หน้า Smart Asset Lab Dashboard"
    )

# ==========================
# จัดการ session user
# ==========================
if "user" not in st.session_state:
    st.session_state["user"] = None

# ==========================
# CSS: พื้นหลังเดิม + กล่อง login กึ่งกลางจอ
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

    /* แผง login ด้านใน */
    .login-panel {
        width: 100%;
        max-width: 1100px;
        background: rgba(30, 64, 175, 0.25);
        border-radius: 18px;
        padding: 32px 40px 28px 40px;
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.20);
    }

    @media (max-width: 900px) {
        .login-panel {
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
        color: #9ca3af;
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
# Layout หน้า Login
# ==========================
st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="login-panel">', unsafe_allow_html=True)

# หัวข้อ
st.markdown('<div class="mem-title">MEM System</div>', unsafe_allow_html=True)
st.markdown(
    '<p class="mem-subtitle">Medical Equipment Management System</p>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="mem-subsubtitle">โรงพยาบาลมหาวิทยาลัยพะเยา</p>',
    unsafe_allow_html=True
)

# ฟอร์มล็อกอิน — ใช้ st.form เพื่อให้กด Enter ได้
with st.form("login_form", clear_on_submit=False):
    username = st.text_input("ชื่อผู้ใช้", placeholder="เช่น ton")
    password = st.text_input("รหัสผ่าน", placeholder="กรอกรหัสผ่าน", type="password")
    submitted = st.form_submit_button("เข้าสู่ระบบ")  # กด Enter -> submit ได้

# ตรวจสอบ Login
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

st.markdown(
    '<div class="login-footer">สำหรับเจ้าหน้าที่ภายในเท่านั้น</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)   # ปิด login-panel
st.markdown('</div>', unsafe_allow_html=True)   # ปิด page-wrapper
