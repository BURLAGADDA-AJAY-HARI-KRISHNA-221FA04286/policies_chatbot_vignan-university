# 🎓 University Policy Chatbot – Vignan University

A lightweight **RAG (Retrieval-Augmented Generation)** chatbot built using **LangChain**, **FAISS**, and **Google Gemini API**, designed to help students, faculty, and staff easily query university policies, academic regulations, and rules.

---

## 🚀 Features

✅ Uses **Gemini 2.0 Flash** for accurate and fast responses  
✅ **FAISS vector database** for local document retrieval (efficient memory usage)  
✅ **HuggingFace Sentence Transformer** for text embeddings  
✅ Built with **Streamlit** for a beautiful, minimal chat UI  
✅ Lazy loads FAISS and embeddings — runs smoothly even on low-memory servers  
✅ Easy to deploy locally or on Streamlit Cloud  

---

## 🧩 Project Structure

```
university_policy_chatbot/
│
├── app.py                  # Main Streamlit chatbot file
├── ingest.py               # Script to load PDFs/TXT and build FAISS index
├── faiss_index/            # Folder storing FAISS vector store
├── data/                   # Place your .txt or .pdf documents here
├── requirements.txt        # All dependencies
├── .env                    # Contains your Gemini API key
└── README.md               # This file
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/BURLAGADDA-AJAY-HARI-KRISHNA-221FA04286/policies_chatbot_vignan-university.git
cd policies_chatbot_vignan-university
```

### 2️⃣ Create Virtual Environment (Optional but Recommended)
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Add Your Google Gemini API Key
Create a `.env` file in the project root and add:
```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

Get your API key free from 👉 [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

## 🧠 Building the FAISS Index

Before chatting, you must prepare your document database.

1. Place your university policies in the `data/` folder (`.txt` or `.pdf`).
2. Run:
   ```bash
   python ingest.py
   ```
3. This creates a `faiss_index/` folder automatically.

---

## 💬 Run the Chatbot

```bash
python -m streamlit run app.py
```

Then open:  
👉 http://localhost:8501

You’ll see a clean, glowing chat UI like this:

```
👋 Hi there! Ask me anything about university rules or policies.
```

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| LLM | Google Gemini 2.0 Flash |
| Framework | Streamlit |
| Vector DB | FAISS |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| RAG Framework | LangChain |
| Language | Python 3.10+ |

---

## 🌐 Deployment (Optional)

You can easily deploy this chatbot using:

- **Streamlit Cloud** → Easiest  
- **Render** or **Railway** → Lightweight  
- **AWS EC2 or Lightsail** → For full control  

Make sure to:
- Upload your `.env`
- Pre-build your `faiss_index/`
- Set memory limit at least **512 MB**

---

## 👨‍💻 Author

**Burlagadda Ajay Hari Krishna**  
B.Tech CSE Student – Vignan University  
📧 [ajayb@example.com](mailto:ajayb@example.com)

---

## 🪪 License

This project is licensed under the **MIT License** — free to use and modify with attribution.

---

⭐ **If you found this helpful, don’t forget to star the repository!**
