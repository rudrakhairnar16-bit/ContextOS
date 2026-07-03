import os

os.environ["ENABLE_BACKEND_ACCESS_CONTROL"] = "false"
os.environ["COGNEE_SKIP_CONNECTION_TEST"] = "true"

import asyncio
from typing import Any, List
from dotenv import load_dotenv

load_dotenv()

import cognee


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