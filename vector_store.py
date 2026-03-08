import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()


VECTOR_PATH = "faiss_index"


def create_vectorstore():

    docs = []
    folder = "documents"

    for file in os.listdir(folder):
        loader = TextLoader(os.path.join(folder, file))
        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    splits = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(splits, embeddings)

    vectorstore.save_local(VECTOR_PATH)

    return vectorstore


def load_vectorstore():

    embeddings = OpenAIEmbeddings()

    if os.path.exists(VECTOR_PATH):
        return FAISS.load_local(
            VECTOR_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

    return create_vectorstore()