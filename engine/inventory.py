"""Character inventory with capacity limits and equipment slots."""

from __future__ import annotations

from collections.abc import Iterator

from engine.exceptions import InvalidItemError, InventoryFullError
from engine.items import Armor, Item, Weapon


class Inventory:
    """Store items and track equipped weapon and armor.

    Args:
        capacity: Maximum number of items the inventory can hold.
    """

    def __init__(self, capacity: int = 20) -> None:
        """Initialize an empty inventory with the given capacity."""
        self._items: list[Item] = []
        self._capacity = capacity
        self._equipped_weapon: Weapon | None = None
        self._equipped_armor: Armor | None = None

    @property
    def capacity(self) -> int:
        """Maximum number of items this inventory can store."""
        return self._capacity

    @property
    def equipped_weapon(self) -> Weapon | None:
        """Currently equipped weapon, if any."""
        return self._equipped_weapon

    @property
    def equipped_armor(self) -> Armor | None:
        """Currently equipped armor piece, if any."""
        return self._equipped_armor

    def add(self, item: Item) -> None:
        """Add an item to the inventory.

        Args:
            item: Item instance to store.

        Raises:
            InventoryFullError: If the inventory has reached capacity.
        """
        if len(self._items) >= self._capacity:
            raise InventoryFullError(
                f"Inventory is full (capacity={self._capacity})."
            )
        self._items.append(item)

    def remove(self, item: Item) -> Item:
        """Remove an item from the inventory.

        Args:
            item: Item instance to remove.

        Returns:
            The removed item instance.

        Raises:
            InvalidItemError: If the item is not present in the inventory.
        """
        if item not in self._items:
            raise InvalidItemError(f"Item {item.name!r} not found in inventory.")
        self._items.remove(item)
        if self._equipped_weapon is item:
            self._equipped_weapon = None
        if self._equipped_armor is item:
            self._equipped_armor = None
        return item

    def equip_weapon(self, weapon: Weapon) -> None:
        """Equip a weapon from the inventory.

        Args:
            weapon: Weapon instance to equip.

        Raises:
            InvalidItemError: If ``weapon`` is not a ``Weapon`` or not in the
                inventory.
        """
        if not isinstance(weapon, Weapon):
            raise InvalidItemError(
                f"Cannot equip {type(weapon).__name__}; expected Weapon."
            )
        if weapon not in self._items:
            raise InvalidItemError(
                f"Weapon {weapon.name!r} is not in the inventory."
            )
        self._equipped_weapon = weapon

    def equip_armor(self, armor: Armor) -> None:
        """Equip an armor piece from the inventory.

        Args:
            armor: Armor instance to equip.

        Raises:
            InvalidItemError: If ``armor`` is not ``Armor`` or not in the
                inventory.
        """
        if not isinstance(armor, Armor):
            raise InvalidItemError(
                f"Cannot equip {type(armor).__name__}; expected Armor."
            )
        if armor not in self._items:
            raise InvalidItemError(
                f"Armor {armor.name!r} is not in the inventory."
            )
        self._equipped_armor = armor

    def get_defense(self) -> int:
        """Return defense bonus from equipped armor."""
        if self._equipped_armor is None:
            return 0
        return self._equipped_armor.defense

    def get_damage(self) -> int:
        """Return effective damage from the equipped weapon."""
        if self._equipped_weapon is None:
            return 0
        return self._equipped_weapon.calculate_effective_damage()

    def __len__(self) -> int:
        """Return the number of items currently stored."""
        return len(self._items)

    def __iter__(self) -> Iterator[Item]:
        """Iterate over stored items in insertion order."""
        return iter(self._items)

    def __contains__(self, item: object) -> bool:
        """Return True when ``item`` is stored in this inventory."""
        return item in self._items

    def __getitem__(self, index: int) -> Item:
        """Return the item at the given index."""
        return self._items[index]
