import os
from google import genai
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=GOOGLE_API_KEY)

# Lazy-loaded global variables
embeddings = None
vectorstore = None
retriever = None


def load_faiss():
    """Load FAISS index and embeddings only when needed."""
    global embeddings, vectorstore, retriever
    if retriever is None:
        print("⚙️ Loading FAISS index and embeddings...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    return retriever


def get_relevant_context(query):
    """Retrieve relevant text chunks using FAISS retriever."""
    retriever = load_faiss()  # Load lazily
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])


def generate_answer(prompt):
    """Generate content using Gemini API."""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text if hasattr(response, "text") else str(response)
    except Exception as e:
        return f"❌ Gemini API error: {e}"


def answer_question(query):
    """Pipeline to get context and generate a final answer."""
    print("🧠 Retrieving context...")
    context = get_relevant_context(query)

    prompt = f"""
You are a helpful university assistant.
Use the context below to answer accurately.

Context:
{context}

Question:
{query}

Answer:
"""
    return generate_answer(prompt)


if __name__ == "__main__":
    print("\n🎓 University RAG Chatbot is ready! Type your question below:\n")
    while True:
        question = input("> ").strip()
        if question.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        try:
            answer = answer_question(question)
            print("\n" + answer + "\n")
        except Exception as e:
            print(f"\n❌ An error occurred during processing: {e}\n")
