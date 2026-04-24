"""
components/phase1.py
Phase 1 — Mob Elaboration: Discovery & Requirements.

Three-step pipeline:
  GENERATE          → ai_engine.generate_nl_stories()    → NL draft for human cross-examination
  COMPILE           → ai_engine.compile_gherkin_stories() → formal Gherkin per story, human review
  CONFIRM PUSH      → taiga_adapter.create_story() × N   → Taiga + context lock

Session state keys are documented in _STATE_DEFAULTS.
"""

import streamlit as st

import ai_engine
import context_manager
import taiga_adapter
from taiga_adapter import TaigaAPIError

_STATE_DEFAULTS: dict = {
    "nl_draft":         "",    # Step 1: formatted NL text shown in the editor
    "nl_editor":        "",    # live text-area value (human edits)
    "story_subject":    "",
    "compiled_stories": None,  # list[{"title", "size", "gherkin"}] after Step 2
    "push_done":        False,
    "push_result":      None,
    "ai_error":         None,
    "compile_error":    None,
}


def render_phase1() -> None:
    _init_state()

    st.title("Phase 1 · Requirements")
    st.caption("Mob Elaboration — transform an Epic into formal Gherkin Acceptance Criteria")
    st.image("requirements.svg", use_container_width=True)
    st.divider()

    _section_epic()
    st.divider()
    _section_generate()
    st.divider()

    if st.session_state.nl_draft:
        _section_review()
        st.divider()
        if not st.session_state.compiled_stories:
            _section_compile()
        else:
            _section_gherkin_review()


# ── Session state ─────────────────────────────────────────────────────────────

def _init_state() -> None:
    for key, default in _STATE_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


# ── Section: Epic input ───────────────────────────────────────────────────────

def _apply_epic_selection() -> None:
    """on_change callback — stages the selected epic for application on next render."""
    idx: int = st.session_state.get("epic_selectbox_idx", 0)
    epics: list[dict] = st.session_state.get("epics_list") or []
    if idx > 0 and epics:
        chosen = epics[idx - 1]
        # Fetch the full epic to get the complete description (list endpoint may omit it).
        try:
            full = taiga_adapter.get_epic(chosen["id"])
        except TaigaAPIError:
            full = chosen
        st.session_state["_pending_epic_data"] = {
            "subject":     full.get("subject", chosen.get("subject", "")),
            "description": full.get("description", "") or "",
            "id":          str(chosen["id"]),
        }


def _apply_pending_epic() -> None:
    """Apply staged epic data BEFORE any widget with those keys is rendered."""
    pending: dict | None = st.session_state.pop("_pending_epic_data", None)
    if not pending:
        return
    if "subject" in pending:
        st.session_state["epic_subject_input"] = pending["subject"]
    if "description" in pending:
        st.session_state["epic_desc_input"] = pending["description"]
    if "id" in pending:
        st.session_state["epic_id_input"] = pending["id"]


def _section_epic() -> None:
    _apply_pending_epic()   # must run before any widget with these keys renders
    st.markdown("#### EPIC")
    _epic_browser()

    col_title, col_id = st.columns([3, 1])
    with col_title:
        st.text_input(
            "Title",
            placeholder="e.g. User Authentication with OAuth2",
            key="epic_subject_input",
        )
    with col_id:
        st.text_input(
            "Taiga Epic ID (optional)",
            placeholder="e.g. 42",
            key="epic_id_input",
        )

    st.text_area(
        "Description",
        placeholder="Describe the feature, its goals, and any known constraints...",
        height=120,
        key="epic_desc_input",
    )

    st.text_area(
        "AI Guidance (optional)",
        placeholder=(
            "Steer the output — e.g. 'Focus only on the happy path', "
            "'At most 3 stories', 'Assume a REST API backend', "
            "'Skip mobile for this iteration'..."
        ),
        height=70,
        key="ai_hint_input",
    )

