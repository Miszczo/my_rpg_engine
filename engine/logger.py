"""
EventLogger implementation (Observer-style logging).
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional


class EventLogger:
    """Collect and optionally persist game events.

    This logger replaces ``print()`` calls and keeps logging logic separate
    from game logic (SRP).

    :param persist_path: Optional default file path for persistence.
    """

    _events: List[str]
    _persist_path: Optional[Path]

    def __init__(self, persist_path: Optional[str] = None) -> None:
        """Create a new logger.

        :param persist_path: Optional default path to save events.
        :return: None
        """

        self._events = []
        self._persist_path = Path(persist_path) if persist_path else None

    def log(self, message: str) -> None:
        """Add a new event message.

        :param message: Event message to store.
        :return: None
        """

        self._events.append(message)

    def get_events(self) -> List[str]:
        """Return a copy of all stored events.

        :return: List of logged messages.
        """

        return list(self._events)

    def save_to_file(self, path: Optional[str] = None) -> None:
        """Persist stored events to a file.

        :param path: Optional file path override. If not provided, uses
            ``persist_path`` passed to the constructor.
        :return: None
        :raises ValueError: If no target path is available.
        """

        target = Path(path) if path else self._persist_path
        if target is None:
            raise ValueError("No file path provided for saving events.")

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(self._events) + ("\n" if self._events else ""))

