from brain import remember_this

SUPPORTED_EXTENSIONS = [
    ".py", ".js", ".ts", ".md", ".txt",
    ".json", ".yaml", ".yml", ".html", ".css"
]


def ingest_file_content(filename: str, content: str) -> bool:
    """Ingest a file's content into Cognee memory"""
    memory_text = f"""
PROJECT FILE INGESTED:
File Name: {filename}
Content:
{content[:4000]}
"""
    return remember_this(memory_text)


def ingest_decision(decision: str, reason: str) -> bool:
    """Log an architectural decision permanently"""
    text = f"""
ARCHITECTURAL DECISION LOG:
Decision Made: {decision}
Reason / Justification: {reason}
Status: Active
"""
    return remember_this(text)


def ingest_bug(description: str, status: str) -> bool:
    """Log a bug with its current status"""
    text = f"""
BUG LOG:
Bug Description: {description}
Current Status: {status}
"""
    return remember_this(text)


def ingest_note(note: str) -> bool:
    """Log a developer note"""
    text = f"""
DEVELOPER NOTE:
{note}
"""
    return remember_this(text)