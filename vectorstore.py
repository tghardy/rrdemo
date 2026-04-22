from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

def create_vector_db(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=400
    )

    chunks = text_splitter.split_documents(data)

    embeddings= OllamaEmbeddings(
        model="mxbai-embed-large"
    )

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    print(f"Vector database created with {len(chunks)} chunks.")
    return vector_db

mydb = create_vector_db("./regression.pdf")
mydb = mydb.as_retriever()