import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ["ENABLE_BACKEND_ACCESS_CONTROL"] = "false"
os.environ["COGNEE_SKIP_CONNECTION_TEST"] = "true"
os.environ.setdefault("LLM_MODEL", "openai/mixtral-8x7b-32768")
os.environ.setdefault("LLM_ENDPOINT", "https://api.groq.com/openai/v1")
os.environ.setdefault("EMBEDDING_PROVIDER", "fastembed")
os.environ.setdefault("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
os.environ.setdefault("EMBEDDING_DIMENSIONS", "384")

from brain import remember_this, ask_brain, improve_brain, forget_all


def test_remember_returns_bool():
    result = remember_this("TEST: Unit test entry")
    assert isinstance(result, bool)


def test_recall_returns_list():
    result = ask_brain("test")
    assert isinstance(result, list)


def test_improve_does_not_crash():
    result = improve_brain()
    assert result is True


def test_forget_does_not_crash():
    result = forget_all()
    assert result is True


def test_extract_text_handles_empty():
    from app import extract_text
    assert extract_text(None) == ""
    assert extract_text([]) == ""
    assert extract_text("") == ""
