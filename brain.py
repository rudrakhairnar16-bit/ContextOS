import os

os.environ["ENABLE_BACKEND_ACCESS_CONTROL"] = "false"
os.environ["COGNEE_SKIP_CONNECTION_TEST"] = "true"

import asyncio
from typing import Any, List
from dotenv import load_dotenv

load_dotenv()

# --- Cognee LLM Configuration ---
# Cognee reads LLM_API_KEY, not GROQ_API_KEY.
# Groq is OpenAI-compatible, so LLM_PROVIDER must be "openai".
# Fix common misconfigurations so the app works regardless of secrets setup.

if not os.getenv("LLM_API_KEY"):
    os.environ["LLM_API_KEY"] = os.getenv("GROQ_API_KEY", "")

if os.getenv("LLM_PROVIDER", "").lower() == "groq":
    os.environ["LLM_PROVIDER"] = "openai"

if not os.getenv("LLM_ENDPOINT"):
    os.environ["LLM_ENDPOINT"] = "https://api.groq.com/openai/v1"

model = os.getenv("LLM_MODEL", "")
if model and not model.startswith("openai/"):
    os.environ["LLM_MODEL"] = f"openai/{model}"

import cognee

# Programmatic Cognee configuration (overrides env vars if already set by Cognee)
cognee.config.set_llm_provider(os.getenv("LLM_PROVIDER", "openai"))
cognee.config.set_llm_model(os.getenv("LLM_MODEL", "openai/llama-3.1-8b-instant"))
cognee.config.set_llm_endpoint(os.getenv("LLM_ENDPOINT", "https://api.groq.com/openai/v1"))
cognee.config.set_llm_api_key(os.getenv("LLM_API_KEY", ""))


def run_async(coro):
    """Thread-safe async runner that works inside Streamlit"""
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
    """Synchronous wrapper for remember — safe to call from Streamlit"""
    try:
        run_async(_remember(text))
        return True
    except Exception as e:
        print(f"Remember error: {e}")
        return False


def ask_brain(question: str) -> List[Any]:
    """Synchronous wrapper for recall — safe to call from Streamlit"""
    try:
        results = run_async(_recall(question))
        return results if results else []
    except Exception as e:
        print(f"Recall error: {e}")
        return []


def improve_brain() -> bool:
    """Synchronous wrapper for improve — safe to call from Streamlit"""
    try:
        run_async(_improve())
        return True
    except Exception as e:
        print(f"Improve error (non-fatal): {e}")
        return True


def forget_all() -> bool:
    """Synchronous wrapper for forget — safe to call from Streamlit"""
    try:
        run_async(_forget())
        return True
    except Exception as e:
        print(f"Forget error (non-fatal): {e}")
        return True


print("✅ ContextOS Brain — Connected to Cognee")