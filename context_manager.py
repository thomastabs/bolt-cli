"""
context_manager.py
Manages read/write operations on three spec files in openspec/:

  memory-bank.md       — architecture rules, tech stack, vaccine records
  functional-spec.md   — per-story Gherkin Acceptance Criteria
  technical-spec.md    — per-story technical contracts (OpenAPI / DB schema)
"""

import re
from datetime import datetime, timezone
from pathlib import Path

CONTEXT_DIR          = Path("openspec")
MEMORY_BANK_FILE     = CONTEXT_DIR / "memory-bank.md"
FUNCTIONAL_SPEC_FILE = CONTEXT_DIR / "functional-spec.md"
TECHNICAL_SPEC_FILE  = CONTEXT_DIR / "technical-spec.md"

_MEMORY_BANK_TEMPLATE = """\
# Memory Bank

> Immutable architecture rules, tech stack decisions, enterprise policies, and
> historical bug workarounds. Edited only by the Tech Lead.

## Project Concept

<!-- Describe the project's purpose, target users, and core value proposition. -->

## Tech Stack

<!-- Fill in the project's language, frameworks, libraries, and runtime environment. -->

## Architecture Principles

<!-- Document the core architectural decisions and constraints for this project. -->

---

# Vaccine Records

> Permanent log of diagnosed bugs. Prevents the AI from hallucinating the same error twice.

"""

_FUNCTIONAL_SPEC_TEMPLATE = """\
# Functional Specification

> Per-story Gherkin Acceptance Criteria.
> Appended automatically by bolt after human approval.

"""

_TECHNICAL_SPEC_TEMPLATE = """\
# Technical Specification

> Per-story technical contracts (OpenAPI / DB schema).
> Appended automatically by bolt after human approval.

"""


def init_context() -> None:
    """Create the three spec files with standard templates if they do not exist."""
    CONTEXT_DIR.mkdir(parents=True, exist_ok=True)
    for path, template in [
        (MEMORY_BANK_FILE,     _MEMORY_BANK_TEMPLATE),
        (FUNCTIONAL_SPEC_FILE, _FUNCTIONAL_SPEC_TEMPLATE),
        (TECHNICAL_SPEC_FILE,  _TECHNICAL_SPEC_TEMPLATE),
    ]:
        if not path.exists():
            path.write_text(template, encoding="utf-8")


def read_context() -> str:
    """Return all spec files concatenated — used to build AI prompts."""
    init_context()
    return "\n\n---\n\n".join(
        p.read_text(encoding="utf-8")
        for p in (MEMORY_BANK_FILE, FUNCTIONAL_SPEC_FILE, TECHNICAL_SPEC_FILE)
    )


def get_project_concept() -> str:
    """Return the Project Concept text from memory-bank.md, or '' if not set."""
    if not MEMORY_BANK_FILE.exists():
        return ""
    in_section = False
    section_lines: list[str] = []
    for line in MEMORY_BANK_FILE.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Project Concept"):
            in_section = True
            continue
        if in_section:
            if line.startswith("#") or line.startswith("---"):
                break
            section_lines.append(line)
    text = "\n".join(section_lines).strip()
    # Empty section or unfilled placeholder both count as "not set".
    if not text or text.startswith("<!--"):
        return ""
    return text


def get_story_gherkin(story_id: int) -> str:
    """Extract the Gherkin block for a specific story from functional-spec.md."""
    init_context()
    content = FUNCTIONAL_SPEC_FILE.read_text(encoding="utf-8")
    # Try new format (nested ### under an Epic) first, then legacy flat ## format.
    for pattern in (
        rf"### Story {story_id}:.*?(?=\n### |\n## |\Z)",
        rf"## Story {story_id}:.*?(?=\n## |\Z)",
    ):
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(0).strip()
    return ""


def get_story_technical_spec(story_id: int) -> str:
    """Extract the technical spec block for a specific story from technical-spec.md."""
    init_context()
    content = TECHNICAL_SPEC_FILE.read_text(encoding="utf-8")
    pattern = rf"### Technical Spec — Story {story_id}.*?(?=\n## |\n### |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(0).strip() if match else ""


