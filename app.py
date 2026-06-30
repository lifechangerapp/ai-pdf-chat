import streamlit as st
from pdf_reader import extract_text
from text_splitter import split_text
from langchain_text_splitters import RecursiveCharacterTextSplitter

st.set_page_config(
    page_title="PDF Reader",
    page_icon="📄"
)

st.title("📄 PDF Reader")
st.write("Upload a PDF file and view its text.")

uploaded_file = st.file_uploader(
    "Choose a PDF",
    type="pdf"
)

if uploaded_file is not None:

    text = extract_text(uploaded_file)

    # पूरा Text दिखाओ
    st.subheader("Extracted Text")

    st.text_area(
        "PDF Content",
        text,
        height=300
    )

    chunks = split_text(text)

    st.subheader("Chunk Information")
    st.write(f"Total Chunks: {len(chunks)}")

    # पहले 3 Chunks दिखाओ
    for i, chunk in enumerate(chunks[:3]):
        st.markdown(f"### Chunk {i+1}")
        st.text(chunk)