import os

os.environ["ENABLE_BACKEND_ACCESS_CONTROL"] = "false"
os.environ["COGNEE_SKIP_CONNECTION_TEST"] = "true"

import asyncio
import threading
from concurrent.futures import TimeoutError as FutureTimeoutError

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
BAD_MODELS = ["mixtral-8x7b-32768", "gpt-oss-20b", "gpt-oss-safeguard-20b"]
if not model or any(bad in model.lower() for bad in BAD_MODELS):
    model = "openai/llama-3.3-70b-versatile"
    os.environ["LLM_MODEL"] = model
elif not model.startswith("openai/"):
    model = f"openai/{model}"
    os.environ["LLM_MODEL"] = model

# ---- Embedding Configuration (FastEmbed — local, no API key) ----
os.environ.setdefault("EMBEDDING_PROVIDER", "fastembed")
os.environ.setdefault("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
os.environ.setdefault("EMBEDDING_DIMENSIONS", "384")

# Disable Cognee telemetry (avoids asyncio.Lock "bound to a different event loop" error)
os.environ["TELEMETRY_DISABLED"] = "true"

# Dedicated event loop for Cognee. Initialized on the main thread
# first so all async locks bind to it during import, then kept alive
# in a background thread.
_cognee_loop = asyncio.new_event_loop()

async def _init_cognee():
    import cognee
    cognee.config.set_llm_provider(os.getenv("LLM_PROVIDER", "openai"))
    cognee.config.set_llm_model(os.getenv("LLM_MODEL", "openai/llama-3.3-70b-versatile"))
    cognee.config.set_llm_endpoint(os.getenv("LLM_ENDPOINT", "https://api.groq.com/openai/v1"))
    cognee.config.set_llm_api_key(os.getenv("LLM_API_KEY", ""))
    cognee.config.data_root_directory(os.environ["DATA_ROOT_DIRECTORY"])
    cognee.config.system_root_directory(os.environ["SYSTEM_ROOT_DIRECTORY"])
    cognee.config.set_embedding_provider(os.environ["EMBEDDING_PROVIDER"])
    cognee.config.set_embedding_model(os.environ["EMBEDDING_MODEL"])
    cognee.config.set_embedding_dimensions(int(os.environ["EMBEDDING_DIMENSIONS"]))
    return cognee

# Initialize Cognee on the main thread while importing, so module-level
# async objects (locks, connections) bind to _cognee_loop.
_cognee = _cognee_loop.run_until_complete(_init_cognee())

# Keep the loop alive in a background thread for future operations.
def _run_cognee_loop():
    asyncio.set_event_loop(_cognee_loop)
    _cognee_loop.run_forever()

threading.Thread(target=_run_cognee_loop, daemon=True).start()


COGNEE_TIMEOUT = 120

def run_async(coro):
    global _cognee_loop
    try:
        future = asyncio.run_coroutine_threadsafe(
            asyncio.wait_for(coro, timeout=COGNEE_TIMEOUT),
            _cognee_loop
        )
        return future.result(timeout=COGNEE_TIMEOUT + 10)
    except FutureTimeoutError:
        print("run_async timeout")
        raise
    except Exception as e:
        print(f"run_async error: {e}")
        raise


async def _remember(text: str):
    await _cognee.remember(text)


async def _recall(question: str):
    return await _cognee.recall(question)


async def _improve():
    try:
        await _cognee.improve()
    except Exception as e:
        print(f"Improve note: {e}")


async def _forget():
    try:
        await _cognee.forget()
    except Exception as e:
        print(f"Forget note: {e}")


def remember_this(text: str) -> bool:
    run_async(_remember(text))
    return True


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


print("✅ ContextOS Brain — Connected to Cognee")
