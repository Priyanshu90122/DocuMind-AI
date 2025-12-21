import streamlit as st
import requests

st.set_page_config(page_title="OCR AI Agent", page_icon="🧠", layout="centered")

st.markdown("<h1 style='text-align:center;'>🧠 OCR + AI Agent System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload document image to analyze</p>", unsafe_allow_html=True)

file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if file:
    st.image(file, use_container_width=True)

    if st.button("🔍 Analyze Document", use_container_width=True):
        with st.spinner("Processing..."):
            res = requests.post(
                "http://127.0.0.1:8000/analyze",
                files={"file": file.getvalue()}
            )

        if res.status_code != 200:
            st.error("Backend error")
            st.text(res.text)
        else:
            data = res.json()

            st.subheader("📄 OCR Extracted Text")
            st.text_area("", data["ocr_text"], height=150)

            col1, col2 = st.columns(2)
            with col1:
                st.success(f"📌 Document Type: {data['document_type']}")
            with col2:
                st.warning(f"⚙️ Decision: {data['decision']}")

            st.subheader("📝 Explanation")
            st.info(data["explanation"])
