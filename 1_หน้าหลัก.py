# pages/1_asset_dashboard.py

import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

EXCEL_PATH = "Smart Asset Lab (2).xlsx"  # ไฟล์อยู่โฟลเดอร์เดียวกับ Home.py

# ----------------------------
# ถ้าไม่ได้ล็อกอิน ให้บล็อกหน้าไว้
# ----------------------------
if "user" not in st.session_state:
    st.error("ยังไม่ได้เข้าสู่ระบบ กรุณาไปที่หน้า Home เพื่อล็อกอินก่อน")
    st.stop()

user = st.session_state["user"]

# ================================
# ฟังก์ชันโหลดข้อมูลจาก Excel
# ================================
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    file = Path(path)
    if not file.exists():
        st.error(f"ไม่พบไฟล์ Excel: {file.name}\n\nโปรดวางไฟล์ไว้ในโฟลเดอร์เดียวกับ Home.py")
        st.stop()

    df = pd.read_excel(file)
    df = df.dropna(how="all").reset_index(drop=True)

    if "ต้นทุนต่อหน่วย" in df.columns:
        df["ต้นทุนต่อหน่วย"] = pd.to_numeric(df["ต้นทุนต่อหน่วย"], errors="coerce")

    return df


df = load_data(EXCEL_PATH)

# ตั้งชื่อคอลัมน์
COL_NAME = "ชื่อ"
COL_CODE = "รหัสเครื่องมือห้องปฏิบัติการ"
COL_TYPE = "ประเภทครุภัณฑ์"
COL_SUBTYPE = "ชนิดของครุภัณฑ์"
COL_ASSET_ID = "AssetID"
COL_YEAR = "ปี"
COL_STATUS = "สถานะ"
COL_LOCATION = "สถานที่ใช้งาน (ปัจจุบัน)"
COL_OWNER = "ผู้รับผิดชอบ (ปัจจุบัน)"
COL_COST = "ต้นทุนต่อหน่วย"

