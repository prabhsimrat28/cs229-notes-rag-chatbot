from langchain_community.document_loaders import PyPDFLoader
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from JinaEmbeddings import JinaEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()


loader=PyPDFLoader("../data/FULL_DOCUMENT.pdf")
docs=loader.load()

splitter=RecursiveCharacterTextSplitter(chunk_size=700,chunk_overlap=100)
chunks=splitter.split_documents(docs)
print(f"Total chunks: {len(chunks)}")



embeddings = JinaEmbeddings(api_key=os.getenv("JINA_API_KEY"))

# ======================== 3. CONNECT TO QDRANT ========================


COLLECTION_NAME = "ml_book"
VECTOR_SIZE = 768  # jina-embeddings-v5-nano default dimension

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    url=os.getenv("QDRANT_ENDPOINT"),
    api_key=os.getenv("QDRANT_API_KEY"),
    collection_name=COLLECTION_NAME
)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})

docs = retriever.invoke("What is supervised learning?")