def append_gherkin(
    story_id: int,
    story_title: str,
    gherkin: str,
    *,
    epic_id: int | None = None,
    epic_title: str = "",
) -> None:
    """Append a locked Gherkin block for a story to functional-spec.md.

    When epic_id is provided stories are nested under an ## Epic section;
    otherwise a legacy flat ## Story block is written.
    """
    init_context()
    content = FUNCTIONAL_SPEC_FILE.read_text(encoding="utf-8")

    # Remove any previous entry for this story (handles both format versions).
    content = re.sub(rf"\n### Story {story_id}:.*?(?=\n### |\n## |\Z)", "", content, flags=re.DOTALL)
    content = re.sub(rf"\n## Story {story_id}:.*?(?=\n## |\Z)", "", content, flags=re.DOTALL)

    if epic_id is not None:
        story_block = (
            f"\n### Story {story_id}: {story_title}\n\n"
            f"**Status:** Gherkin Locked  \n"
            f"**Locked at:** {_now()}\n\n"
            f"```gherkin\n{gherkin.strip()}\n```\n"
        )
        epic_pattern = rf"\n## Epic {epic_id}:.*?(?=\n## |\Z)"
        epic_match = re.search(epic_pattern, content, re.DOTALL)
        if epic_match:
            # Insert story at the end of the existing epic section.
            end = epic_match.end()
            content = content[:end].rstrip() + "\n" + story_block + content[end:]
        else:
            # No section for this epic yet — create one at the end.
            content = content.rstrip() + f"\n\n## Epic {epic_id}: {epic_title}\n" + story_block
    else:
        # Legacy flat format (no epic context).
        block = (
            f"\n## Story {story_id}: {story_title}\n\n"
            f"**Status:** Gherkin Locked  \n"
            f"**Locked at:** {_now()}\n\n"
            f"```gherkin\n{gherkin.strip()}\n```\n"
        )
        content = content.rstrip() + "\n" + block

    FUNCTIONAL_SPEC_FILE.write_text(content, encoding="utf-8")


def append_technical_spec(story_id: int, spec: str) -> None:
    """Append a formal technical spec for a story to technical-spec.md."""
    init_context()
    content = TECHNICAL_SPEC_FILE.read_text(encoding="utf-8")

    tech_block = (
        f"\n### Technical Spec — Story {story_id}\n\n"
        f"**Locked at:** {_now()}\n\n"
        f"```yaml\n{spec.strip()}\n```\n"
    )

    existing = rf"\n### Technical Spec — Story {story_id}.*?(?=\n## |\n### |\Z)"
    content = re.sub(existing, "", content, flags=re.DOTALL)
    content = content.rstrip() + "\n" + tech_block
    TECHNICAL_SPEC_FILE.write_text(content, encoding="utf-8")


def append_vaccine_record(issue_id: int, root_cause: str, resolution_summary: str) -> None:
    """Append a permanent Vaccine Record for a resolved bug to memory-bank.md."""
    init_context()
    content = MEMORY_BANK_FILE.read_text(encoding="utf-8")

    record = (
        f"\n## Vaccine #{issue_id} — {_now()}\n\n"
        f"**Root Cause:** {root_cause.strip()}\n\n"
        f"**Resolution:** {resolution_summary.strip()}\n"
    )

    content = content.rstrip() + "\n" + record + "\n"
    MEMORY_BANK_FILE.write_text(content, encoding="utf-8")


def save_proposal(task_id: int, proposal: str) -> Path:
    """Save a coding proposal to openspec/proposal_task_<id>.md and return the path."""
    CONTEXT_DIR.mkdir(parents=True, exist_ok=True)
    path = CONTEXT_DIR / f"proposal_task_{task_id}.md"
    path.write_text(proposal, encoding="utf-8")
    return path


def save_bdd_tests(story_id: int, test_script: str) -> Path:
    """Save BDD test scripts to openspec/bdd_story_<id>.feature and return the path."""
    CONTEXT_DIR.mkdir(parents=True, exist_ok=True)
    path = CONTEXT_DIR / f"bdd_story_{story_id}.feature"
    path.write_text(test_script, encoding="utf-8")
    return path


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