# ================================
# HEADER + แสดงชื่อผู้ใช้ / ปุ่มออกจากระบบ
# ================================
top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.markdown(
        """
        <div style="
            padding: 18px 24px;
            border-radius: 18px;
            background: linear-gradient(90deg, #0d47a1, #1976d2);
            color: #e3f2fd;
            margin-bottom: 18px;
        ">
            <h2 style="margin: 0; font-weight: 600;">Smart Asset Lab Dashboard</h2>
            <p style="margin: 4px 0 0; opacity: 0.9;">
                แดชบอร์ดสรุปข้อมูลครุภัณฑ์จากไฟล์ Excel: Smart Asset Lab
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with top_col2:
    st.markdown(
        f"""
        <div style="
            padding: 12px 16px;
            border-radius: 14px;
            background: #e3f2fd;
            margin-top: 8px;
        ">
            <div style="font-size:13px;color:#546e7a;">ผู้ใช้งานปัจจุบัน</div>
            <div style="font-size:14px;font-weight:600;color:#0d47a1;">
                {user.get("display_name","-")}
            </div>
            <div style="font-size:12px;color:#78909c;">({user.get("username","")})</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.sidebar.markdown(f"**👤 ผู้ใช้งาน:** {user.get('display_name','-')}")
if st.sidebar.button("ออกจากระบบ"):
    st.session_state.clear()
    st.sidebar.success("ออกจากระบบแล้ว กลับไปหน้า Home เพื่อล็อกอินใหม่")
    st.stop()

# ================================
# ตัวกรองข้อมูล
# ================================
st.sidebar.header("🔍 ตัวกรองข้อมูล")

locations = ["ทั้งหมด"] + sorted(df[COL_LOCATION].dropna().unique().tolist())
selected_location = st.sidebar.selectbox("สถานที่ใช้งาน (ปัจจุบัน)", locations, index=0)

statuses = df[COL_STATUS].dropna().unique().tolist()
selected_statuses = st.sidebar.multiselect(
    "สถานะครุภัณฑ์",
    options=statuses,
    default=statuses
)

keyword = st.sidebar.text_input("คำค้นหา (ชื่อ / รหัส / AssetID)", value="").strip()

years = df[COL_YEAR].dropna().unique().tolist()
years = sorted(years)
selected_year = st.sidebar.selectbox("ปีที่ได้มา (ปีงบประมาณ)", ["ทั้งหมด"] + years, index=0)

st.sidebar.markdown("---")
st.sidebar.caption("ข้อมูลดึงจากไฟล์ Excel โดยตรง")

# ================================
# ใช้ตัวกรอง
# ================================
filtered_df = df.copy()

if selected_location != "ทั้งหมด":
    filtered_df = filtered_df[filtered_df[COL_LOCATION] == selected_location]

if selected_statuses:
    filtered_df = filtered_df[filtered_df[COL_STATUS].isin(selected_statuses)]

if selected_year != "ทั้งหมด":
    filtered_df = filtered_df[filtered_df[COL_YEAR] == selected_year]

if keyword:
    keyword_lower = keyword.lower()
    mask = (
        filtered_df[COL_NAME].astype(str).str.lower().str.contains(keyword_lower)
        | filtered_df[COL_CODE].astype(str).str.lower().str.contains(keyword_lower)
        | filtered_df[COL_ASSET_ID].astype(str).str.lower().str.contains(keyword_lower)
    )
    filtered_df = filtered_df[mask]

# ================================
# KPI
# ================================
total_items = len(filtered_df)
total_cost = filtered_df[COL_COST].sum(skipna=True)

status_counts = filtered_df[COL_STATUS].value_counts()

count_ready = int(status_counts.get("พร้อมใช้งาน", 0))
count_repairable = int(status_counts.get("ชำรุด(ซ่อมแซมได้)", 0))
count_not_repairable = int(status_counts.get("ชำรุด(ซ่อมแซมไม่ได้)", 0))
count_not_found = int(status_counts.get("ตรวจไม่พบ", 0))

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("จำนวนครุภัณฑ์ (ตามตัวกรอง)", f"{total_items:,} ชิ้น")
with c2:
    st.metric("มูลค่ารวมประมาณการ", f"{total_cost:,.2f} บาท")
with c3:
    st.metric("พร้อมใช้งาน", f"{count_ready:,} ชิ้น")
with c4:
    st.metric(
        "ชำรุด / ตรวจไม่พบ",
        f"{(count_repairable + count_not_repairable + count_not_found):,} ชิ้น"
    )

with st.expander("ดูจำนวนตามสถานะรายประเภท", expanded=False):
    cc1, cc2, cc3, cc4 = st.columns(4)
    cc1.write(f"✅ พร้อมใช้งาน: **{count_ready:,}**")
    cc2.write(f"🛠 ชำรุด(ซ่อมแซมได้): **{count_repairable:,}**")
    cc3.write(f"❌ ชำรุด(ซ่อมแซมไม่ได้): **{count_not_repairable:,}**")
    cc4.write(f"❓ ตรวจไม่พบ: **{count_not_found:,}**")

st.markdown("---")

# ================================
# กราฟแท่งภาพรวม
# ================================
st.subheader("📊 กราฟสรุปภาพรวม")

g1, g2 = st.columns(2)

with g1:
    st.markdown("**จำนวนครุภัณฑ์ตามสถานที่ใช้งาน (ปัจจุบัน)**")
    if not filtered_df.empty:
        loc_counts = (
            filtered_df.groupby(COL_LOCATION)[COL_CODE]
            .count().sort_values(ascending=False)
        )
        st.bar_chart(loc_counts)
    else:
        st.info("ไม่มีข้อมูลสำหรับแสดงกราฟ")

with g2:
    st.markdown("**จำนวนครุภัณฑ์ตามสถานะ**")
    if not filtered_df.empty:
        status_for_chart = (
            filtered_df.groupby(COL_STATUS)[COL_CODE]
            .count().sort_values(ascending=False)
        )
        st.bar_chart(status_for_chart)
    else:
        st.info("ไม่มีข้อมูลสำหรับแสดงกราฟ")

st.markdown("---")

# ================================
# กราฟโดนัท + ตารางรายละเอียดสถานะ (สีโทนอ่อน + legend แบบตัวอักษร)
# ================================
st.subheader("📌 สัดส่วนตามสถานะครุภัณฑ์")

col_pie, col_table = st.columns([2, 1])

if not filtered_df.empty and not status_counts.empty:
    # กำหนดลำดับสถานะให้สีคงที่เสมอ
    status_order = [
        "พร้อมใช้งาน",
        "ตรวจไม่พบ",
        "ชำรุด(ซ่อมแซมได้)",
        "ชำรุด(ซ่อมแซมไม่ได้)",
    ]

    # สีโทนอ่อน ดูสบายตา
    color_map = {
        "พร้อมใช้งาน": "#4CAF50",            # เขียวอ่อน
        "ตรวจไม่พบ": "#90A4AE",             # เทา
        "ชำรุด(ซ่อมแซมได้)": "#FFCA28",     # เหลืองอ่อน
        "ชำรุด(ซ่อมแซมไม่ได้)": "#EF5350",  # แดงอ่อน
    }

    labels = []
    sizes = []
    colors = []

    for s in status_order:
        if s in status_counts:
            labels.append(s)
            sizes.append(int(status_counts[s]))
            colors.append(color_map.get(s))

    total = sum(sizes)
    percents = [value / total * 100 for value in sizes]

    # ---------- ฝั่งกราฟโดนัท ----------
    with col_pie:
        fig, ax = plt.subplots(figsize=(5.2, 5.2))

        def autopct_fmt(pct):
            return f"{pct:.1f}%" if pct >= 3 else ""

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=None,  # ไม่แสดงชื่อสถานะบนชาร์ต กันตัวหนังสือไทยทับกัน
            autopct=autopct_fmt,
            startangle=90,
            colors=colors,
            wedgeprops=dict(width=0.42, edgecolor="white"),
            pctdistance=0.8
        )
        ax.axis("equal")

        # ปรับสไตล์ตัวเลขเปอร์เซ็นต์บนชิ้นกราฟ
        plt.setp(autotexts, size=12, weight="bold", color="white")

        # ❌ ลบ legend ของ matplotlib ทิ้ง (อันที่เป็นกล่องเล็ก ๆ )
        # ax.legend(
        #     wedges,
        #     labels,
        #     title="สถานะ",
        #     loc="center left",
        #     bbox_to_anchor=(1.05, 0.5),
        #     frameon=False,
        #     fontsize=10
        # )

        st.pyplot(fig)

        # Legend แบบตัวอักษรชัด ๆ ใต้กราฟ (ใช้ emoji สีแทน)
        emoji_map = {
            "พร้อมใช้งาน": "🟢",
            "ตรวจไม่พบ": "⚪",
            "ชำรุด(ซ่อมแซมได้)": "🟡",
            "ชำรุด(ซ่อมแซมไม่ได้)": "🔴",
        }
        lines = []
        for lbl, size, pct in zip(labels, sizes, percents):
            emoji = emoji_map.get(lbl, "⬜")
            lines.append(f"{emoji} **{lbl}** – {size:,} ชิ้น ({pct:.1f}%)")
            # เช่น: 🟢 พร้อมใช้งาน – 213 ชิ้น (66.4%)
        st.markdown("\n".join(lines))

    # ---------- ฝั่งตาราง ----------
    with col_table:
        status_summary_df = pd.DataFrame({
            "สถานะ": labels,
            "จำนวน": sizes,
            "เปอร์เซ็นต์": [f"{p:.1f}%" for p in percents]
        }).reset_index(drop=True)

        st.markdown("### รายละเอียดสถานะ")
        st.table(status_summary_df)
