"""
components/sidebar.py
Shared sidebar — rendered by app.py on every page load.
"""

import os
from pathlib import Path

import streamlit as st

import ai_engine
import taiga_adapter

_PHASES = [
    ("views/phase1.py", "Phase 1 · Requirements"),
    ("views/phase2.py", "Phase 2 · Design"),
    ("views/phase3.py", "Phase 3 · Implementation"),
    ("views/phase4.py", "Phase 4 · Testing"),
    ("views/phase5.py", "Phase 5 · Deployment"),
    ("views/phase6.py", "Phase 6 · Maintenance"),
]

_CONTENT_HEIGHT = 260  # px


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(
            '<span style="font-size:1.35rem;font-weight:700;color:#ffffff;letter-spacing:-0.02em;">bolt</span>'
            '<span style="font-size:11px;color:#555;font-weight:400;margin-left:6px;">· Spec-Anchored Continuity</span>',
            unsafe_allow_html=True,
        )
        st.divider()

        for path, label in _PHASES:
            st.page_link(path, label=label)

        st.divider()
        _ai_status()
        _taiga_status()
        st.divider()
        _memory_bank()


def _ai_status() -> None:
    try:
        ai_engine.check_api_key()
        st.markdown(f"**Anthropic** &nbsp; `{ai_engine.get_fast_model()}`")
    except EnvironmentError as exc:
        st.error(str(exc))
        st.stop()


def _taiga_status() -> None:
    project_id = os.getenv("TAIGA_PROJECT_ID", "0")
    if taiga_adapter.is_configured() and project_id != "0":
        st.markdown(f"**Taiga** &nbsp; project `{project_id}`")
    else:
        st.caption("Taiga not configured — push will fail")


def _memory_bank() -> None:
    col_label, col_btn = st.columns([6, 1], vertical_alignment="center")
    with col_label:
        st.markdown("**Context**")
    with col_btn:
        if st.button("↻", key="ctx_reload_btn", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith(("mem_bank", "func_spec", "tech_spec")):
                    del st.session_state[key]
            st.rerun()

    any_exists = any(
        (Path("openspec") / f).exists()
        for f in ("memory-bank.md", "functional-spec.md", "technical-spec.md")
    )
    if not any_exists:
        st.caption("No context files yet.")
        return
    _context_file_editor("memory-bank.md",    "mem_bank",  "Memory Bank")
    _context_file_editor("functional-spec.md", "func_spec", "Functional Specification")
    _context_file_editor("technical-spec.md",  "tech_spec", "Technical Specification")


def _context_file_editor(filename: str, state_key: str, label: str) -> None:
    path = Path("openspec") / filename
    if not path.exists():
        return

    disk_content = path.read_text(encoding="utf-8")
    disk_key  = f"{state_key}_disk"
    buf_key   = f"{state_key}_buf"    # plain str — read mode source, never a widget key
    write_key = f"{state_key}_write"  # ONLY ever used as a st.text_area widget key
    mode_key  = f"{state_key}_read_mode"

    # Sync buf from disk whenever the file changes externally.
    if st.session_state.get(disk_key) != disk_content:
        st.session_state[buf_key]  = disk_content
        st.session_state[disk_key] = disk_content
    elif buf_key not in st.session_state:
        st.session_state[buf_key] = disk_content

    if mode_key not in st.session_state:
        st.session_state[mode_key] = True  # default: read

    is_read = st.session_state[mode_key]

    # Seed write_key BEFORE the expander/widget renders so Streamlit sees it
    # as a pre-existing value when st.text_area(key=write_key) is first drawn.
    if not is_read and write_key not in st.session_state:
        st.session_state[write_key] = st.session_state[buf_key]

    with st.expander(label, expanded=False):
        # Content and button share the same row so their tops are aligned.
        col_content, col_btn = st.columns([8, 1])

        with col_btn:
            icon = "✏" if is_read else "👁"
            if st.button(icon, key=f"{state_key}_mode_btn", use_container_width=True):
                st.session_state[mode_key] = not is_read
                st.rerun()

        with col_content:
            if is_read:
                with st.container(height=_CONTENT_HEIGHT, border=False):
                    st.markdown(st.session_state[buf_key])
            else:
                st.text_area(
                    label,
                    height=_CONTENT_HEIGHT,
                    label_visibility="collapsed",
                    key=write_key,
                )
                current = st.session_state[write_key]
                if current != st.session_state[disk_key]:
                    path.write_text(current, encoding="utf-8")
                    st.session_state[disk_key] = current
                    st.session_state[buf_key]  = current  # keep read mode in sync
