from langchain_qdrant import QdrantVectorStore
from JinaEmbeddings import JinaEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

# Use the same embedding model used during ingestion
embeddings = JinaEmbeddings(os.getenv("JINA_API_KEY"))

COLLECTION_NAME = "ml_book"

# Connect to existing Qdrant collection (no re-creation)
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    url=os.getenv("QDRANT_ENDPOINT"),
    api_key=os.getenv("QDRANT_API_KEY"),
    collection_name=COLLECTION_NAME
)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})

query = "What is LSTM?"
docs = retriever.invoke(query)

print(type(docs))
print(docs[0])