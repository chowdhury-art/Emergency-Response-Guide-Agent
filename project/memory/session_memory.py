from typing import Any, Dict
import time


class SessionMemory:
    """
    Very simple in-memory session memory.

    In a Colab / demo context this is process-local and ephemeral.
    """

    def __init__(self) -> None:
        # session_id -> dict
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        summary = self._sessions.get(session_id, {})
        return summary.copy()

    def update_session_summary(self, session_id: str, new_info: Dict[str, Any]) -> None:
        if session_id not in self._sessions:
            self._sessions[session_id] = {"created_at": time.time()}
        self._sessions[session_id].update(new_info)

    def set_default_region_if_missing(self, session_id: str, default_region: str = "global") -> None:
        if session_id not in self._sessions:
            self._sessions[session_id] = {}
        if "region" not in self._sessions[session_id]:
            self._sessions[session_id]["region"] = default_region

    def set_default_language_if_missing(self, session_id: str, default_language: str = "en") -> None:
        if session_id not in self._sessions:
            self._sessions[session_id] = {}
        if "language" not in self._sessions[session_id]:
            self._sessions[session_id]["language"] = default_language


# Global singleton for simplicity in this demo
GLOBAL_SESSION_MEMORY = SessionMemory()
