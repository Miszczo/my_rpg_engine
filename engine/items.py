"""Item hierarchy: weapons, armor, potions, and rarity."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum

from engine.exceptions import InvalidItemError


class Rarity(Enum):
    """Item rarity tiers used for valuation and loot generation."""

    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"


class Item(ABC):
    """Abstract base class for all inventory items.

    Each instance receives a unique identifier from the class-level ``_next_id``
    counter.
    """

    _next_id: int = 1

    def __init__(
        self,
        name: str,
        value: int = 0,
        rarity: Rarity = Rarity.COMMON,
        weight: float = 1.0,
    ) -> None:
        """Initialize item metadata and assign a unique id.

        Args:
            name: Human-readable item name.
            value: Monetary value used for sorting and comparison.
            rarity: Rarity tier of the item.
            weight: Item weight in inventory units.
        """
        self._id = Item._next_id
        Item._next_id += 1
        self.name = name
        self.value = value
        self.rarity = rarity
        self.weight = weight

    @property
    def id(self) -> int:
        """Unique identifier assigned at creation time."""
        return self._id

    @abstractmethod
    def item_type(self) -> str:
        """Return a short type label for the item."""

    @abstractmethod
    def use_description(self) -> str:
        """Return a human-readable description of the item's effect."""

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self._id}, name={self.name!r}, "
            f"value={self.value}, rarity={self.rarity.value})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return self._id == other._id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return self.value < other.value


class Weapon(Item, ABC):
    """Abstract base class for weapons with durability-based damage."""

    MIN_DAMAGE: int = 1

    def __init__(
        self,
        name: str,
        damage: int,
        durability: int = 100,
        value: int = 0,
        rarity: Rarity = Rarity.COMMON,
        weight: float = 1.0,
    ) -> None:
        """Create a weapon with base damage and durability.

        Args:
            name: Human-readable weapon name.
            damage: Base damage before durability penalties.
            durability: Initial durability (values below 0 are clamped to 0).
            value: Monetary value of the weapon.
            rarity: Rarity tier of the weapon.
            weight: Weapon weight in inventory units.
        """
        super().__init__(name=name, value=value, rarity=rarity, weight=weight)
        self.damage = damage
        self._durability = max(0, durability)

    @property
    def durability(self) -> int:
        """Current durability (never below 0)."""
        return self._durability

    @durability.setter
    def durability(self, value: int) -> None:
        self._durability = max(0, value)

    @property
    def is_broken(self) -> bool:
        """Return True when durability has reached zero."""
        return self.durability <= 0

    def calculate_effective_damage(self) -> int:
        """Return effective damage accounting for weapon condition.

        Returns:
            Base damage when durability is above zero, otherwise ``MIN_DAMAGE``.
        """
        if self.is_broken:
            return self.MIN_DAMAGE
        return self.damage

    def degrade(self, amount: int = 5) -> None:
        """Reduce durability by ``amount`` (default 5).

        Args:
            amount: Durability loss. Non-positive values are ignored.
        """
        if amount <= 0:
            return
        self.durability = self.durability - amount


class Sword(Weapon):
    """Melee sword with default iron-sword stats."""

    def __init__(
        self,
        name: str = "Iron Sword",
        damage: int = 15,
        durability: int = 100,
        value: int = 0,
        rarity: Rarity = Rarity.COMMON,
        weight: float = 1.0,
    ) -> None:
        """Create a sword with optional overrides for default stats."""
        super().__init__(
            name=name,
            damage=damage,
            durability=durability,
            value=value,
            rarity=rarity,
            weight=weight,
        )

    def item_type(self) -> str:
        return "sword"

    def use_description(self) -> str:
        return f"A sword that deals up to {self.damage} damage."


class Staff(Weapon):
    """Magical staff with an associated mana cost for special attacks."""

    def __init__(
        self,
        name: str = "Oak Staff",
        damage: int = 20,
        mana_cost: int = 10,
        durability: int = 100,
        value: int = 0,
        rarity: Rarity = Rarity.COMMON,
        weight: float = 1.0,
    ) -> None:
        """Create a staff with optional overrides for default stats."""
        super().__init__(
            name=name,
            damage=damage,
            durability=durability,
            value=value,
            rarity=rarity,
            weight=weight,
        )
        self._mana_cost = mana_cost

    @property
    def mana_cost(self) -> int:
        """Mana cost associated with staff-based special attacks."""
        return self._mana_cost

    def item_type(self) -> str:
        return "staff"

    def use_description(self) -> str:
        return (
            f"A staff that deals up to {self.damage} damage "
            f"(mana cost: {self.mana_cost})."
        )


class Armor(Item):
    """Protective gear occupying a single equipment slot."""

    VALID_SLOTS: tuple[str, ...] = ("head", "chest", "legs")

    def __init__(
        self,
        name: str,
        defense: int,
        slot: str = "chest",
        value: int = 0,
        rarity: Rarity = Rarity.COMMON,
        weight: float = 1.0,
    ) -> None:
        """Create armor for a validated body slot.

        Args:
            name: Human-readable armor name.
            defense: Defense bonus provided when equipped.
            slot: Body slot; must be one of ``VALID_SLOTS``.
            value: Monetary value of the armor.
            rarity: Rarity tier of the armor.
            weight: Armor weight in inventory units.

        Raises:
            InvalidItemError: If ``slot`` is not a valid armor slot.
        """
        if slot not in self.VALID_SLOTS:
            raise InvalidItemError(
                f"Invalid armor slot {slot!r}; expected one of {self.VALID_SLOTS}"
            )
        super().__init__(name=name, value=value, rarity=rarity, weight=weight)
        self.defense = defense
        self.slot = slot

    def item_type(self) -> str:
        return "armor"

    def use_description(self) -> str:
        return f"Armor for the {self.slot} slot providing {self.defense} defense."


class Potion(Item):
    """Consumable item restoring HP and/or mana via ``Character.use_potion``."""

    def __init__(
        self,
        name: str = "Health Potion",
        heal_amount: int = 30,
        mana_restore: int = 0,
        value: int = 0,
        rarity: Rarity = Rarity.COMMON,
        weight: float = 0.5,
    ) -> None:
        """Create a potion with restorative properties."""
        super().__init__(name=name, value=value, rarity=rarity, weight=weight)
        self.heal_amount = heal_amount
        self.mana_restore = mana_restore

    def item_type(self) -> str:
        return "potion"

    def use_description(self) -> str:
        effects: list[str] = []
        if self.heal_amount > 0:
            effects.append(f"restores {self.heal_amount} HP")
        if self.mana_restore > 0:
            effects.append(f"restores {self.mana_restore} mana")
        if not effects:
            return "A potion with no restorative effect."
        return f"A potion that {' and '.join(effects)}."
