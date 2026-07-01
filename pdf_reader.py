from langchain_core.documents import Document
from pypdf import PdfReader


def extract_documents(pdf_file):

    reader = PdfReader(pdf_file)

    documents = []

    for page_number, page in enumerate(reader.pages):

        page_text = page.extract_text()

        if page_text:

            documents.append(
                Document(
                    page_content=page_text,
                    metadata={
                        "page": page_number + 1
                    }
                )
            )

    return documents