def _epic_browser() -> None:
    is_open: bool = st.session_state.get("epics_visible", False)

    if st.button("Browse Epics", key="browse_epics_btn"):
        if not is_open:
            # Opening — fetch only on first load.
            if st.session_state.get("epics_list") is None:
                try:
                    with st.spinner("Loading Epics..."):
                        epics = taiga_adapter.get_epics()
                    st.session_state["epics_list"] = epics
                    st.session_state.pop("epics_load_error", None)
                except TaigaAPIError as exc:
                    st.session_state["epics_load_error"] = str(exc)
        else:
            # Closing — clear the epic form fields.
            st.session_state["_pending_epic_data"] = {"subject": "", "description": "", "id": ""}
        st.session_state["epics_visible"] = not is_open
        st.rerun()

    if not st.session_state.get("epics_visible"):
        return

    if st.session_state.get("epics_load_error"):
        st.error(st.session_state["epics_load_error"])
        return

    epics: list[dict] | None = st.session_state.get("epics_list")
    if epics is None:
        return
    if not epics:
        st.caption("No Epics found in this project.")
        return

    labels = ["— select an existing Epic —"] + [
        f"#{e.get('ref', e['id'])} · {e['subject']}" for e in epics
    ]
    st.selectbox(
        "Existing Epics",
        options=range(len(labels)),
        format_func=lambda i: labels[i],
        key="epic_selectbox_idx",
        on_change=_apply_epic_selection,
        label_visibility="collapsed",
    )


# ── Section: Generate ─────────────────────────────────────────────────────────

def _section_generate() -> None:
    st.markdown("#### GENERATE")

    subject = st.session_state.get("epic_subject_input", "").strip()
    description = st.session_state.get("epic_desc_input", "").strip()
    hint = st.session_state.get("ai_hint_input", "").strip()
    can_generate = bool(subject and description)

    project_concept = context_manager.get_project_concept()
    if not project_concept:
        st.warning(
            "No Project Concept found in the Memory Bank. "
            "Add a description under **## Project Concept** in the sidebar to give the AI better context."
        )

    if st.button(
        "Generate stories",
        type="primary",
        disabled=not can_generate,
        key="generate_btn",
    ):
        _run_generation(subject, description, hint, project_concept)

    if not can_generate:
        st.caption("Title and Description are required.")

    if st.session_state.ai_error:
        st.error(st.session_state.ai_error)


def _run_generation(subject: str, description: str, hint: str, project_concept: str = "") -> None:
    with st.spinner("Drafting User Stories in Natural Language..."):
        try:
            story_list = ai_engine.generate_nl_stories(
                subject, description, hint=hint, project_concept=project_concept
            )
            nl_text = ai_engine.format_nl_draft(story_list)
            st.session_state.nl_draft = nl_text
            st.session_state.nl_editor = nl_text
            st.session_state.story_subject = subject
            st.session_state.push_done = False
            st.session_state.push_result = None
            st.session_state.ai_error = None
            st.session_state.compile_error = None
        except Exception as exc:
            st.session_state.ai_error = _classify_ai_error(exc)


def _classify_ai_error(exc: Exception) -> str:
    msg = str(exc)
    if "429" in msg or "rate_limit" in msg.lower() or "quota" in msg.lower():
        return (
            "Rate limit or quota exceeded (HTTP 429). "
            "Check your Anthropic usage at console.anthropic.com, "
            "or verify ANTHROPIC_API_KEY is correct in .env."
        )
    return msg


# ── Section: Review & Edit (Interactive Bridge) ───────────────────────────────

def _section_review() -> None:
    st.markdown("#### REVIEW AND EDIT")
    st.caption(
        "Review the Natural Language draft. Edit freely — "
        "this will be compiled to formal Gherkin on approval."
    )

    if "nl_editor" not in st.session_state:
        st.session_state.nl_editor = st.session_state.nl_draft

    st.text_area(
        "Natural Language Story Draft",
        key="nl_editor",
        height=400,
    )


# ── Section: Compile (Discovery Gate — step 1) ───────────────────────────────

def _section_compile() -> None:
    st.markdown("#### APPROVE AND COMPILE")
    st.caption("Approve the NL draft to compile it into formal Gherkin for review.")

    col_compile, col_reset = st.columns([2, 1])
    with col_compile:
        compile_clicked = st.button(
            "Compile Gherkin",
            type="primary",
            key="compile_btn",
        )
    with col_reset:
        if st.button("Reset", key="reset_btn"):
            _reset_state()
            st.rerun()

    if compile_clicked:
        _run_compile()

    if st.session_state.get("compile_error"):
        st.error(f"Gherkin compilation failed: {st.session_state.compile_error}")


