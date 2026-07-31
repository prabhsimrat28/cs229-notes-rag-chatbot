import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/stream"

st.set_page_config(
    page_title="Stanford CS231n RAG Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Stanford CS231n Notes RAG Chatbot")
st.write("Ask any question about the Stanford CS231n notes.")

query = st.text_area(
    "Your Question",
    height=120,
    placeholder="Example: Explain what a GRU is."
)

if st.button("Ask", type="primary"):

    if not query.strip():
        st.warning("Please enter a question.")
        st.stop()

    try:
        response = requests.post(
            API_URL,
            json={"text": query},
            stream=True,
        )

        if response.status_code != 200:
            st.error(f"API Error: {response.status_code}")
            st.stop()

        st.subheader("Answer")

        placeholder = st.empty()
        answer = ""

        for chunk in response.iter_content(
            chunk_size=None,
            decode_unicode=True,
        ):
            if chunk:
                answer += chunk
                placeholder.markdown(answer + "▌")

        placeholder.markdown(answer)

    except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to the FastAPI server.\n\n"
            "Make sure it is running on http://127.0.0.1:8000"
        )

    except Exception as e:
        st.error(str(e))