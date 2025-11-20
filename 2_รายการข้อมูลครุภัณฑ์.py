import streamlit as st
import pandas as pd
from pathlib import Path

EXCEL_PATH = "Smart Asset Lab (2).xlsx"  # ไฟล์อยู่โฟลเดอร์เดียวกับ Home.py

# ----------------------------
# บังคับให้ต้องล็อกอินก่อน
# ----------------------------
if "user" not in st.session_state:
    st.error("ยังไม่ได้เข้าสู่ระบบ กรุณาไปที่หน้า Home เพื่อล็อกอินก่อน")
    st.stop()

user = st.session_state["user"]

st.set_page_config(page_title="แก้ไขข้อมูลครุภัณฑ์", page_icon="✏️", layout="wide")

# ----------------------------
# helper สลับไปหน้าอื่น (เช่น Dashboard)
# ----------------------------
def go_to_page(page_path: str):
    """
    page_path เช่น 'pages/1_asset_dashboard.py'
    """
    if hasattr(st, "switch_page"):
        st.switch_page(page_path)
    else:
        st.warning("เวอร์ชัน Streamlit นี้ยังไม่รองรับ switch_page กรุณาใช้เมนูด้านซ้ายสลับหน้าแทน")


# ================================
# ฟังก์ชันโหลด & บันทึก Excel
# ================================
@st.cache_data
def load_assets(path: str) -> pd.DataFrame:
    file = Path(path)
    if not file.exists():
        st.error(f"ไม่พบไฟล์ Excel: {file.name}")
        st.stop()

    df = pd.read_excel(file)
    df = df.dropna(how="all").reset_index(drop=True)

    if "ต้นทุนต่อหน่วย" in df.columns:
        df["ต้นทุนต่อหน่วย"] = pd.to_numeric(df["ต้นทุนต่อหน่วย"], errors="coerce")

    return df


