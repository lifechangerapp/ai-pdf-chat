import streamlit as st

from pdf_reader import extract_text
from text_splitter import split_text
from embeddings import get_embeddings
from vector_store import create_vector_store
from chatbot import get_llm, ask_question


@st.cache_resource
def load_vector_store(text):

    chunks = split_text(text)

    embeddings = get_embeddings()

    vector_store = create_vector_store(
        chunks,
        embeddings
    )

    return vector_store, chunks


st.set_page_config(
    page_title="PDF Reader",
    page_icon="📄"
)

st.title("📄 PDF Reader")
st.write("Upload a PDF file and ask questions about it.")

uploaded_file = st.file_uploader(
    "Choose a PDF",
    type="pdf"
)

if uploaded_file is not None:

    # Extract text
    text = extract_text(uploaded_file)

    st.success("PDF Loaded Successfully!")

    # Show extracted text
    st.subheader("Extracted Text")

    st.text_area(
        "PDF Content",
        text,
        height=300
    )

    # Create Vector Store (Cached)
    vector_store, chunks = load_vector_store(text)

    # Load LLM
    llm = get_llm()

    # Chunk Info
    st.subheader("Chunk Information")
    st.write(f"Total Chunks: {len(chunks)}")

    # Show first 3 chunks
    for i, chunk in enumerate(chunks[:3]):
        st.markdown(f"### Chunk {i + 1}")
        st.text(chunk)

    # Ask Question
    question = st.text_input(
        "Ask a question about this PDF"
    )

    if question:

        answer, docs = ask_question(
            llm,
            vector_store,
            question
        )

        st.subheader("Answer")
        st.success(answer)

        with st.expander("Retrieved Chunks"):

            for i, doc in enumerate(docs):

                st.markdown(f"### Match {i + 1}")

                st.write(doc.page_content)