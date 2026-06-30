from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


def get_llm():

    return ChatOllama(
        model="llama3.2",
        temperature=0
    )


def ask_question(llm, vector_store, question):

    # Better Retrieval using MMR
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 20
        }
    )

    docs = retriever.invoke(question)

    # Create Context
    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful AI assistant.

Answer ONLY using the provided context.

You may make simple logical inferences.

Example:

Context:
My Name Is Balveer Singh Meena.
I Am From Sikar, Rajasthan.

Question:
Where do I live?

Answer:
You are from Sikar, Rajasthan.

If the answer cannot be found from the context,
reply only:

"I could not find the answer in the PDF."

Context:
{context}

Question:
{question}
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