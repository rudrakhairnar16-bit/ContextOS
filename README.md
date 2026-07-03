# ContextOS — Developer Second Brain

> *Your codebase has a permanent memory now. Never lose context again.*

A **hackathon project** built for *The Hangover Part AI Hackathon* by WeMakeDevs x Cognee. ContextOS solves the problem of losing mental context when returning to a codebase after a break (e.g., Monday morning after Friday's close). It acts as a **persistent memory layer** — ingesting code files, architecture decisions, bugs, and developer notes, then letting you query everything via natural language through Cognee's hybrid graph-vector knowledge store.

---

## Features

| Feature | Description |
|---|---|
| **Feed Your Brain** | Ingest code files (`.py`, `.js`, `.ts`, `.md`, `.txt`, `.json`, `.yaml`, `.html`, `.css`), developer notes, architecture decisions, and bug reports via the sidebar |
| **Ask Your Brain** | Natural language chat interface with history — queries Cognee's graph+vector memory |
| **Context Resume** | One-click restore of last session's context with suggested next actions |
| **Knowledge Explorer** | Concept search with visual entity graphs and relationships |
| **4 Core Cognee Ops** | `remember()` (store), `recall()` (query), `improve()` (refine), `forget()` (clear) — all wired through the UI |

---

## Architecture

```
Streamlit UI (app.py)
    |
    v
brain.py --- async-to-sync Cognee adapter
    |
    v
Cognee --- hybrid graph-vector knowledge store
    |
    v
LanceDB (vector DB) + NetworkX (graph)
```

### Key Files

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit UI (627 LOC) — 3 tabs, sidebar ingestion, chat, context resume, explorer |
| `brain.py` | Cognee adapter — wraps async Cognee ops for Streamlit compatibility (96 LOC) |
| `ingest.py` | Formats files, decisions, bugs, and notes for Cognee storage (47 LOC) |
| `main.py` | Backend test harness — validates all 4 Cognee operations (104 LOC) |
| `auth.py` | OAuth2 auth stubs (architectural example, not live) |
| `temp_auth.py` | Backup auth variant |
| `database.js` | Redis + MongoDB architectural example stubs |
| `architecture_notes.md` | Dev notebook — bugs, decisions, where left off |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **UI** | Streamlit 1.58.0 |
| **Memory Engine** | Cognee 1.2.2 (graph + vector) |
| **LLM** | Groq API (llama-3.1-8b-instant) via OpenAI-compatible SDK |
| **Embeddings** | FastEmbed (all-MiniLM-L6-v2, 384d) |
| **Vector DB** | LanceDB 0.33.0 |
| **Graph** | NetworkX 3.6.1 + RDflib 7.1.4 |
| **Structured Output** | Instructor 1.15.1 |
| **Planned** | Redis (cache), MongoDB (prefs), PostgreSQL (auth / FastAPI Users) |

---

## Setup

1. **Clone & set up venv:**
```
python -m venv venv
venv\Scripts\activate
pip install streamlit cognee python-dotenv openai
```

2. **Get your own API key** — Sign up at [console.groq.com](https://console.groq.com) and create a free API key.

3. **Configure `.env`:** (required — use your own API key, not the one from the repo)
```
GROQ_API_KEY=gsk_your_own_key_here
LLM_API_KEY=gsk_your_own_key_here
LLM_PROVIDER=openai
LLM_ENDPOINT=https://api.groq.com/openai/v1
LLM_MODEL=openai/llama-3.1-8b-instant
ENABLE_BACKEND_ACCESS_CONTROL=false
COGNEE_SKIP_CONNECTION_TEST=true
```

4. **Run:**
```
streamlit run app.py
```

---

## Testing

```
python main.py
```

---

## Notes

- **Hackathon quality** — built for submission, not production
- **No `requirements.txt`** — dependencies installed directly into `venv/`
- **Auth stubs** — `auth.py` and `database.js` are architectural examples, not functional
- **Single git commit** — `fab1eed` ("ContextOS: Developer Second Brain -- Hackathon Submission")

---

## Built For

**The Hangover Part AI Hackathon** — WeMakeDevs x Cognee