else:
    with col_pie:
        st.info("ไม่มีข้อมูลสำหรับแสดงสัดส่วนตามสถานะ")
    with col_table:
        st.markdown("### รายละเอียดสถานะ")
        st.info("ไม่มีข้อมูล")

st.markdown("---")

# ================================
# ตาราง + ดาวน์โหลด Excel
# ================================
st.subheader("📋 รายการครุภัณฑ์ (ตามตัวกรอง)")
st.caption(f"แสดงทั้งหมด {len(filtered_df):,} แถว จาก {len(df):,} แถวในไฟล์ Excel")

st.dataframe(
    filtered_df[
        [
            COL_CODE,
            COL_NAME,
            COL_TYPE,
            COL_SUBTYPE,
            COL_ASSET_ID,
            COL_YEAR,
            COL_STATUS,
            COL_LOCATION,
            COL_OWNER,
            COL_COST,
        ]
    ],
    use_container_width=True,
    height=450
)

output_file_name = "Smart_Asset_Lab_Filtered.xlsx"

@st.cache_data
def convert_df_to_excel_bytes(dataframe: pd.DataFrame) -> bytes:
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="FilteredData")
    output.seek(0)
    return output.getvalue()

if not filtered_df.empty:
    excel_bytes = convert_df_to_excel_bytes(filtered_df)
    st.download_button(
        label="⬇️ ดาวน์โหลดข้อมูลที่กรองแล้วเป็น Excel",
        data=excel_bytes,
        file_name=output_file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
