import streamlit as st
from pdf_reader import extract_documents
from text_splitter import split_documents
from embeddings import get_embeddings
from vector_store import create_vector_store
from chatbot import get_llm, ask_question

# Page configuration
st.set_page_config(
    page_title="PDF Chat App",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "processing" not in st.session_state:
    st.session_state.processing = False
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None
if "pdf_size" not in st.session_state:
    st.session_state.pdf_size = None
if "num_chunks" not in st.session_state:
    st.session_state.num_chunks = None

# Sidebar
with st.sidebar:
    st.title("📄 PDF Chat App")
    st.caption("Powered by Ollama + LangChain")

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type="pdf",
        label_visibility="collapsed",
        help="Select a PDF file to chat with"
    )

    # Process uploaded file
    if uploaded_file is not None:
        # Only process if not already processed or if new file
        if st.session_state.pdf_name != uploaded_file.name or st.session_state.vector_store is None:
            with st.status("Processing PDF...", expanded=True) as status:
                try:
                    # Read PDF
                    st.write("📖 Reading PDF...")
                    documents = extract_documents(uploaded_file)

                    # Split text
                    st.write("✂️ Splitting text into chunks...")
                    chunks = split_documents(documents)

                    # Get embeddings
                    st.write("🔢 Generating embeddings...")
                    embeddings = get_embeddings()

                    # Create vector store
                    st.write("🗄️ Creating vector store...")
                    vector_store = create_vector_store(chunks, embeddings)

                    # Store in session state
                    st.session_state.vector_store = vector_store
                    st.session_state.pdf_name = uploaded_file.name
                    st.session_state.pdf_size = uploaded_file.size
                    st.session_state.num_chunks = len(chunks)

                    status.update(label="✅ PDF processed successfully!", state="complete", expanded=False)
                except Exception as e:
                    st.session_state.vector_store = None
                    status.update(label=f"❌ Error processing PDF: {str(e)}", state="error")

        # Display PDF info
        if st.session_state.pdf_name:
            st.divider()
            st.subheader("📄 Document Info")
            st.text(f"Name: {st.session_state.pdf_name}")
            st.text(f"Size: {st.session_state.pdf_size / 1024:.1f} KB")
            st.text(f"Chunks: {st.session_state.num_chunks}")
    else:
        st.info("👆 Upload a PDF to get started")
        # Reset state when no file
        st.session_state.vector_store = None
        st.session_state.pdf_name = None
        st.session_state.pdf_size = None
        st.session_state.num_chunks = None
        st.session_state.chat_history = []

# Main chat interface
st.title("💬 Chat with your PDF")
st.caption("Ask questions about the content of your uploaded PDF")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Show sources if available
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("🔍 View Sources", expanded=False):
                for source in message["sources"]:
                    st.markdown(f"**Page {source['page']}**")
                    st.markdown(f"> {source['content']}")
                    st.divider()

# Chat input
if prompt := st.chat_input("Ask a question about your PDF..."):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    if st.session_state.vector_store is not None:
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    # Get LLM
                    llm = get_llm()

                    # Ask question
                    answer, docs = ask_question(llm, st.session_state.vector_store, prompt)

                    # Format sources
                    sources = []
                    for doc in docs:
                        page = doc.metadata.get("page", "Unknown")
                        sources.append({
                            "page": page,
                            "content": doc.page_content.strip()
                        })

                    # Display answer
                    st.markdown(answer)

                    # Create expandable sources section
                    with st.expander("🔍 View Sources", expanded=False):
                        for source in sources:
                            st.markdown(f"**Page {source['page']}**")
                            st.markdown(f"> {source['content']}")
                            st.divider()

                    # Add to chat history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except Exception as e:
                    st.error(f"❌ Error generating response: {str(e)}")
    else:
        st.warning("⚠️ Please upload a PDF first")

# Developer information (hidden in expander)
with st.sidebar.expander("👨‍💻 Developer Info", expanded=False):
    st.markdown("""
    **Built with:**
    - [Streamlit](https://streamlit.io)
    - [LangChain](https://www.langchain.com)
    - [Ollama](https://ollama.com)
    - [Llama 3.2](https://ai.meta.com/llama/)

    **Features:**
    - Modern ChatGPT-inspired UI
    - Dark theme friendly
    - MMR-based retrieval for better context
    - Source citations with page numbers

    **Version:** 1.0.0
    """)

# Footer
st.divider()
st.caption("💡 Tip: Ask specific questions for better answers. The AI only knows what's in your PDF.")