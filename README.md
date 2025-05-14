# La Rosalina Resort Assistant 👋🛎️

This project is a fully bilingual (English & Spanish) assistant that demonstrates how a **LangGraph agent** can combine Retrieval‑Augmented Generation with live tool calls against an existing hotel‑management backend.
The chatbot can explain services, amenities, check‑in policies, and – crucially – perform **real‑time room‑availability checks** by hitting the Booking REST API I had built previously (Swagger docs: [http://sdtsoftware-001-site14.atempurl.com/swagger](http://sdtsoftware-001-site14.atempurl.com/swagger)).
All reasoning, retrieval, and tool‑use steps are orchestrated inside a single stateful LangGraph workflow.

## 🌐 Public demo

A public demo is running on **Streamlit Community Cloud**:

**Live URL:** [https://larosalinaresort.streamlit.app/](https://larosalinaresort.streamlit.app/)

Feel free to try the quick‑suggestion buttons or ask any question about the hotel in either English or Spanish.

---

## ✨ Features

| Capability                     | Tech behind it                                               |
| ------------------------------ | ------------------------------------------------------------ |
| Conversational UI              | **Streamlit** `st.chat_*`                                    |
| Routing & orchestration        | **LangGraph** (`StateGraph`)                                 |
| Retrieval‑Augmented Generation | **Pinecone** vector DB + OpenAI embeddings                   |
| Live availability check        | Internal **Booking REST API** (tool use)                     |
| Parallel tool execution        | `RunnableParallel` → `both_node`                             |
| Language auto‑detection        | `langdetect`, forces answer in user language                 |
| Observability                  | **LangSmith** tracing (toggle with `LANGSMITH_TRACING=true`) |

---

## 🖇️ Agent architecture & LangGraph flow

The core of this project is a **LangGraph agent** — an autonomous workflow that decides which tool(s) to call, gathers knowledge, and synthesises the final answer. The agent orchestrates four nodes:

```text
┌───────────────┐
│   router_node │  (LLM decides: info / availability / both / end)
└──────┬────────┘
       │ conditional edges
       │           
┌──────┴──────┐      ┌──────────────────┐
│ info_node   │      │ availability_node│
│ (RAG over   │      │ (LLM → Booking   │
│  Pinecone)  │      │  API wrapper)    │
└──────┬──────┘      └──────────┬───────┘
       │                         │
       │         ▽ parallel      │
       └─────────► both_node ◄───┘  (runs the two above in parallel and merges results)
                     │
                     ▼
            ┌────────────────┐
            │ response_node  │  (LLM crafts final answer in the user's language)
            └────────────────┘
```

### End‑to‑end flow

1. **Streamlit** displays the chat UI and captures the user’s message.
2. The message, plus an empty `GraphState`, is sent to **`graph_runnable.invoke()`**.
3. The **router node** uses GPT‑4 to decide which branch(es) to execute:

   * `info_node` → retrieves docs from the Pinecone index (RAG).
   * `availability_node` → calls the hotel **Booking API** you built previously.
   * `both_node` → runs both in parallel and merges.
4. **response\_node** receives the enriched state (history, documents, availability) and
   returns the final text.
5. Streamlit streams the reply, stores both turns in `InMemoryChatMessageHistory`, and reruns the app so the chat input re‑appears.

> **Why LangGraph?** Unlike vanilla LangChain chains, a **LangGraph agent** persists state between nodes, offers first‑class branching & parallel execution, and integrates perfectly with LangSmith tracing.

---

## 🗂️ Directory structure

```text
src/
 ├ app/               # Streamlit frontend
 │   └─ main.py
 ├ agents/            # LangGraph orchestration
 │   ├─ graph.py
 │   ├─ state.py
 │   ├─ utils/merge.py
 │   └─ nodes/
 │       ├─ router_node.py
 │       ├─ info_node.py
 │       ├─ availability_node.py
 │       └─ response_node.py
 ├ services/          # Wrapper for Booking API
 └ config/            # settings.py (reads env vars)
tests/                # pytest cases
requirements.txt
Dockerfile            # local docker build (Streamlit Cloud ignores this)
```

---

## 🚀 Quick start (local)

```bash
# 1. clone repo
git clone https://github.com/ezequielsirne/LangGraph-Agent-API.git
cd LangGraph-Agent-API

# 2. create venv & install deps
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. set environment variables
cp .env.example .env               # fill with your keys, or export manually
export $(grep -v ^# .env | xargs)  # Linux/macOS only

# 4. run streamlit
streamlit run src/app/main.py
```

Open [http://localhost:8501](http://localhost:8501) ➜ chat with the assistant.

---

## 🐳 Run with Docker

```bash
docker build -t larosalina:latest .
docker run --env-file .env -p 8501:8501 larosalina:latest
```

## ⚙️ Required environment variables

Create `.env` (or use Streamlit Cloud “Secrets”) in **TOML** format:

```toml
# OpenAI
OPENAI_API_KEY = "sk-..."
MODEL          = "gpt-4.1-nano"

# Pinecone
PINECONE_API_KEY     = "pcsk_..."
PINECONE_ENVIRONMENT = "us-east-1"
PINECONE_INDEX_NAME  = "langgraph-agent-api"

# LangSmith (optional)
LANGSMITH_TRACING  = true
LANGSMITH_ENDPOINT = "https://api.smith.langchain.com"
LANGSMITH_API_KEY  = "lsv2_..."
LANGSMITH_PROJECT  = "langgraph-agent-api"

# Booking API
BOOKING_API_URL  = "http://sdtsoftware-001-site14.atempurl.com"
BOOKING_API_USER = "admin"
BOOKING_API_PASS = "admin"
```

---

## 🛠️ Development tips

* **Hot‑reload**: Streamlit auto‑reloads on file save.
* **Vector index**: First run creates the Pinecone index if it doesn't exist.
* **Testing**: `pytest -q` runs unit tests for nodes and utils.
* **Tracing**: Set `LANGSMITH_TRACING=true` to record every LangGraph run.

---

## 📄 License

MIT © 2025 — Ezequiel Sirne
Feel free to fork, adapt, and improve! PRs & issues welcome.