def _run_compile() -> None:
    nl_text = st.session_state.get("nl_editor", "")
    with st.spinner("Compiling Natural Language draft to formal Gherkin..."):
        try:
            gherkin_list = ai_engine.compile_gherkin_stories(nl_text)
            compiled = [
                {
                    "title": story.title,
                    "size": story.size,
                    "gherkin": ai_engine.format_gherkin_story(story),
                }
                for story in gherkin_list.stories
            ]
            st.session_state.compiled_stories = compiled
            # seed per-story editor keys so text_areas are pre-filled
            for i, item in enumerate(compiled):
                st.session_state[f"gherkin_edit_{i}"] = item["gherkin"]
            st.session_state.compile_error = None
        except Exception as exc:
            st.session_state.compile_error = _classify_ai_error(exc)
    st.rerun()


# ── Section: Gherkin Review + Confirm Push ────────────────────────────────────

def _sync_editors_to_compiled() -> None:
    """Snapshot current text-area values back into compiled_stories before mutating the list."""
    for i, item in enumerate(st.session_state.compiled_stories):
        item["gherkin"] = st.session_state.get(f"gherkin_edit_{i}", item["gherkin"])


def _reseed_editors() -> None:
    """Clear all gherkin_edit_* keys and re-seed them from the (mutated) compiled_stories."""
    _clear_gherkin_editors()
    for i, item in enumerate(st.session_state.compiled_stories):
        st.session_state[f"gherkin_edit_{i}"] = item["gherkin"]


def _delete_story(index: int) -> None:
    _sync_editors_to_compiled()
    del st.session_state.compiled_stories[index]
    # Clear rename state so stale indices don't bleed into the shifted list.
    for key in [k for k in st.session_state if k.startswith(("rename_mode_", "rename_input_"))]:
        del st.session_state[key]
    _reseed_editors()


def _add_story() -> None:
    _sync_editors_to_compiled()
    new_story = {
        "title": "New Story",
        "size": "S",
        "gherkin": "Feature: New Story\n\n  Scenario: \n    Given \n    When \n    Then ",
    }
    st.session_state.compiled_stories.append(new_story)
    idx = len(st.session_state.compiled_stories) - 1
    st.session_state[f"gherkin_edit_{idx}"] = new_story["gherkin"]


def _section_gherkin_review() -> None:
    st.markdown("#### COMPILED GHERKIN")
    st.caption(
        "Review the formal Gherkin below. "
        "Each story will be created as a separate entity in Taiga."
    )

    compiled: list[dict] = st.session_state.compiled_stories
    push_done = st.session_state.push_done

    for i, item in enumerate(compiled):
        with st.expander(f"[{item['size']}] {item['title']}", expanded=True):
            if not push_done:
                is_renaming: bool = st.session_state.get(f"rename_mode_{i}", False)

                col_title_input, col_ren, col_del = st.columns([8, 1, 1])
                with col_title_input:
                    if is_renaming:
                        st.text_input(
                            "Story title",
                            key=f"rename_input_{i}",
                            label_visibility="collapsed",
                        )
                with col_ren:
                    if st.button("✓" if is_renaming else "✎", key=f"rename_btn_{i}", use_container_width=True):
                        if is_renaming:
                            new_title = st.session_state.get(f"rename_input_{i}", "").strip()
                            if new_title:
                                compiled[i]["title"] = new_title
                            st.session_state[f"rename_mode_{i}"] = False
                        else:
                            st.session_state[f"rename_mode_{i}"] = True
                            st.session_state[f"rename_input_{i}"] = item["title"]
                        st.rerun()
                with col_del:
                    if st.button("✕", key=f"del_story_{i}", use_container_width=True):
                        _delete_story(i)
                        st.rerun()

            st.text_area(
                "Gherkin",
                key=f"gherkin_edit_{i}",
                height=250,
                label_visibility="collapsed",
                disabled=push_done,
            )

    if not push_done:
        if st.button("+ Add Story", key="add_story_btn"):
            _add_story()
            st.rerun()

    st.divider()
    st.markdown("#### CONFIRM PUSH")

    col_push, col_back = st.columns([2, 1])
    with col_push:
        push_clicked = st.button(
            "Confirm Push to Taiga",
            type="primary",
            disabled=st.session_state.push_done,
            key="push_btn",
        )
    with col_back:
        if st.button("Edit Draft", key="edit_btn", disabled=st.session_state.push_done):
            _clear_gherkin_editors()
            st.session_state.compiled_stories = None
            st.session_state.compile_error = None
            st.rerun()

    if push_clicked:
        _run_push()

    _render_push_result()


