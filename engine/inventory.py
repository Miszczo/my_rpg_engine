"""
Inventory implementation.
"""

from __future__ import annotations

from typing import List, Optional

from engine.base import Item


class Inventory:
    """Store a character's items.

    Inventory manages adding and removing items and can optionally write
    actions to an :class:`~engine.logger.EventLogger`.

    :param logger: Optional event logger instance.
    """

    _items: List[Item]
    _logger: Optional["EventLogger"]

    def __init__(self, logger: Optional["EventLogger"] = None) -> None:
        """Create a new inventory.

        :param logger: Optional event logger instance.
        :return: None
        """

        self._items = []
        self._logger = logger

    def add_item(self, item: Item) -> None:
        """Add an item to the inventory.

        :param item: Item instance to add.
        :return: None
        """

        self._items.append(item)
        if self._logger is not None:
            self._logger.log(f"Added: {item.name}")

    def remove_item(self, item: Item) -> None:
        """Remove an item from the inventory.

        :param item: Item instance to remove.
        :return: None
        :raises ValueError: If the item is not present in the inventory.
        """

        try:
            self._items.remove(item)
        except ValueError as exc:
            raise ValueError("Item not found in inventory.") from exc

        if self._logger is not None:
            self._logger.log(f"Removed: {item.name}")

    @property
    def items(self) -> List[Item]:
        """Return a copy of stored items.

        :return: List of items.
        """

        return list(self._items)

    def __len__(self) -> int:
        """Return number of items in the inventory."""

        return len(self._items)

