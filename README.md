# Machine Learning Notes RAG Application

An advanced Retrieval-Augmented Generation (RAG) system built to answer questions based on Stanford machine learning notes. The application leverages a modern AI stack to process document chunks, generate high-quality semantic embeddings, and synthesize accurate answers from a language model, all served through a real-time streaming web interface.

## Architecture and Service Integration

The project is designed with a microservices-oriented approach, ensuring modularity and clean separation of concerns. The distinct services work together seamlessly to form the complete RAG pipeline:

1. **Document Processing and Ingestion**
   Raw PDF documents are parsed using PyPDFLoader and split into optimized semantic chunks using a recursive character text splitter. 
   
2. **Vector Database (Qdrant)**
   The chunked documents are processed by Jina Embeddings via a custom integration. These high-dimensional vectors are upserted into a Qdrant Cloud vector database. Qdrant handles efficient similarity search to retrieve the most relevant context for any given user query.

3. **Agentic Workflow (LangGraph)**
   The core reasoning engine is built with LangGraph. It defines a stateful graph that takes a user query, reformulates it for better semantic retrieval, fetches top results from Qdrant, and finally prompts an advanced Large Language Model (accessed via OpenRouter) to generate a concise, context-aware answer.

4. **Backend API (FastAPI)**
   A FastAPI server exposes the LangGraph workflow as REST endpoints. It handles concurrent requests and provides a streaming response endpoint (`/stream`) to deliver the language model's output in real time.

5. **Frontend UI (Streamlit)**
   The user interface is built with Streamlit. It communicates with the FastAPI backend over HTTP, rendering the streamed text tokens as they arrive to provide a responsive and interactive user experience.

## Project Structure

The repository is cleanly divided into specific modules to maintain a professional, production-ready codebase:

* `Book_RAG_routes/`: Contains the data ingestion scripts, including document splitting, embedding generation using the custom JinaEmbeddings class, and Qdrant database population.
* `chains/`: Houses the LangGraph workflow (`book_chain.py`), defining the state graph, prompt templates, and the language model reasoning logic.
* `qdrant_store.py`: A utility module for establishing connections to the Qdrant Cloud vector store and instantiating the retriever.
* `app.py`: The FastAPI application entry point, defining the API routes and integrating the LangGraph inference chain.
* `frontend.py`: The Streamlit web application that serves as the client-side user interface.

## Application Interface

![Application Screenshot Placeholder](images/Screenshot%202026-07-31%20193156.png.png)

## Installation and Usage

### Prerequisites
* Python 3.10+
* API Keys for OpenRouter, Jina AI, and Qdrant Cloud

### Setup
1. Clone the repository and navigate to the project directory.
2. Install the necessary dependencies (ensure you install both backend and frontend requirements).
3. Create a `.env` file in the root directory containing your specific environment configurations:
   * `OPENROUTER_API_KEY`
   * `JINA_API_KEY`
   * `QDRANT_ENDPOINT`
   * `QDRANT_API_KEY`

### Running the Application
1. Start the FastAPI backend server:
   ```bash
   uvicorn app:app --reload
   ```
2. In a separate terminal, launch the Streamlit frontend:
   ```bash
   streamlit run frontend.py
   ```