def save_assets(df_to_save: pd.DataFrame, path: str):
    """
    บันทึก DataFrame กลับไปที่ sheet แรกของไฟล์ Excel
    (แทนที่ข้อมูลเดิมทั้งหมดใน sheet แรก)
    """
    file = Path(path)
    xls = pd.ExcelFile(file)
    first_sheet = xls.sheet_names[0]

    with pd.ExcelWriter(file, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df_to_save.to_excel(writer, index=False, sheet_name=first_sheet)

    # เคลียร์ cache เพื่อให้โหลดข้อมูลใหม่หลังบันทึก
    load_assets.clear()


# ================================
# โหลดข้อมูล
# ================================
df = load_assets(EXCEL_PATH)

COL_NAME = "ชื่อ"
COL_CODE = "รหัสเครื่องมือห้องปฏิบัติการ"
COL_ASSET_ID = "AssetID"
COL_STATUS = "สถานะ"
COL_LOCATION = "สถานที่ใช้งาน (ปัจจุบัน)"

# ================================
# แถบนำทางด้านบน (ไปหน้าอื่น)
# ================================
nav_left, nav_right = st.columns([1.5, 1])

with nav_left:
    st.markdown(
        """
        <h2 style="margin-bottom:0.2rem;">
            ✏️ แก้ไขข้อมูลครุภัณฑ์
        </h2>
        """,
        unsafe_allow_html=True,
    )
    st.caption(
        "สามารถแก้ไขข้อมูลในตารางได้โดยตรง แล้วกดปุ่ม **บันทึกการแก้ไขลง Excel** ด้านล่าง "
        "ระบบจะอัปเดตเฉพาะแถวที่เห็นอยู่ในตาราง (ตามตัวกรอง) ลงในไฟล์ Excel"
    )

with nav_right:
    st.markdown("<div style='text-align:right;'>", unsafe_allow_html=True)
    if st.button("📊 ไปหน้า Dashboard สรุป", key="go_dashboard"):
        go_to_page("pages/1_asset_dashboard.py")
    st.markdown("</div>", unsafe_allow_html=True)

# กล่องข้อมูลผู้ใช้ด้านขวาบนเล็ก ๆ
info_col1, info_col2 = st.columns([4, 1.2])
with info_col2:
    st.markdown(
        f"""
        <div style="
            padding: 8px 12px;
            border-radius: 14px;
            background: #e3f2fd;
            margin-top: 4px;
        ">
            <div style="font-size:12px;color:#546e7a;">ผู้ใช้งาน</div>
            <div style="font-size:13px;font-weight:600;color:#0d47a1;">
                {user.get("display_name","-")}
            </div>
            <div style="font-size:11px;color:#78909c;">({user.get("username","")})</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ================================
# ตัวกรองด้านบน
# ================================
with st.expander("🔍 ตัวกรองรายการครุภัณฑ์", expanded=True):
    col_f1, col_f2, col_f3 = st.columns([2, 1.2, 1.2])

    with col_f1:
        keyword = st.text_input("ค้นหาจากชื่อ / รหัส / AssetID", placeholder="พิมพ์คำค้นหา...").strip()

    with col_f2:
        locations = ["ทั้งหมด"] + sorted(df[COL_LOCATION].dropna().unique().tolist()) if COL_LOCATION in df.columns else ["ทั้งหมด"]
        selected_location = st.selectbox("สถานที่ใช้งาน (ปัจจุบัน)", locations, index=0)

    with col_f3:
        if COL_STATUS in df.columns:
            statuses = df[COL_STATUS].dropna().unique().tolist()
        else:
            statuses = []
        selected_statuses = st.multiselect(
            "สถานะครุภัณฑ์",
            options=statuses,
            default=statuses
        )

# ใช้ตัวกรอง
filtered_df = df.copy()

if keyword:
    kw = keyword.lower()
    mask = (
        filtered_df[COL_NAME].astype(str).str.lower().str.contains(kw)
        | filtered_df[COL_CODE].astype(str).str.lower().str.contains(kw)
        | filtered_df[COL_ASSET_ID].astype(str).str.lower().str.contains(kw)
    )
    filtered_df = filtered_df[mask]

if COL_LOCATION in df.columns and selected_location != "ทั้งหมด":
    filtered_df = filtered_df[filtered_df[COL_LOCATION] == selected_location]

if COL_STATUS in df.columns and selected_statuses:
    filtered_df = filtered_df[filtered_df[COL_STATUS].isin(selected_statuses)]

st.caption(f"แสดง {len(filtered_df):,} แถว จากทั้งหมด {len(df):,} แถวในไฟล์ Excel")

# ================================
# ตารางแก้ไขข้อมูล
# ================================
st.markdown("### ✏️ แก้ไขข้อมูลในตาราง")

edited_df = st.data_editor(
    filtered_df,
    num_rows="fixed",         # ไม่ให้เพิ่ม/ลบแถวผ่านหน้าจอ (ปลอดภัยต่อโครงสร้างไฟล์)
    use_container_width=True,
    height=500,
    key="asset_editor_table"
)

# ================================
# ปุ่มบันทึกการแก้ไข
# ================================
st.markdown("---")
save_col1, save_col2 = st.columns([1.3, 3])

with save_col1:
    if st.button("💾 บันทึกการแก้ไขลง Excel", type="primary", use_container_width=True):
        try:
            # อัปเดตกลับเข้า df ต้นฉบับ ตาม index เดิม
            df_updated = df.copy()
            df_updated.loc[edited_df.index, :] = edited_df

            save_assets(df_updated, EXCEL_PATH)
            st.success("บันทึกการแก้ไขเรียบร้อยแล้ว ✅")
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดระหว่างบันทึกข้อมูล: {e}")

with save_col2:
    st.caption("ระบบจะเขียนทับข้อมูลในชีตแรกของไฟล์ Excel เท่านั้น (โครงสร้างไฟล์เดิมยังคงอยู่)")
