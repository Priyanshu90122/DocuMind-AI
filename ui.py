import streamlit as st
import requests
import time

st.set_page_config(
    page_title="Document Intelligence Dashboard",
    page_icon="🧠",
    layout="centered"
)

st.markdown(
    "<h1 style='text-align:center;'>🧠 Document Intelligence Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Upload a document image to analyze classification, extraction, and approval decision</p>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload Document Image",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file:
    st.image(uploaded_file, use_container_width=True)

    if st.button("🔍 Run Analysis", use_container_width=True):
        start_time = time.time()

        with st.spinner("Processing document..."):
            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                files={"file": uploaded_file.getvalue()}
            )

        if response.status_code != 200:
            st.error("Processing failed")
            st.text(response.text)
        else:
            data = response.json()

            st.subheader("📄 OCR Extracted Text")
            st.text_area("", data.get("ocr_text", ""), height=150)

            st.subheader("📌 Classification & Decision")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Document Type", data.get("document_type", "N/A"))
            with col2:
                st.metric("Decision", data.get("decision", "N/A"))
            with col3:
                st.metric(
                    "Processing Time (s)",
                    data.get("processing_time_seconds", round(time.time() - start_time, 3))
                )

            st.subheader("🧩 Extracted Fields")
            st.json(data.get("extracted_fields", {}))

            st.subheader("📝 System Explanation")
            st.info(data.get("explanation", ""))
