from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from app import answer_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>🎓 University Assistant</title>
            <style>
                body {
                    margin: 0;
                    height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: linear-gradient(135deg, #0a0a0a, #1b1b1b, #222);
                    font-family: 'Poppins', sans-serif;
                    color: #f5f5f5;
                    overflow: hidden;
                }

                #chat-container {
                    width: 90%;
                    max-width: 750px;
                    height: 85vh;
                    display: flex;
                    flex-direction: column;
                    border-radius: 20px;
                    background: rgba(255, 255, 255, 0.07);
                    backdrop-filter: blur(15px);
                    box-shadow: 0 0 40px rgba(0, 255, 255, 0.25);
                    overflow: hidden;
                    animation: fadeIn 0.8s ease;
                }

                #header {
                    background: linear-gradient(90deg, #007bff, #00c6ff);
                    color: white;
                    text-align: center;
                    padding: 15px;
                    font-size: 22px;
                    font-weight: bold;
                    letter-spacing: 0.5px;
                    text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
                }

                #chat-box {
                    flex: 1;
                    padding: 20px;
                    overflow-y: auto;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }

                .message {
                    max-width: 80%;
                    padding: 14px 18px;
                    border-radius: 14px;
                    line-height: 1.5;
                    animation: slideUp 0.3s ease;
                }

                .user {
                    align-self: flex-end;
                    background: linear-gradient(135deg, #0072ff, #00c6ff);
                    color: white;
                    border-bottom-right-radius: 5px;
                    box-shadow: 0 0 15px rgba(0, 114, 255, 0.4);
                }

                .bot {
                    align-self: flex-start;
                    background: rgba(255, 255, 255, 0.08);
                    color: #e4e4e4;
                    border-bottom-left-radius: 5px;
                    box-shadow: 0 0 10px rgba(0, 255, 255, 0.25);
                    animation: glow 3s infinite ease-in-out alternate;
                }

                .bot p {
                    margin: 6px 0;
                }

                .bot ul {
                    list-style-type: none;
                    padding-left: 10px;
                }

                .bot li::before {
                    content: "• ";
                    color: #00c6ff;
                    font-weight: bold;
                }

                #input-area {
                    display: flex;
                    align-items: center;
                    padding: 15px;
                    background: rgba(255, 255, 255, 0.06);
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
                }

                #query {
                    flex: 1;
                    padding: 12px 18px;
                    background: rgba(255, 255, 255, 0.12);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 10px;
                    font-size: 15px;
                    outline: none;
                    transition: 0.3s;
                }

                #query:focus {
                    border-color: #00c6ff;
                    box-shadow: 0 0 10px rgba(0, 198, 255, 0.3);
                }

                #send-btn {
                    margin-left: 10px;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 10px;
                    font-size: 15px;
                    background: linear-gradient(135deg, #00c6ff, #0072ff);
                    color: white;
                    cursor: pointer;
                    transition: 0.3s;
                    box-shadow: 0 0 20px rgba(0, 198, 255, 0.3);
                }

                #send-btn:hover {
                    background: linear-gradient(135deg, #0072ff, #00c6ff);
                    transform: scale(1.05);
                }

                @keyframes slideUp {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }

                @keyframes fadeIn {
                    from { opacity: 0; transform: scale(0.95); }
                    to { opacity: 1; transform: scale(1); }
                }

                @keyframes glow {
                    from { box-shadow: 0 0 10px rgba(0, 255, 255, 0.2); }
                    to { box-shadow: 0 0 25px rgba(0, 255, 255, 0.4); }
                }

                ::-webkit-scrollbar {
                    width: 8px;
                }

                ::-webkit-scrollbar-thumb {
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 10px;
                }
            </style>
        </head>

        <body>
            <div id="chat-container">
                <div id="header">🎓 University Policy Chatbot</div>
                <div id="chat-box">
                    <div class="message bot">👋 Hi there! Ask me about university rules, holidays, or academic policies.</div>
                </div>
                <div id="input-area">
                    <input type="text" id="query" placeholder="Type your question..." onkeydown="if(event.key==='Enter') ask()" />
                    <button id="send-btn" onclick="ask()">Send</button>
                </div>
            </div>

            <script>
                function cleanText(text) {
                    // Remove markdown stars and extra spaces
                    text = text.replace(/\\*\\*/g, "");
                    text = text.replace(/\\*/g, "");
                    text = text.replace(/\\n{2,}/g, "\\n").trim();

                    // Split by newlines into paragraphs
                    const parts = text.split(/\\n/).filter(line => line.trim());
                    let formatted = "";

                    parts.forEach(line => {
                        if (line.match(/^[\\-•\\d]+\\.?\\s/)) {
                            if (!formatted.includes("<ul>")) formatted += "<ul>";
                            formatted += `<li>${line.replace(/^[\\-•\\d]+\\.?\\s/, "")}</li>`;
                        } else {
                            if (formatted.endsWith("</ul>")) formatted += "";
                            formatted += `<p>${line}</p>`;
                        }
                    });

                    if (formatted.includes("<li>")) formatted += "</ul>";
                    return formatted;
                }

                async function ask() {
                    const input = document.getElementById("query");
                    const chatBox = document.getElementById("chat-box");
                    const query = input.value.trim();
                    if (!query) return;

                    const userMsg = document.createElement("div");
                    userMsg.className = "message user";
                    userMsg.textContent = query;
                    chatBox.appendChild(userMsg);
                    input.value = "";

                    const botTyping = document.createElement("div");
                    botTyping.className = "message bot";
                    botTyping.textContent = "💬 Thinking...";
                    chatBox.appendChild(botTyping);
                    chatBox.scrollTop = chatBox.scrollHeight;

                    try {
                        const res = await fetch("/ask", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ query })
                        });
                        const data = await res.json();
                        botTyping.remove();

                        const botMsg = document.createElement("div");
                        botMsg.className = "message bot";
                        botMsg.innerHTML = cleanText(data.answer || "❌ No response.");
                        chatBox.appendChild(botMsg);
                        chatBox.scrollTop = chatBox.scrollHeight;
                    } catch (err) {
                        botTyping.remove();
                        const errMsg = document.createElement("div");
                        errMsg.className = "message bot";
                        errMsg.textContent = "⚠️ Server error.";
                        chatBox.appendChild(errMsg);
                    }
                }
            </script>
        </body>
    </html>
    """

@app.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
        query = data.get("query", "")
        answer = answer_question(query)
        return JSONResponse({"answer": answer})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

