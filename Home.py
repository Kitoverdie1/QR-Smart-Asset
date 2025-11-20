import streamlit as st

st.set_page_config(
    page_title="MEM System Login",
    page_icon="🩺",
    layout="wide"
)

# ----------------------------
# USERS สำหรับล็อกอิน (แก้ได้)
# ----------------------------
USERS = {
    "admin": {"password": "admin123", "display_name": "ผู้ดูแลระบบครุภัณฑ์"},
    "lab":   {"password": "lab123",   "display_name": "เจ้าหน้าที่ห้องปฏิบัติการ"},
    # "user1": {"password": "pass001", "display_name": "เจ้าหน้าที่ 1"},
}

# ----------------------------
# helper สำหรับเด้งไปหน้า dashboard
# ----------------------------
def go_to_dashboard():
    if hasattr(st, "switch_page"):
        # ชื่อไฟล์ในโฟลเดอร์ pages
        st.switch_page("pages/1_หน้าหลัก.py")
    else:
        # ถ้าเวอร์ชันเก่าไม่มี switch_page ก็ยังใช้งานได้ แค่ให้คลิกเมนูเอง
        st.info("ล็อกอินสำเร็จแล้ว ให้คลิกเมนู 'asset dashboard' ที่แถบซ้ายเพื่อเข้าใช้งาน")

# ================================
# CSS: ทำให้เป็นการ์ดขาวกลางจอ
# ================================
st.markdown(
    """
    <style>
    /* พื้นหลังไล่สี */
    .stApp {
        background: radial-gradient(circle at 20% 0%, #A8C5FF 0%, #6D79FF 40%, #4B2CA3 100%);
    }

    /* ให้ block-container เป็นการ์ดกลางจอ */
    section.main {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    section.main > div.block-container {
        max-width: 480px;
        width: 100%;
        background: #ffffff;
        border-radius: 32px;
        padding: 32px 40px 28px 40px;
        box-shadow: 0 26px 60px rgba(15, 23, 42, 0.40);
    }

    /* หัวการ์ด */
    .login-title {
        font-size: 26px;
        font-weight: 700;
        text-align: center;
        color: #111827;
        margin-bottom: 4px;
    }
    .login-subtitle-main {
        text-align: center;
        font-size: 14px;
        font-weight: 600;
        color: #4b5563;
        margin-bottom: 0;
    }
    .login-subtitle-org {
        text-align: center;
        font-size: 13px;
        color: #7c3aed;
        margin-bottom: 20px;
    }
    .login-footer {
        margin-top: 16px;
        font-size: 11px;
        text-align: center;
        color: #9ca3af;
    }

    /* ปรับ input ให้โค้งสวย */
    .stTextInput > div > div > input {
        border-radius: 999px !important;
        border: 1px solid #e5e7eb !important;
        padding: 0.55rem 0.9rem !important;
        box-shadow: none !important;
        outline: none !important;
        font-size: 14px !important;
    }
    .stTextInput > label {
        font-weight: 600;
        color: #111827;
        font-size: 14px;
    }

    /* ปุ่มเข้าสู่ระบบ */
    .stButton > button {
        border-radius: 999px;
        border: none;
        width: 100%;
        background: linear-gradient(90deg, #6366f1, #ec4899);
        color: #ffffff;
        font-weight: 600;
        padding: 0.55rem 1.2rem;
        font-size: 14px;
        box-shadow: 0 12px 25px rgba(79, 70, 229, 0.45);
    }
    .stButton > button:hover {
        filter: brightness(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ================================
# ถ้าล็อกอินแล้ว เปิด Home อีก -> ส่งเข้า dashboard เลย
# ================================
if "user" in st.session_state:
    go_to_dashboard()
    st.stop()

# ================================
# เนื้อหาการ์ด Login (อยู่กลางจอ)
# ================================
st.markdown('<div class="login-title">MEM System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="login-subtitle-main">Medical Equipment Management System</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="login-subtitle-org">โรงพยาบาลมหาวิทยาลัยพะเยา</div>',
    unsafe_allow_html=True,
)

username = st.text_input("ชื่อผู้ใช้", placeholder="เช่น ton", key="login_username")
password = st.text_input("รหัสผ่าน", type="password", placeholder="กรอกรหัสผ่าน", key="login_password")

login_btn = st.button("เข้าสู่ระบบ")

if login_btn:
    user = USERS.get(username)
    if user and password == user["password"]:
        st.session_state["user"] = {
            "username": username,
            "display_name": user["display_name"],
        }
        go_to_dashboard()
    else:
        st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

st.markdown('<div class="login-footer">สำหรับเจ้าหน้าที่ภายในเท่านั้น</div>', unsafe_allow_html=True)
