from JinaEmbeddings import JinaEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()
embeddings = JinaEmbeddings(os.getenv("JINA_API_KEY"))

query_vector = embeddings.embed_query("What is machine learning?")

doc_vectors = embeddings.embed_documents([
    "This is chunk 1",
    "This is chunk 2",
])

print(doc_vectors)