# ContextOS — Architecture Notes
Last updated: July 4, 2026

## Current Status
Backend (Cognee 1.2.2 + Groq LLM + FastEmbed) is configured and deployed. Streamlit frontend has 3 tabs: Chat, Context Resume, Knowledge Explorer. App live at https://contextos-developer-second-brain.streamlit.app

## WHERE I LEFT OFF (Last Session)
- Switched LLM model from decommissioned `mixtral-8x7b-32768` to `openai/gpt-oss-20b`
- Streamlit Cloud secrets still have old `LLM_MODEL=openai/mixtral-8x7b-32768` — need to update to `openai/gpt-oss-20b`
- Need to verify `remember()` pipeline succeeds with new model (previous models failed to return KnowledgeGraph JSON schema)
- Next immediate task: Update Streamlit Cloud secrets, test the live app

## Key Decisions Made

### Option A: Local Cognee over Cognee Cloud
- Cognee Cloud uses REST API (not open-source `import cognee`) — would disqualify from Open Source track
- Decision: Use `import cognee` library directly, with Groq LLM via OpenAI-compatible endpoint
- Do not revisit unless Open Source track requirement changes

### Groq over OpenAI for LLM
- OpenAI: requires paid API key, slower, rate-limited
- Groq: free tier includes `gpt-oss-20b`, 1000 t/s inference speed
- Downside: Cognee's KnowledgeGraph JSON schema requires OpenAI-compatible function calling — some Groq models fail
- Decision final for now; fallback `openai/gpt-oss-120b` or `qwen/qwen3.6-27b` if `gpt-oss-20b` fails

### FastEmbed over OpenAI Embeddings
- OpenAI embeddings: requires paid API key, network call every time
- FastEmbed: local `all-MiniLM-L6-v2` model (~90MB), no API key, runs offline
- Decision final. Do not revisit.

### Data Directory Override
- Cognee 1.2.2 default data dir is inside `site-packages/` (read-only on Streamlit Cloud)
- Override via `DATA_ROOT_DIRECTORY`, `SYSTEM_ROOT_DIRECTORY`, `CACHE_ROOT_DIRECTORY` env vars → `~/.cognee/`
- Implemented in `brain.py:13-16`

## Open Bugs (Priority Order)
1. CRITICAL: `mixtral-8x7b-32768` decommissioned by Groq; `gpt-oss-20b` may also fail KnowledgeGraph JSON schema. If so, fallback models: `openai/gpt-oss-120b` or `qwen/qwen3.6-27b`
2. HIGH: Streamlit Cloud secrets still reference old model — update needed
3. MEDIUM: API key exposed in chat history — rotate
4. LOW: FastEmbed downloads `all-MiniLM-L6-v2` (~90MB) on first run — may timeout on cold start

## Architecture Stack
- UI: Streamlit 1.58.0
- Memory Engine: Cognee 1.2.2 (graph + vector)
- LLM: Groq API (`openai/gpt-oss-20b`) via OpenAI-compatible SDK
- Embeddings: FastEmbed (`all-MiniLM-L6-v2`, 384d)
- Vector DB: LanceDB
- Graph: NetworkX + RDflib
- Deployment: Streamlit Community Cloud (auto-deploy on push to `main`)
