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
if not model or "llama" in model.lower():
    os.environ["LLM_MODEL"] = "openai/mixtral-8x7b-32768"
elif not model.startswith("openai/"):
    os.environ["LLM_MODEL"] = f"openai/{model}"

# ---- Embedding Configuration (FastEmbed — local, no API key) ----
os.environ.setdefault("EMBEDDING_PROVIDER", "fastembed")
os.environ.setdefault("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
os.environ.setdefault("EMBEDDING_DIMENSIONS", "384")

import cognee

cognee.config.set_llm_provider(os.getenv("LLM_PROVIDER", "openai"))
cognee.config.set_llm_model(os.getenv("LLM_MODEL", "openai/mixtral-8x7b-32768"))
cognee.config.set_llm_endpoint(os.getenv("LLM_ENDPOINT", "https://api.groq.com/openai/v1"))
cognee.config.set_llm_api_key(os.getenv("LLM_API_KEY", ""))
cognee.config.data_root_directory(os.environ["DATA_ROOT_DIRECTORY"])
cognee.config.system_root_directory(os.environ["SYSTEM_ROOT_DIRECTORY"])
cognee.config.set_embedding_provider(os.environ["EMBEDDING_PROVIDER"])
cognee.config.set_embedding_model(os.environ["EMBEDDING_MODEL"])
cognee.config.set_embedding_dimensions(int(os.environ["EMBEDDING_DIMENSIONS"]))


def run_async(coro):
    try:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(coro)
        else:
            return asyncio.run(coro)
    except Exception as e:
        print(f"run_async error: {e}")
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


print("✅ ContextOS Brain — Connected to Cognee")
