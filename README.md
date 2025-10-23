# 🩺 RAG Local – FastAPI Bridge for Ollama LLM

This repository contains a lightweight **FastAPI bridge** that exposes a local [Ollama](https://ollama.com) model (like `phi3:mini`) over a simple REST API.  
It’s designed for integration with the **AI for Healthcare Emergency Room Simulator** project — allowing the .NET web app to query a locally hosted LLM through HTTP.

---

## 🚀 Features

- FastAPI server with `/health` and `/api/ask` endpoints  
- `.env` configuration for easy setup  
- CORS enabled for local testing and frontend integration  
- Compatible with any small Ollama model (`phi3:mini`, `llama3`, etc.)  
- Works with both localhost and LAN IPs

---

## 🧩 Project Structure

```
rag-local/
│
├── app/
│   └── server.py        # FastAPI app that bridges Ollama and HTTP
│
├── sample_data/
│   └── notes.txt        # Example text for ingest/testing
│
├── .env.example         # Environment variables template
├── requirements.txt     # Dependencies
├── README.md            # Documentation
└── scripts/             # (Optional) For future ingest or RAG utilities
```

---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites
- Python 3.10+  
- Ollama installed and running  
- A pulled model (example):
  ```bash
  ollama pull phi3:mini
  ```

---

### 2️⃣ Local Setup
```bash
# Clone the repo
git clone https://github.com/nadia-sharief/rag-local.git
cd rag-local

# Create env file
cp .env.example .env

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3️⃣ Run the API
```bash
uvicorn app.server:app --host 127.0.0.1 --port 5001 --reload
```

The server will start on:  
👉 **http://127.0.0.1:5001**

---

## 🧠 Endpoints

### ✅ GET `/health`
Check if the API is up and connected to Ollama.
```bash
curl 127.0.0.1:5001/health
```
Response:
```json
{
  "status": "ok",
  "model": "phi3:mini",
  "ollama": "http://127.0.0.1:11434"
}
```

### 💬 POST `/api/ask`
Send a prompt to your local Ollama model and receive the model’s response.
```bash
curl -X POST 127.0.0.1:5001/api/ask -H "Content-Type: application/json" -d '{"q": "Hello"}'
```
Response:
```json
{
  "answer": "Hello! How can I help you today?",
  "model": "phi3:mini"
}
```

---

## 🌐 LAN / Remote Access (Optional)

To allow another teammate (e.g., Hayden) to connect:

1️⃣ Get your local IP:
```bash
hostname -I
```

2️⃣ Edit your `.env`:
```
OLLAMA_BASE=http://<YOUR_LAN_IP>:11434
RAG_PORT=5001
```

3️⃣ Run:
```bash
uvicorn app.server:app --host 0.0.0.0 --port 5001 --reload
```

Then teammates can reach your server at:  
👉 **http://<YOUR_LAN_IP>:5001/api/ask**

---

## 🤝 Integration Example (.NET Web App)

Example POST request from Hayden’s .NET app:
```json
POST http://192.168.1.67:11434/api/generate
{
  "model": "phi3:mini",
  "prompt": "<your message>",
  "stream": false
}
```
Your FastAPI bridge handles forwarding and returning the LLM response.

---

## 🧑‍💻 Maintainer

**Nadia Sharief**  
University of Arizona – AI for Healthcare Project  
📧 Nadiasharief@arizona.edu  

---

## 🩵 Credits

- [Ollama](https://ollama.com)  
- [FastAPI](https://fastapi.tiangolo.com)  
- University of Arizona – AI for Healthcare Capstone Team

