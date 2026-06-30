import streamlit as st
from pypdf import PdfReader
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

    reader = PdfReader(uploaded_file)

    text = ""

    # PDF का पूरा Text पढ़ो
    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    st.success("PDF Loaded Successfully!")

    # पूरा Text दिखाओ
    st.subheader("Extracted Text")

    st.text_area(
        "PDF Content",
        text,
        height=300
    )

    # Text को Chunks में बाँटो
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    st.subheader("Chunk Information")
    st.write(f"Total Chunks: {len(chunks)}")

    # पहले 3 Chunks दिखाओ
    for i, chunk in enumerate(chunks[:3]):
        st.markdown(f"### Chunk {i+1}")
        st.text(chunk)