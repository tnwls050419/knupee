import streamlit as st

st.title("📄 수업 자료 다운로드")
st.markdown("---")

# --------------------------
# 1) 수업지도안(hwp) 다운로드
# --------------------------
st.subheader("📘 수업지도안(hwp) 다운로드")

try:
    with open("수업지도안.hwp", "rb") as f:
        st.download_button(
            label="💾 수업지도안 다운로드",
            data=f,
            file_name="수업지도안.hwp",
            mime="application/octet-stream",
        )
except FileNotFoundError:
    st.warning(
        "⚠️ `수업지도안.hwp` 파일이 없습니다.\n"
        "프로젝트 폴더(app.py와 같은 위치)에 파일을 넣어 주세요."
    )

st.markdown("---")

# --------------------------
# 2) 학습지(hwpx) 다운로드
# --------------------------
st.subheader("📝 학습지(hwpx) 다운로드")

try:
    with open("학습지.hwpx", "rb") as f:
        st.download_button(
            label="💾 학습지 다운로드",
            data=f,
            file_name="학습지.hwpx",
            mime="application/octet-stream",  # hwpx도 이걸로 OK
        )
except FileNotFoundError:
    st.warning(
        "⚠️ `학습지.hwpx` 파일이 없습니다.\n"
        "프로젝트 폴더(app.py와 같은 위치)에 파일을 넣어 주세요."
    )
