"""
taiga_adapter.py
All Taiga REST API GET/POST/PATCH logic.

Authentication: Bearer token from TAIGA_AUTH_TOKEN.
Auto-refresh: when a request returns 401 and TAIGA_USERNAME + TAIGA_PASSWORD are
present in .env, the adapter re-authenticates automatically, updates the
in-memory token, and writes the new token back to .env so it survives restarts.
All public methods raise TaigaAPIError on non-2xx responses.
"""

import os
import re
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

TAIGA_API_URL    = os.getenv("TAIGA_API_URL", "https://api.taiga.io").rstrip("/")
TAIGA_PROJECT_ID = int(os.getenv("TAIGA_PROJECT_ID", "0"))
TAIGA_USERNAME   = os.getenv("TAIGA_USERNAME", "")
TAIGA_PASSWORD   = os.getenv("TAIGA_PASSWORD", "")

# Mutable so _refresh_token() can update it without a module reload.
_token: dict[str, str] = {"value": os.getenv("TAIGA_AUTH_TOKEN", "")}


class TaigaAPIError(Exception):
    """Raised when a Taiga API call returns a non-2xx status."""

    def __init__(self, method: str, url: str, status: int, body: str) -> None:
        super().__init__(f"[{method} {url}] HTTP {status}: {body[:300]}")
        self.status = status


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------

def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_token['value']}",
        "Content-Type": "application/json",
        "x-disable-pagination": "True",
    }


def _refresh_token() -> None:
    """Re-authenticate with username/password, update in-memory token and .env."""
    if not TAIGA_USERNAME or not TAIGA_PASSWORD:
        return  # no credentials available — let the caller surface the original 401
    url = f"{TAIGA_API_URL}/api/v1/auth"
    resp = requests.post(
        url,
        json={"username": TAIGA_USERNAME, "password": TAIGA_PASSWORD, "type": "normal"},
        timeout=15,
    )
    if not resp.ok:
        raise TaigaAPIError("POST", url, resp.status_code, resp.text)
    new_token = resp.json()["auth_token"]
    _token["value"] = new_token
    _persist_token(new_token)


def is_configured() -> bool:
    """Return True if auth is available — either a live token or credentials for auto-refresh."""
    return bool(_token["value"] or (TAIGA_USERNAME and TAIGA_PASSWORD))


def _persist_token(token: str) -> None:
    """Write the refreshed token back to .env so it survives a server restart."""
    env_path = Path(".env")
    if not env_path.exists():
        return
    content = env_path.read_text(encoding="utf-8")
    if "TAIGA_AUTH_TOKEN" in content:
        content = re.sub(r"TAIGA_AUTH_TOKEN=\S*", f"TAIGA_AUTH_TOKEN={token}", content)
    else:
        content = content.rstrip() + f"\nTAIGA_AUTH_TOKEN={token}\n"
    env_path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Core request dispatcher — single 401-retry point
# ---------------------------------------------------------------------------

def _request(method: str, path: str, *, params: dict | None = None, payload: dict | None = None) -> Any:
    url = f"{TAIGA_API_URL}/api/v1/{path.lstrip('/')}"
    fn = getattr(requests, method)

    def _call() -> requests.Response:
        kwargs: dict = {"headers": _headers(), "timeout": 15}
        if params is not None:
            kwargs["params"] = params
        if payload is not None:
            kwargs["json"] = payload
        return fn(url, **kwargs)

    resp = _call()
    if resp.status_code == 401 and TAIGA_USERNAME and TAIGA_PASSWORD:
        _refresh_token()
        resp = _call()
    if not resp.ok:
        raise TaigaAPIError(method.upper(), url, resp.status_code, resp.text)
    return resp.json()


def _get(path: str, params: dict | None = None) -> Any:
    return _request("get", path, params=params)


def _post(path: str, payload: dict) -> Any:
    return _request("post", path, payload=payload)


def _patch(path: str, payload: dict) -> Any:
    return _request("patch", path, payload=payload)


# ---------------------------------------------------------------------------
# Epics
# ---------------------------------------------------------------------------

def get_epics() -> list[dict]:
    """Return all Epics for the project, ordered by ref."""
    return _get("epics", params={"project": TAIGA_PROJECT_ID, "order_by": "ref"})


def get_epic(epic_id: int) -> dict:
    """Fetch a single Epic by ID."""
    return _get(f"epics/{epic_id}")


def create_epic(subject: str, description: str) -> dict:
    """Create a new Epic in the project and return the response dict (includes 'id')."""
    return _post("epics", {
        "project": TAIGA_PROJECT_ID,
        "subject": subject,
        "description": description,
    })


def link_story_to_epic(epic_id: int, story_id: int) -> dict:
    """Link an existing User Story to an Epic via the related_userstories sub-resource."""
    return _post(f"epics/{epic_id}/related_userstories", {
        "epic": epic_id,
        "user_story": story_id,
    })


# ---------------------------------------------------------------------------
# User Stories
# ---------------------------------------------------------------------------

def get_story(story_id: int) -> dict:
    """Fetch a single User Story by ID."""
    return _get(f"userstories/{story_id}")


def get_stories_for_epic(epic_id: int) -> list[dict]:
    """Return all User Stories linked to an Epic."""
    return _get("userstories", params={"epic": epic_id, "project": TAIGA_PROJECT_ID})


def create_story(subject: str, description: str, epic_id: int | None = None) -> dict:
    """Create a new User Story in the project, optionally linked to an Epic."""
    payload: dict[str, Any] = {
        "project": TAIGA_PROJECT_ID,
        "subject": subject,
        "description": description,
    }
    if epic_id is not None:
        payload["epic"] = epic_id
    return _post("userstories", payload)


def update_story_status(story_id: int, status_id: int, version: int) -> dict:
    """Move a User Story to a new status (requires the current version for optimistic locking)."""
    return _patch(
        f"userstories/{story_id}",
        {"status": status_id, "version": version},
    )


def get_story_statuses() -> list[dict]:
    """Return all User Story statuses defined for the project."""
    return _get("userstory-statuses", params={"project": TAIGA_PROJECT_ID})


def find_status_id(name_fragment: str) -> int | None:
    """
    Case-insensitive search for a story status whose name contains name_fragment.
    Returns the status ID or None if not found.
    """
    statuses = get_story_statuses()
    for s in statuses:
        if name_fragment.lower() in s.get("name", "").lower():
            return s["id"]
    return None


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------

def get_task(task_id: int) -> dict:
    """Fetch a single Task by ID."""
    return _get(f"tasks/{task_id}")


def get_tasks_for_story(story_id: int) -> list[dict]:
    """Return all Tasks linked to a User Story."""
    return _get("tasks", params={"user_story": story_id, "project": TAIGA_PROJECT_ID})


def create_task(subject: str, description: str, story_id: int) -> dict:
    """Create a new Task linked to a User Story."""
    return _post(
        "tasks",
        {
            "project": TAIGA_PROJECT_ID,
            "user_story": story_id,
            "subject": subject,
            "description": description,
        },
    )


# ---------------------------------------------------------------------------
# Issues (for fix-bolt)
# ---------------------------------------------------------------------------

def get_issue(issue_id: int) -> dict:
    """Fetch a single Issue/Bug by ID."""
    return _get(f"issues/{issue_id}")


def get_issue_comments(issue_id: int) -> list[dict]:
    """Return the comment/history timeline for an issue (includes stack traces)."""
    return _get(f"history/issue/{issue_id}")
