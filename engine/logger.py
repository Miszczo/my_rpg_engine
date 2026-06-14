"""EventLogger implementation (Observer-style logging)."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional


class EventLogger:
    """Collect and optionally persist game events.

    This logger replaces ``print()`` calls and keeps logging logic separate
    from game logic (SRP).
    """

    _events: List[str]
    _persist_path: Optional[Path]

    def __init__(self, persist_path: Optional[str] = None) -> None:
        """Create a new logger.

        Args:
            persist_path: Optional default path to save events.
        """
        self._events = []
        self._persist_path = Path(persist_path) if persist_path else None

    def log(self, message: str) -> None:
        """Add a new event message.

        Args:
            message: Event message to store.
        """
        self._events.append(message)

    def get_events(self) -> List[str]:
        """Return a copy of all stored events.

        Returns:
            List of logged messages.
        """
        return list(self._events)

    def save_to_file(self, path: Optional[str] = None) -> None:
        """Persist stored events to a file.

        Args:
            path: Optional file path override. If not provided, uses
                ``persist_path`` passed to the constructor.

        Raises:
            ValueError: If no target path is available.
        """
        target = Path(path) if path else self._persist_path
        if target is None:
            raise ValueError("No file path provided for saving events.")

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(self._events) + ("\n" if self._events else ""))
