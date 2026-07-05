# ContextOS — Developer Second Brain

> *Your codebase has a permanent memory now. Never lose context again.*

[![Hackathon](https://img.shields.io/badge/Hackathon-Hangover%20Part%20AI-7C3AED)](https://www.wemakedevs.org/hackathons/cognee)
[![Built with Cognee](https://img.shields.io/badge/Built%20with-Cognee-4F46E5)](https://cognee.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Test](https://github.com/rudrakhairnar16-bit/ContextOS/actions/workflows/test.yml/badge.svg)](https://github.com/rudrakhairnar16-bit/ContextOS/actions/workflows/test.yml)
[![Live App](https://img.shields.io/badge/Live-Streamlit%20Cloud-FF4B4B)](https://contextos-developer-second-brain.streamlit.app)

---

## Links

| | |
|---|---|
| 🎥 **Demo Video** | [YouTube](https://youtu.be/KXRg5jHmO4M) |
| 📝 **Blog Post** | [Hashnode](https://contextos-second-brain-for-developer.hashnode.dev/contextos-second-brain-for-developer-the-hangover-part-ai-hackathon) |
| 💼 **LinkedIn** | [Rudra Khaire](https://www.linkedin.com/in/rudra-khaire-2657a5381) |
| 🐙 **GitHub** | [rudrakhairnar16-bit/ContextOS](https://github.com/rudrakhairnar16-bit/ContextOS) |
| 🌐 **Live App** | [contextos-developer-second-brain.streamlit.app](https://contextos-developer-second-brain.streamlit.app) |

---

## Screenshots

| Chat | Context Resume | Knowledge Explorer |
|---|---|---|
| ![Chat tab](assets/screenshot1.png) | ![Context Resume tab](assets/screenshot2.png) | ![Knowledge Explorer tab](assets/screenshot3.png) |

---

## The Problem

It's Monday morning. You closed your laptop Friday with Redis half-configured, a JWT bug mid-debug, and 3 architecture decisions pending. ChatGPT doesn't remember any of it. Your team's Notion is outdated.

**ContextOS remembers everything. One click brings it back.**

---

## Features

| Feature | Description |
|---|---|
| **Feed Your Brain** | Ingest code files, developer notes, architecture decisions, and bugs via the sidebar |
| **Ask Your Brain** | Natural language chat — queries Cognee's hybrid graph+vector memory |
| **Context Resume** | One-click restore of last session with suggested next actions |
| **Export Context** | Copy your full context to Claude, Cursor, or any AI coding tool |
| **Knowledge Explorer** | Concept search with visual entity relationship maps |
| **4 Core Cognee Ops** | `remember()`, `recall()`, `improve()`, `forget()` — all wired through the UI |

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
| `app.py` | Main Streamlit UI — 3 tabs, sidebar ingestion, chat, context resume, explorer |
| `brain.py` | Cognee adapter — async-to-sync bridge with config fallbacks |
| `ingest.py` | Data ingestion helpers (files, decisions, bugs, notes) |
| `main.py` | Backend test harness for all 4 Cognee operations |
| `tests/test_brain.py` | Unit tests for core brain functions |
| `architecture_notes.md` | Dev notebook — bugs, decisions, where left off |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **UI** | Streamlit 1.58.0 |
| **Memory Engine** | Cognee 1.2.2 (graph + vector) |
| **LLM** | Groq — llama-3.1-8b-instant via OpenAI-compatible SDK |
| **Embeddings** | FastEmbed (all-MiniLM-L6-v2, 384d) — local, no API key needed |
| **Vector DB** | LanceDB 0.33.0 |
| **Graph** | NetworkX 3.6.1 + RDflib 7.1.4 |

---

## How Cognee Is Used

ContextOS deeply integrates all four Cognee memory lifecycle APIs:

- **`remember()`** — Ingests code files, text notes, architecture decisions, and bug reports into Cognee's hybrid graph+vector knowledge store. Each data type is classified and stored with metadata tags.
- **`recall()`** — Powers the chat interface. User queries are routed through Cognee's semantic search and graph traversal to return contextually relevant answers.
- **`improve()`** — Runs automatically after every 5 ingests to enrich the knowledge graph, prune stale nodes, and adapt weights.
- **`forget()`** — Available via the UI to surgically delete specific datasets or memories.

The app also leverages Cognee's pipeline system: `classify_documents`, `extract_chunks_from_documents`, and `extract_graph_and_summarize`.

---

## Setup

1. **Clone & set up venv:**
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. **Get a Groq API key** — Sign up at [console.groq.com](https://console.groq.com) (free tier).

3. **Configure `.env`:**
```
GROQ_API_KEY=gsk_your_groq_api_key_here
LLM_API_KEY=gsk_your_groq_api_key_here
LLM_PROVIDER=openai
LLM_ENDPOINT=https://api.groq.com/openai/v1
LLM_MODEL=openai/llama-3.1-8b-instant
EMBEDDING_PROVIDER=fastembed
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSIONS=384
ENABLE_BACKEND_ACCESS_CONTROL=false
COGNEE_SKIP_CONNECTION_TEST=true
```
> ⚠️ Never commit your `.env` file. The `.gitignore` already excludes it.

4. **Run:**
```
streamlit run app.py
```

---

## Testing

Run the backend test harness:
```
python main.py
```

> ✅ If you see **"ALL 4 COGNEE OPERATIONS VERIFIED!"** the backend is working.

Or run unit tests:
```
pip install pytest
pytest tests/ -v
```

---

## Deployment

Deployed on **Streamlit Community Cloud**. Auto-deploys on every push to `main`.

[Open Live App](https://contextos-developer-second-brain.streamlit.app)

---

## Built For

**The Hangover Part AI Hackathon** — WeMakeDevs x Cognee

*Built solo by Rudra Keyur Khaire. Developed with Claude, Gemini, and OpeCode (declared as per Rule 8). YouTube video edited by Hetu.*
