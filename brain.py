import os

os.environ["ENABLE_BACKEND_ACCESS_CONTROL"] = "false"
os.environ["COGNEE_SKIP_CONNECTION_TEST"] = "true"

import asyncio
from typing import Any, List
from dotenv import load_dotenv

load_dotenv()

# ---- Data Directory (writable location) ----
cognee_root = os.path.join(os.environ.get("HOME", "/tmp"), ".cognee")
os.environ.setdefault("DATA_ROOT_DIRECTORY", os.path.join(cognee_root, "data"))
os.environ.setdefault("SYSTEM_ROOT_DIRECTORY", os.path.join(cognee_root, "system"))
os.environ.setdefault("CACHE_ROOT_DIRECTORY", os.path.join(cognee_root, "cache"))

# ---- LLM Configuration (Groq via OpenAI-compatible API) ----
if not os.getenv("LLM_API_KEY"):
    os.environ["LLM_API_KEY"] = os.getenv("GROQ_API_KEY", "")
if os.getenv("LLM_PROVIDER", "").lower() == "groq":
    os.environ["LLM_PROVIDER"] = "openai"
if not os.getenv("LLM_ENDPOINT"):
    os.environ["LLM_ENDPOINT"] = "https://api.groq.com/openai/v1"

model = os.getenv("LLM_MODEL", "")
BAD_MODELS = ["mixtral-8x7b-32768", "gpt-oss-20b", "gpt-oss-safeguard-20b", "llama-3.3-70b"]
if not model or any(bad in model.lower() for bad in BAD_MODELS):
    model = "openai/llama-3.1-8b-instant"
    os.environ["LLM_MODEL"] = model
elif not model.startswith("openai/"):
    model = f"openai/{model}"
    os.environ["LLM_MODEL"] = model

# ---- Embedding Configuration (FastEmbed — local, no API key) ----
os.environ.setdefault("EMBEDDING_PROVIDER", "fastembed")
os.environ.setdefault("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
os.environ.setdefault("EMBEDDING_DIMENSIONS", "384")

os.environ["TELEMETRY_DISABLED"] = "true"

import cognee

cognee.config.set_llm_provider(os.getenv("LLM_PROVIDER", "openai"))
cognee.config.set_llm_model(os.getenv("LLM_MODEL", "openai/llama-3.1-8b-instant"))
cognee.config.set_llm_endpoint(os.getenv("LLM_ENDPOINT", "https://api.groq.com/openai/v1"))
cognee.config.set_llm_api_key(os.getenv("LLM_API_KEY", ""))
cognee.config.data_root_directory(os.environ["DATA_ROOT_DIRECTORY"])
cognee.config.system_root_directory(os.environ["SYSTEM_ROOT_DIRECTORY"])
cognee.config.set_embedding_provider(os.environ["EMBEDDING_PROVIDER"])
cognee.config.set_embedding_model(os.environ["EMBEDDING_MODEL"])
cognee.config.set_embedding_dimensions(int(os.environ["EMBEDDING_DIMENSIONS"]))

COGNEE_TIMEOUT = 120


def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        import cognee.modules.pipelines.operations.pipeline as _p
        _p._dataset_locks = {}
        _p._dataset_locks_guard = asyncio.Lock()
        _p.update_status_lock = asyncio.Lock()
        return loop.run_until_complete(
            asyncio.wait_for(coro, timeout=COGNEE_TIMEOUT)
        )
    except asyncio.TimeoutError:
        print("run_async timeout")
        raise
    except Exception:
        import traceback
        traceback.print_exc()
        raise


async def _remember(text: str):
    await cognee.remember(text)


async def _recall(question: str):
    return await cognee.recall(question)


async def _improve():
    try:
        await cognee.improve()
    except Exception as e:
        print(f"Improve note: {e}")


async def _forget():
    try:
        await cognee.forget()
    except Exception as e:
        print(f"Forget note: {e}")


def remember_this(text: str) -> bool:
    try:
        run_async(_remember(text))
        return True
    except Exception as e:
        print(f"Remember error: {e}")
        return False


def ask_brain(question: str) -> List[Any]:
    try:
        results = run_async(_recall(question))
        return results if results else []
    except Exception as e:
        print(f"Recall error: {e}")
        return []


def improve_brain() -> bool:
    try:
        run_async(_improve())
        return True
    except Exception as e:
        print(f"Improve error (non-fatal): {e}")
        return True


def forget_all() -> bool:
    try:
        run_async(_forget())
        return True
    except Exception as e:
        print(f"Forget error (non-fatal): {e}")
        return True


print("ContextOS Brain -- Connected to Cognee")
