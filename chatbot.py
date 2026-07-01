from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from query_rewriter import rewrite_query


def get_llm():

    return ChatOllama(
        model="llama3.2",
        temperature=0
    )


def ask_question(llm, vector_store, question):

    # Rewrite the question for better retrieval
    rewritten_question = rewrite_query(question)

    # Better Retriever (MMR)
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 2,
            "fetch_k": 5,
            "lambda_mult": 0.5
        }
    )

    docs = retriever.invoke(rewritten_question)

    # Build Context
    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are an expert AI assistant.

Answer ONLY from the provided context.

Rules:

1. Never make up information.
2. If the answer is not available, say:
   "I could not find the answer in the PDF."
3. You may make simple logical inferences.
4. Keep the answer short unless the user asks for details.
5. If multiple chunks contain useful information, combine them.
6. Mention page number(s) if available.

Context:
{context}

Question:
{question}

Answer:
"""
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    return response.content, docs