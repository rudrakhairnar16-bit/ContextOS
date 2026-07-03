"""
ContextOS — Developer Second Brain
Built for The Hangover Part AI Hackathon by WeMakeDevs x Cognee
Uses all 4 Cognee operations: remember(), recall(), improve(), forget()
"""

import os

# CRITICAL: Environment variables MUST be set before importing cognee
os.environ["ENABLE_BACKEND_ACCESS_CONTROL"] = "false"
os.environ["COGNEE_SKIP_CONNECTION_TEST"] = "true"

import nest_asyncio
nest_asyncio.apply()

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from brain import remember_this, ask_brain, improve_brain, forget_all
import traceback
from ingest import (
    ingest_file_content,
    ingest_decision,
    ingest_bug,
    ingest_note
)


def extract_text(results) -> str:
    """Convert Cognee ResponseGraphEntry objects to clean readable text"""
    if not results:
        return ""

    if isinstance(results, str):
        return results

    if isinstance(results, list):
        texts = []
        for r in results:
            if hasattr(r, 'text') and r.text:
                cleaned = r.text.strip()
                skip_phrases = [
                    'the question is "none".',
                    'the question is none.',
                ]
                if cleaned.lower() not in skip_phrases and len(cleaned) > 10:
                    texts.append(cleaned)
            elif isinstance(r, str) and r.strip():
                texts.append(r.strip())
        return "\n\n".join(texts) if texts else ""

    if hasattr(results, 'text') and results.text:
        return results.text.strip()

    return str(results)


# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="ContextOS — Developer Second Brain",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM STYLING
# ============================================
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #7C3AED 0%, #2563EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
        line-height: 1.2;
    }
    .tagline {
        color: #9CA3AF;
        font-size: 1.15rem;
        margin-top: 4px;
        margin-bottom: 32px;
    }
    .cognee-badge {
        display: inline-block;
        background: linear-gradient(135deg, #7C3AED, #4F46E5);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================
if "memory_count" not in st.session_state:
    st.session_state.memory_count = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "confirm_reset" not in st.session_state:
    st.session_state.confirm_reset = False

# ============================================
# HEADER
# ============================================
st.markdown('<p class="main-title">🧠 ContextOS</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="tagline">Your codebase has a permanent memory now. '
    'Never lose context again.</p>',
    unsafe_allow_html=True
)
st.markdown('<span class="cognee-badge">⚡ Powered by Cognee</span>', unsafe_allow_html=True)

# Live stats bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Memories Stored", st.session_state.memory_count, help="Items added this session")
with col2:
    st.metric("Engine", "Cognee 1.2.2", help="Graph-vector memory layer")
with col3:
    st.metric("Operations", "4/4 Active", help="remember, recall, improve, forget")
with col4:
    st.metric("Status", "🟢 Ready", help="Brain is active and accepting data")

st.divider()

# ============================================
# SIDEBAR — FEED YOUR BRAIN
# ============================================
with st.sidebar:
    st.header("⚡ Feed Your Brain")
    st.caption("Everything here is stored permanently in Cognee's knowledge graph")

    # ---- File Upload ----
    st.subheader("📁 Upload Code Files")
    uploaded_files = st.file_uploader(
        "Drop files here (multiple OK)",
        type=["py", "js", "ts", "md", "txt", "json", "yaml", "html", "css"],
        accept_multiple_files=True,
        help="Hold Ctrl to select multiple files"
    )

    if uploaded_files:
        st.info(f"📦 {len(uploaded_files)} file(s) ready to ingest")
        if st.button("🚀 Ingest Files into Brain", type="primary"):
            success_count = 0
            progress_bar = st.progress(0)
            status_text = st.empty()
            errors = []

            for i, file in enumerate(uploaded_files):
                status_text.text(f"Processing {file.name}...")
                try:
                    content = file.read().decode("utf-8", errors="ignore")
                    if content.strip():
                        result = ingest_file_content(file.name, content)
                        if result:
                            success_count += 1
                            st.session_state.memory_count += 1
                        else:
                            errors.append(f"{file.name}: ingestion failed silently")
                    else:
                        errors.append(f"{file.name}: file content is empty")
                except Exception as e:
                    errors.append(f"{file.name}: {str(e)}")
                progress_bar.progress((i + 1) / len(uploaded_files))

            status_text.empty()
            if success_count > 0:
                st.success(f"✅ {success_count}/{len(uploaded_files)} files in memory!")
            if errors:
                st.error("Some issues:")
                for err in errors:
                    st.code(err)

    st.divider()

    # ---- Developer Note ----
    st.subheader("📝 Add a Note")
    with st.form("note_form", clear_on_submit=True):
        note_text = st.text_area(
            "What do you want to remember?",
            placeholder="I was debugging auth.py at line 87. The JWT expiry bug is still "
                        "unsolved. I was trying the token rotation approach next...",
            height=100
        )
        submit_note = st.form_submit_button("💾 Save Note to Brain")
        if submit_note:
            if note_text.strip():
                with st.spinner("Storing in Cognee..."):
                    try:
                        if ingest_note(note_text):
                            st.session_state.memory_count += 1
                            st.success("✅ Note saved!")
                    except Exception as e:
                        st.error(f"Cognee error: {e}")
            else:
                st.warning("Write something first")

    st.divider()

    # ---- Decision Logger ----
    st.subheader("🏛️ Log Architecture Decision")
    with st.form("decision_form", clear_on_submit=True):
        decision_input = st.text_input(
            "Decision made:",
            placeholder="Use Redis instead of PostgreSQL"
        )
        reason_input = st.text_area(
            "Why did you make it?",
            placeholder="Redis gives sub-10ms response times. PostgreSQL had 400ms latency "
                        "under load testing with 10,000 concurrent users.",
            height=80
        )
        submit_decision = st.form_submit_button("📌 Log Decision")
        if submit_decision:
            if decision_input.strip() and reason_input.strip():
                with st.spinner("Logging to Cognee..."):
                    try:
                        if ingest_decision(decision_input, reason_input):
                            st.session_state.memory_count += 1
                            st.success("✅ Decision logged!")
                    except Exception as e:
                        st.error(f"Cognee error: {e}")
            else:
                st.warning("Fill both fields")

    st.divider()

    # ---- Bug Logger ----
    st.subheader("🐛 Log a Bug")
    with st.form("bug_form", clear_on_submit=True):
        bug_input = st.text_input(
            "Bug description:",
            placeholder="JWT token not refreshing on /api/auth/refresh"
        )
        bug_status = st.text_area(
            "Current status:",
            placeholder="Unsolved. Tried sliding window (failed). Tried forced re-login "
                        "(bad UX). Next: try token rotation.",
            height=80
        )
        submit_bug = st.form_submit_button("🐛 Log Bug")
        if submit_bug:
            if bug_input.strip() and bug_status.strip():
                with st.spinner("Logging to Cognee..."):
                    try:
                        if ingest_bug(bug_input, bug_status):
                            st.session_state.memory_count += 1
                            st.success("✅ Bug logged!")
                    except Exception as e:
                        st.error(f"Cognee error: {e}")
            else:
                st.warning("Fill both fields")

    st.divider()

    # ---- Memory Controls ----
    st.subheader("🔧 Memory Controls")
    st.caption(f"Session memories: {st.session_state.memory_count}")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("⚡ Improve Brain", help="Uses Cognee improve() to make memory smarter"):
            with st.spinner("Running improve()..."):
                improve_brain()
            st.success("✅ Brain improved!")

    with col_b:
        if st.button("🗑️ Reset Memory", help="Uses Cognee forget() to clear all data"):
            if st.session_state.confirm_reset:
                with st.spinner("Running forget()..."):
                    forget_all()
                st.session_state.memory_count = 0
                st.session_state.chat_history = []
                st.session_state.confirm_reset = False
                st.success("✅ Memory cleared!")
            else:
                st.session_state.confirm_reset = True
                st.warning("⚠️ Click again to confirm reset")

# ============================================
# MAIN AREA — 3 TABS
# ============================================
tab1, tab2, tab3 = st.tabs([
    "💬 Ask Your Brain",
    "🌅 Context Resume",
    "📊 Knowledge Explorer"
])

# ============================================
# TAB 1: ASK YOUR BRAIN
# ============================================
with tab1:
    st.header("💬 Ask Anything About Your Codebase")
    st.caption("Powered by Cognee recall() — hybrid graph + vector search")

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_question = st.chat_input(
        "Why did we use Redis? / What bugs are open? / What was I working on last?"
    )

    if user_question:
        with st.chat_message("user"):
            st.markdown(user_question)
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("assistant"):
            with st.spinner("Querying Cognee knowledge graph... (may take 20-40 seconds)"):
                results = ask_brain(user_question)

            clean_answer = extract_text(results)

            if clean_answer:
                st.markdown("**Found in your memory:**")
                st.info(clean_answer)
                answer = clean_answer
            else:
                answer = (
                    "I don't have information about this yet.\n\n"
                    "💡 **Try this:** Use the sidebar to upload code files, "
                    "log decisions, or add notes. Then ask again!"
                )
                st.write(answer)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

    # Quick question buttons
    st.divider()
    st.caption("Quick questions — make sure you've added data first:")
    q_col1, q_col2, q_col3 = st.columns(3)

    with q_col1:
        if st.button("🐛 Open bugs?"):
            with st.spinner("Recalling from Cognee graph..."):
                r = ask_brain("What bugs are currently unsolved?")
            clean = extract_text(r)
            if clean:
                st.info(clean)
            else:
                st.warning("No bugs found. Log a bug using the sidebar first, then ask again.")

    with q_col2:
        if st.button("🏛️ Key decisions?"):
            with st.spinner("Recalling from Cognee graph..."):
                r = ask_brain("What architectural decisions were made?")
            clean = extract_text(r)
            if clean:
                st.info(clean)
            else:
                st.warning("No decisions found. Log a decision using the sidebar first.")

    with q_col3:
        if st.button("📝 Recent notes?"):
            with st.spinner("Recalling from Cognee graph..."):
                r = ask_brain("What developer notes have been added?")
            clean = extract_text(r)
            if clean:
                st.info(clean)
            else:
                st.warning("No notes found. Add a note using the sidebar first.")

# ============================================
# TAB 2: CONTEXT RESUME (THE KILLER FEATURE)
# ============================================
with tab2:
    st.header("🌅 Context Resume")
    st.markdown("### Pick up *exactly* where you left off")

    st.markdown("""
    <div style="background: rgba(124, 58, 237, 0.08); border-left: 4px solid #7C3AED;
    padding: 20px; border-radius: 0 12px 12px 0; margin: 16px 0;">
    <strong>The Problem ContextOS Solves:</strong><br>
    It's Monday morning. You closed your laptop Friday. You had Redis configured,
    a critical JWT bug half-solved, and 3 architecture decisions pending.
    ChatGPT doesn't remember any of it. Your team's Notion is outdated.
    <br><br>
    <strong>ContextOS remembers everything. One click.</strong>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        resume_clicked = st.button(
            "📖 RESUME MY CONTEXT",
            type="primary",
            use_container_width=True,
            help="ContextOS will tell you exactly where you left off using Cognee recall()"
        )

    if resume_clicked:
        with st.spinner("ContextOS is pulling your last session from Cognee memory... (30-60s)"):
            resume_results = ask_brain(
                "Give me a complete summary: What files was I working on last? "
                "What bugs are currently unsolved and what approaches have been tried? "
                "What architectural decisions are pending or were recently made? "
                "What was I last debugging or implementing? "
                "Where exactly did I leave off and what should I do first?"
            )

        clean_resume = extract_text(resume_results)

        st.divider()

        if clean_resume:
            st.success("📍 Welcome back! Here's exactly where you left off:")
            st.divider()
            st.markdown(clean_resume)

            st.divider()
            st.subheader("⚡ Suggested Next Actions")
            action_col1, action_col2 = st.columns(2)

            with action_col1:
                st.markdown("**Based on your memory:**")
                with st.spinner("Generating action items..."):
                    actions = ask_brain(
                        "What are the 3 most important things I should work on right now "
                        "based on what's unresolved and what was last being worked on?"
                    )
                clean_actions = extract_text(actions)
                if clean_actions:
                    st.write(clean_actions)

            with action_col2:
                st.markdown("**What to avoid:**")
                with st.spinner("Checking..."):
                    blockers = ask_brain(
                        "What decisions have already been made that I should not revisit? "
                        "What approaches have already been tried and failed?"
                    )
                clean_blockers = extract_text(blockers)
                if clean_blockers:
                    st.write(clean_blockers)

            st.caption(
                "💡 This context was retrieved from Cognee's hybrid graph-vector "
                "knowledge store using recall()"
            )
        else:
            st.info(
                "No context found yet!\n\n"
                "To use Context Resume:\n"
                "1. Upload your code files using the sidebar\n"
                "2. Log any decisions you've made\n"
                "3. Add notes about what you were working on\n"
                "4. Then click Resume My Context"
            )

    st.divider()

    # ---- Instant Recall ----
    st.subheader("⚡ Instant Recall")
    q1, q2, q3, q4 = st.columns(4)

    with q1:
        if st.button("🐛 Unsolved bugs", use_container_width=True):
            with st.spinner("Recalling..."):
                r = ask_brain("What bugs are currently unsolved and what is their status?")
            result = extract_text(r)
            st.info(result if result else "No bugs logged yet")

    with q2:
        if st.button("🏛️ Last decision", use_container_width=True):
            with st.spinner("Recalling..."):
                r = ask_brain("What architectural decisions have been made and why?")
            result = extract_text(r)
            st.info(result if result else "No decisions logged yet")

    with q3:
        if st.button("📁 Files edited", use_container_width=True):
            with st.spinner("Recalling..."):
                r = ask_brain("What files have been ingested or worked on recently?")
            result = extract_text(r)
            st.info(result if result else "No files found yet")

    with q4:
        if st.button("⚠️ Blockers", use_container_width=True):
            with st.spinner("Recalling..."):
                r = ask_brain(
                    "What are the current blockers, issues or things that need attention?"
                )
            result = extract_text(r)
            st.info(result if result else "No blockers found yet")

# ============================================
# TAB 3: KNOWLEDGE EXPLORER
# ============================================
with tab3:
    st.header("📊 Knowledge Explorer")
    st.caption(
        "Explore how Cognee's knowledge graph connects concepts in your codebase"
    )

    st.markdown("""
    <div style="background: rgba(37, 99, 235, 0.08); border: 1px solid rgba(37, 99, 235, 0.2);
    border-radius: 12px; padding: 20px; margin-bottom: 24px;">
    <strong>What makes Cognee different:</strong> Unlike regular AI that just stores text,
    Cognee builds a <em>knowledge graph</em> — it understands that Redis is related to
    caching, which connects to auth, which connects to JWT, which connects to your bug.
    This tab lets you explore those connections.
    </div>
    """, unsafe_allow_html=True)

    concept = st.text_input(
        "Enter a concept to explore:",
        value="Redis",
        placeholder="Redis, authentication, database, performance, JWT..."
    )

    if st.button("🔍 Explore This Concept") and concept:
        with st.spinner(f"Querying Cognee graph for '{concept}'... (30-60 seconds)"):
            direct = ask_brain(
                f"Tell me everything about {concept} — "
                f"how it's used, what decisions were made, "
                f"any bugs related to it, and what files mention it."
            )

        clean_direct = extract_text(direct)

        st.subheader(f"🔮 Results for: {concept}")
        if clean_direct:
            st.success("Found in Cognee's knowledge graph:")
            st.write(clean_direct)

            # Visual concept map
            st.divider()
            import re
            words = re.findall(r'\b[A-Za-z][a-z]{3,}\b', clean_direct)
            unique_words = list(dict.fromkeys(
                [w for w in words if len(w) > 4 and w.lower() != concept.lower()]
            ))[:8]
            colors = ["#7C3AED", "#2563EB", "#059669", "#D97706",
                      "#DC2626", "#4F46E5", "#0891B2", "#7C3AED"]

            if unique_words:
                concept_html = f"""
                <div style="background:#0F172A;border-radius:16px;padding:30px;
                min-height:150px;display:flex;flex-wrap:wrap;align-items:center;
                justify-content:center;gap:12px;border:1px solid #1E293B;">
                    <div style="background:linear-gradient(135deg,#7C3AED,#4F46E5);
                    color:white;padding:12px 24px;border-radius:50px;font-weight:800;
                    font-size:1.1rem;">🔮 {concept}</div>
                    {"".join([
                        f'<div style="background:{colors[i % len(colors)]}22;'
                        f'color:{colors[i % len(colors)]};'
                        f'padding:8px 16px;border-radius:50px;'
                        f'border:1px solid {colors[i % len(colors)]}44;'
                        f'font-weight:600;">{w}</div>'
                        for i, w in enumerate(unique_words)
                    ])}
                </div>
                """
                st.components.v1.html(concept_html, height=200)
        else:
            st.warning(
                f"No information found about '{concept}' yet.\n\n"
                f"**Make sure you have:**\n"
                f"1. Uploaded files that mention '{concept}'\n"
                f"2. Waited for ingestion to complete\n"
                f"3. Try a simpler word like 'Redis', 'auth', or 'bug'"
            )

    st.divider()

    st.subheader("💡 How Cognee's Memory Works")
    exp_col1, exp_col2, exp_col3 = st.columns(3)

    with exp_col1:
        st.markdown("""
        **remember()**
        - Takes your text
        - Chunks it intelligently
        - Extracts entities
        - Builds graph nodes
        - Creates embeddings
        """)

    with exp_col2:
        st.markdown("""
        **recall()**
        - Takes your question
        - Searches the graph
        - Searches vector store
        - Combines both results
        - Returns richer context
        """)

    with exp_col3:
        st.markdown("""
        **improve() + forget()**
        - improve() refines weights
        - Makes recall smarter
        - forget() removes nodes
        - Keeps memory clean
        - Full lifecycle control
        """)

# ============================================
# FOOTER
# ============================================
st.divider()
st.markdown("""
<div style="text-align: center; padding: 20px; color: #6B7280;">
    🧠 <strong>ContextOS</strong> — Built for The Hangover Part AI Hackathon 2026
    &nbsp;|&nbsp;
    Powered by <a href="https://cognee.ai" style="color: #7C3AED; text-decoration: none;">
    Cognee</a>
    &nbsp;|&nbsp;
    <a href="https://github.com/rudrakhairnar16-bit/ContextOS"
    style="color: #7C3AED; text-decoration: none;">GitHub</a>
    &nbsp;|&nbsp;
    Never lose your mental stack again
</div>
""", unsafe_allow_html=True)