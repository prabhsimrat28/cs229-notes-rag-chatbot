from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from qdrant_store import qdrant_store
from dotenv import load_dotenv

load_dotenv()


llm = ChatOpenAI(
    model="openai/gpt-oss-20b:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7
)


def enriched_query(state):
    prompt=PromptTemplate(
        input_variables=["query"],
        template="""
Rewrite the user's question to improve semantic retrieval.

Rules:
- Preserve the original intent.
- Do NOT answer the question.
- Do NOT add unrelated concepts.
- Return only the rewritten query.

Question:
{query}
"""
    )

    formatted_query=prompt.format(query=state['query'])

    response=llm.invoke(formatted_query).content
    return {'enriched_query':response}


def top_results(state):
    retreiver=qdrant_store()
    query=state['enriched_query']
    docs=retreiver.invoke(query)
    return {'top_results':[doc.page_content for doc in docs]}

def final_stream_result(state):
    prompt=PromptTemplate(
        input_variables=["question","context"],
        template="""
You are an expert AI assistant.

Answer the user's question using ONLY the information provided in the context below.

Instructions:
- Use the retrieved context as the primary source.
- If the answer is fully supported by the context, answer clearly and completely.
- If the context only partially answers the question, say what is supported and mention what is missing.
- If the answer cannot be found in the context, reply:
  "I couldn't find enough information in the provided documents to answer this question."
- Do not make up facts or use outside knowledge.
- Keep the answer well-structured and easy to read.

Context:
{context}

Question:
{question}

Answer:
"""
)
    context_str = "\n\n---\n\n".join(state['top_results'])
    prompt=prompt.format(context=context_str,question=state['enriched_query'])
    for chunk in llm.stream(prompt):
        if chunk.content:
            yield chunk.content


def final_result(state):
    prompt=PromptTemplate(
        input_variables=["question","context"],
        template="""
You are an expert AI assistant.

Answer the user's question using ONLY the information provided in the context below.

Instructions:
- Use the retrieved context as the primary source.
- If the answer is fully supported by the context, answer clearly and completely.
- If the context only partially answers the question, say what is supported and mention what is missing.
- If the answer cannot be found in the context, reply:
  "I couldn't find enough information in the provided documents to answer this question."
- Do not make up facts or use outside knowledge.
- Keep the answer well-structured and easy to read.

Context:
{context}

Question:
{question}

Answer:
"""
)
    context_str = "\n\n---\n\n".join(state['top_results'])
    prompt=prompt.format(context=context_str,question=state['enriched_query'])
    response=llm.invoke(prompt)
    return {'final_result':response.content}