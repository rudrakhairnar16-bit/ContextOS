# ContextOS — Developer Second Brain

> *Your codebase has a permanent memory now. Never lose context again.*

[![Hackathon](https://img.shields.io/badge/Hackathon-Hangover%20Part%20AI-7C3AED)](https://www.wemakedevs.org/hackathons/cognee)
[![Built with Cognee](https://img.shields.io/badge/Built%20with-Cognee-4F46E5)](https://cognee.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Test](https://github.com/rudrakhairnar16-bit/ContextOS/actions/workflows/test.yml/badge.svg)](https://github.com/rudrakhairnar16-bit/ContextOS/actions/workflows/test.yml)
[![Live App](https://img.shields.io/badge/Live-Streamlit%20Cloud-FF4B4B)](https://contextos-developer-second-brain.streamlit.app)

> 🎥 **Watch the demo video:** [YouTube Link — Add your video URL here]

**Live app:** [contextos-developer-second-brain.streamlit.app](https://contextos-developer-second-brain.streamlit.app)

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
| **LLM** | Groq API (mixtral-8x7b-32768) via OpenAI-compatible SDK |
| **Embeddings** | FastEmbed (all-MiniLM-L6-v2, 384d) — local, no API key needed |
| **Vector DB** | LanceDB 0.33.0 |
| **Graph** | NetworkX 3.6.1 + RDflib 7.1.4 |

---

## Setup

1. **Clone & set up venv:**
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. **Get your own Cognee Cloud API key** — Sign up at [app.cognee.ai](https://app.cognee.ai) and use hackathon code `COGNEE-35` for free credits.

3. **Configure `.env`:**
```
COGNEE_CLOUD_URL=https://api.cognee.ai/v1
COGNEE_API_KEY=your_cognee_cloud_key_here
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
> `main.py` tests all 4 Cognee operations: `remember()` stores 3 sample memories (decision, bug, note), `recall()` queries the knowledge graph, `improve()` refines it, and `forget()` cleans up.
> **This is the quickest way to verify ContextOS works with your API key.**

Or run unit tests:
```
pip install pytest
pytest tests/ -v
```

---

## Quick Test (No Installation Required)

If the live Streamlit app is down or you want to test offline:

1. **Download** the repo as ZIP or clone it to your desktop
2. **Add your own Cognee Cloud API key** — Sign up at [app.cognee.ai](https://app.cognee.ai) (use hackathon code `COGNEE-35`). Create a `.env` file in the project folder:
```
COGNEE_CLOUD_URL=https://api.cognee.ai/v1
COGNEE_API_KEY=your_cognee_cloud_key_here
ENABLE_BACKEND_ACCESS_CONTROL=false
COGNEE_SKIP_CONNECTION_TEST=true
```
3. **Run this single command** to verify everything works:
```
python main.py
```
> The output walks you through all 4 Cognee operations. If all pass, launch the full UI with:
> ```
> streamlit run app.py
> ```

---

## Deployment

Deployed on **Streamlit Community Cloud**. Auto-deploys on every push to `main`.

[Open Live App](https://contextos-developer-second-brain.streamlit.app)

---

## Notes

- **Hackathon project** — built for The Hangover Part AI Hackathon by WeMakeDevs x Cognee
- **FastEmbed** for local embeddings — no OpenAI embedding API key required
- Uses **Groq** for LLM inference (free tier, mixtral-8x7b-32768)

---

## Built For

**The Hangover Part AI Hackathon** — WeMakeDevs x Cognee
