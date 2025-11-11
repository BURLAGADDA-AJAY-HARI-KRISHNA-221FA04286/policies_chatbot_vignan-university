import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
# Note: You need to install google-genai, streamlit, python-dotenv, 
# langchain-community, faiss-cpu, and sentence-transformers.
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


# 🌍 Load API key securely from Streamlit Secrets
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# --- Constants ---
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
FAISS_INDEX_PATH = "faiss_index" # Ensure this directory exists
GEMINI_MODEL = "gemini-2.0-flash"

# ==========================
# 🔑 Initialization
# ==========================
try:
    # Initialize Gemini Client and store it in session state
    if "client" not in st.session_state:
        st.session_state.client = genai.Client(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"❌ Failed to initialize Gemini Client. Check GOOGLE_API_KEY. Error: {e}")
    # Stop the app if the client can't be initialized
    st.stop() 

# ==========================
# 🔹 FAISS + Retriever Loader (Memoized via st.cache_resource)
# ==========================
@st.cache_resource
def load_faiss_retriever():
    """
    Loads the FAISS index and creates a retriever. 
    Uses st.cache_resource to load this expensive object only once.
    """
    try:
        with st.spinner("⚙️ Loading FAISS index and embeddings..."):
            # Load embeddings
            embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
            
            # Load FAISS vector store. 
            vectorstore = FAISS.load_local(
                FAISS_INDEX_PATH, 
                embeddings, 
                # This is necessary when loading a FAISS index created by Langchain
                allow_dangerous_deserialization=True 
            )
            
            # Create retriever with k=5 for top 5 relevant documents
            retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
            return retriever
    except Exception as e:
        # Inform user if the index is missing or corrupted
        st.error(f"❌ Failed to load FAISS index. Ensure '{FAISS_INDEX_PATH}' directory exists. Error: {e}")
        st.stop()
    

# ==========================
# 🔹 Get Relevant Context
# ==========================
def get_relevant_context(query):
    """Fetches relevant documents from the FAISS index."""
    retriever = load_faiss_retriever()
    docs = retriever.invoke(query)
    # The context retrieved contains the text content of the documents
    return "\n\n".join([doc.page_content for doc in docs])


# ==========================
# 🔹 Gemini Answer Generator
# ==========================
def generate_answer(prompt):
    """Generates an answer using the Gemini API."""
    try:
        response = st.session_state.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return response.text 
    except Exception as e:
        return f"❌ Gemini API error: Could not generate content. Details: {e}"


# ==========================
# 🔹 Main RAG Function (Hybrid RAG)
# ==========================
def answer_question(query):
    """Combines context retrieval and answer generation with conditional logic."""
    # 1. Get Context
    context = get_relevant_context(query)
    
    # 2. Build Prompt (The crucial update for handling greetings)
    # This prompt provides conditional instructions to the LLM. 
    prompt = f"""
You are a helpful university assistant named UniBot.
Your primary role is to answer questions about university policies.

---
**INSTRUCTION SET:**
1.  **Policy Questions (High Relevance):** If the 'Context' below contains relevant information, you **MUST** use it to answer the 'Question' factually and clearly. Do not invent facts outside of the context.
2.  **General Questions (Low Relevance/Greetings):** If the 'Context' below is empty, or clearly irrelevant (like a greeting, simple small-talk, or thank you), you are allowed to use your general knowledge to provide a brief, polite, and conversational response.
3.  **No Policy Answer:** If the question is about university policy but the 'Context' is empty or irrelevant, you **MUST** state: "I am sorry, but the current university policy documents do not contain the answer to your question."
---

Context:
{context}

Question:
{query}

Answer:
"""
    # 3. Generate Answer
    return generate_answer(prompt)


# ==========================
# 🌐 Streamlit UI
# ==========================
st.set_page_config(page_title="🎓 University Policy Chatbot", layout="wide")

# Custom CSS for chat look and feel (optional, can use native st.chat_message)
st.markdown(
    """
    <style>
    .user-msg {
        text-align: right;
        background: #0072ff; 
        color: white;
        padding: 10px;
        margin: 8px 0;
        border-radius: 10px 0 10px 10px;
        display: inline-block;
        max-width: 80%;
    }
    .bot-msg {
        text-align: left;
        background: #262730; 
        color: #f5f5f5;
        padding: 10px;
        margin: 8px 0;
        border-radius: 0 10px 10px 10px;
        display: inline-block;
        max-width: 80%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎓 University Policy Chatbot")
st.caption("Ask about university rules, academic policies, and regulations.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "👋 Hi there! Ask me anything about university rules or policies."}
    ]


# --- Display Chat History ---
# Use a fixed-height container for the chat history
chat_container = st.container(height=450, border=True)

with chat_container:
    for msg in st.session_state.messages:
        # Using native st.chat_message is the idiomatic and cleaner way
        with st.chat_message(msg["role"]):
            st.write(msg["content"])


# --- Input Area using st.form ---
# Use a form to group the input and button to handle submission cleaner
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        # Text input inside the form
        query = st.text_input("Type your question:", key="user_input_text", label_visibility="collapsed")
    with col2:
        # Form submission button
        search_clicked = st.form_submit_button("🔍 Send")

# Handle form submission logic
if search_clicked and query.strip():
    # 1. Append User Message to history
    st.session_state.messages.append({"role": "user", "content": query})

    # 2. Get Bot Response
    with st.spinner("💬 Thinking... Retrieving context and generating answer..."):
        answer = answer_question(query)

    # 3. Append Bot Message to history
    st.session_state.messages.append({"role": "bot", "content": answer})

    # 4. Rerun the script to update the display with the new messages
    st.rerun()