def _run_push() -> None:
    compiled: list[dict] = st.session_state.compiled_stories
    epic_id_val = _parse_epic_id()
    epic_info: dict | None = None

    with st.spinner("Pushing stories to Taiga, locking Gherkin to context..."):
        context_manager.init_context()

        if epic_id_val is None:
            # No existing epic selected — create one from the form fields.
            subject     = st.session_state.get("epic_subject_input", "").strip()
            description = st.session_state.get("epic_desc_input", "").strip()
            try:
                epic = taiga_adapter.create_epic(subject, description)
                epic_id_val = epic["id"]
                epic_info = {"epic_id": epic_id_val, "title": subject, "created": True}
            except TaigaAPIError as exc:
                st.session_state.push_result = {"ok": False, "error": str(exc)}
                st.rerun()
                return
        else:
            # Existing epic selected — link stories to it, do NOT create a new one.
            epic_info = {
                "epic_id": epic_id_val,
                "title": st.session_state.get("epic_subject_input", "").strip(),
                "created": False,
            }

        created: list[dict] = []
        push_error: str | None = None

        for i, item in enumerate(compiled):
            gherkin_text = st.session_state.get(f"gherkin_edit_{i}", item["gherkin"])
            try:
                taiga_story = taiga_adapter.create_story(
                    item["title"], ai_engine.bold_gherkin_keywords(gherkin_text)
                )
                story_id = taiga_story["id"]
                taiga_adapter.link_story_to_epic(epic_id_val, story_id)
                context_manager.append_gherkin(
                    story_id, item["title"], gherkin_text,
                    epic_id=epic_id_val,
                    epic_title=epic_info["title"] if epic_info else "",
                )
                created.append({"story_id": story_id, "title": item["title"]})
            except TaigaAPIError as exc:
                push_error = str(exc)
                break

        if created:
            st.session_state.push_done = True
            st.session_state.push_result = {
                "ok": True,
                "epic": epic_info,
                "stories": created,
                "partial": push_error is not None,
                "partial_error": push_error,
            }
        else:
            st.session_state.push_result = {"ok": False, "error": push_error}

    st.rerun()


def _render_push_result() -> None:
    result = st.session_state.push_result
    if not result:
        return

    stories = result.get("stories", [])
    story_lines = "\n".join(
        f"- Story #{s['story_id']}: **{s['title']}**" for s in stories
    )

    if result["ok"] and not result.get("partial"):
        count = len(stories)
        noun = "story" if count == 1 else "stories"
        epic = result.get("epic")
        if epic:
            if epic.get("created"):
                epic_line = f"Epic #{epic['epic_id']}: **{epic['title']}** created.\n\n"
            else:
                epic_line = f"Linked to existing Epic #{epic['epic_id']}: **{epic['title']}**.\n\n"
        else:
            epic_line = ""
        st.success(
            f"{epic_line}"
            f"{count} {noun} created and linked in Taiga. "
            f"Gherkin locked to `openspec/functional-spec.md`.\n\n"
            f"{story_lines}"
        )

    elif result["ok"] and result.get("partial"):
        st.warning(
            f"{len(stories)} pushed, then stopped — {result['partial_error']}\n\n"
            f"{story_lines}"
        )

    else:
        st.error(f"Push failed: {result['error']}")

    if result["ok"] and st.button("New Epic", key="new_epic_btn"):
        _reset_state()
        st.rerun()


def _parse_epic_id() -> int | None:
    raw = st.session_state.get("epic_id_input", "").strip()
    try:
        return int(raw) if raw else None
    except ValueError:
        return None


def _clear_gherkin_editors() -> None:
    for key in [k for k in st.session_state if k.startswith(
        ("gherkin_edit_", "rename_mode_", "rename_input_")
    )]:
        del st.session_state[key]


def _reset_state() -> None:
    _clear_gherkin_editors()
    for key in (
        "nl_draft", "nl_editor", "story_subject",
        "compiled_stories", "push_done", "push_result",
        "ai_error", "compile_error",
        "epic_selectbox_idx",
        "epic_subject_input", "epic_desc_input", "epic_id_input",
    ):
        st.session_state.pop(key, None)
