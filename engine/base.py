"""
Core abstract contracts for the RPG engine.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from engine.inventory import Inventory


class Item(ABC):
    """Abstract base class for all items.

    :param name: Human-readable item name.
    """

    name: str

    def __init__(self, name: str) -> None:
        """Create a new item.

        :param name: Human-readable item name.
        :return: None
        """

        self.name = name

    @abstractmethod
    def use(self, target: "Character") -> None:
        """Apply the item effect to the given character.

        :param target: Character to apply the item to.
        :return: None
        """


class Weapon(Item, ABC):
    """Base class for weapons with durability (encapsulation via property).

    When durability reaches 0, damage calculation degrades to the minimum
    value used in melee-like behavior.
    """

    MIN_DAMAGE: int = 1

    damage: int
    _durability: int

    def __init__(self, name: str, damage: int, durability: int) -> None:
        """Create a new weapon with durability.

        :param name: Human-readable weapon name.
        :param damage: Base damage value.
        :param durability: Initial durability (values < 0 are clamped to 0).
        :return: None
        """

        super().__init__(name=name)
        self.damage = damage
        self._durability = max(0, durability)

    @property
    def durability(self) -> int:
        """Current durability value (never below 0).

        :return: Durability as an integer.
        """

        return self._durability

    @durability.setter
    def durability(self, value: int) -> None:
        """Set durability (clamped to 0..inf).

        :param value: New durability.
        :return: None
        """

        self._durability = max(0, value)

    @property
    def is_broken(self) -> bool:
        """Whether the weapon is effectively broken.

        :return: True if durability is 0, otherwise False.
        """

        return self.durability <= 0

    def calculate_effective_damage(self) -> int:
        """Calculate effective damage considering durability.

        If durability is 0, returns a minimum damage value.

        :return: Effective damage value.
        """

        if self.durability <= 0:
            return self.MIN_DAMAGE
        return self.damage

    def decrease_durability(self, amount: int) -> None:
        """Decrease durability by `amount`.

        :param amount: Durability decrease amount (ignored if <= 0).
        :return: None
        """

        if amount <= 0:
            return
        self.durability = self.durability - amount

    @abstractmethod
    def use(self, target: "Character") -> None:
        """Apply weapon effect to the given character.

        :param target: Character to apply the effect to.
        :return: None
        """


class Character(ABC):
    """Abstract base class for all characters.

    :param name: Character name.
    :param health: Current health points.
    :param inventory: Character's inventory instance.
    """

    name: str
    health: int
    inventory: "Inventory"

    def __init__(self, name: str, health: int, inventory: "Inventory") -> None:
        """Create a new character.

        :param name: Character name.
        :param health: Initial health points.
        :param inventory: Character's inventory instance.
        :return: None
        """

        self.name = name
        self.health = health
        self.inventory = inventory

    @abstractmethod
    def attack(self, target: "Character") -> None:
        """Attack another character.

        :param target: Enemy character to attack.
        :return: None
        """

    def take_damage(self, amount: int) -> None:
        """Reduce health by `amount` (clamped to 0..inf).

        :param amount: Damage amount (if <= 0, ignored).
        :return: None
        """

        if amount <= 0:
            return
        self.health = max(0, self.health - amount)

