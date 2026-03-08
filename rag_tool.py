from vector_store import load_vectorstore
from langchain.tools import tool

vectorstore = load_vectorstore()

@tool
def fitness_rag(query: str) -> str:
    """Retrieve relevant fitness information from the vector database."""

    retriever = vectorstore.as_retriever()

    docs = retriever.invoke(query)

    context = "\n".join([doc.page_content for doc in docs])

    return context