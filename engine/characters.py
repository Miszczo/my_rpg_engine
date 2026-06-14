"""Character hierarchy with stats, inventory composition, and special attacks."""

from __future__ import annotations

from abc import ABC, abstractmethod

from engine.exceptions import InsufficientStatsError, InvalidItemError
from engine.inventory import Inventory
from engine.items import Potion


class Character(ABC):
    """Abstract base class for all playable characters."""

    _next_id: int = 1
    XP_PER_LEVEL: int = 100

    def __init__(
        self,
        name: str,
        max_hp: int = 100,
        strength: int = 10,
        defense: int = 5,
    ) -> None:
        """Create a character with base stats and a composed inventory.

        Args:
            name: Character display name.
            max_hp: Maximum hit points.
            strength: Base strength before level bonuses.
            defense: Base defense before level bonuses and armor.
        """
        self._id = Character._next_id
        Character._next_id += 1
        self.name = name
        self._max_hp = max_hp
        self._hp = max_hp
        self._base_strength = strength
        self._base_defense = defense
        self._level = 1
        self._xp = 0
        self.inventory = Inventory(capacity=20)

    @property
    def id(self) -> int:
        """Unique identifier assigned at creation time."""
        return self._id

    @property
    def level(self) -> int:
        """Current character level."""
        return self._level

    @property
    def max_hp(self) -> int:
        """Maximum hit points."""
        return self._max_hp

    @property
    def hp(self) -> int:
        """Current hit points."""
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        """Set HP with clamping to the range ``[0, max_hp]``."""
        self._hp = max(0, min(value, self._max_hp))

    @property
    def strength(self) -> int:
        """Effective strength including level bonuses."""
        return self._base_strength + (self._level - 1) * 2

    @property
    def defense(self) -> int:
        """Effective defense including level bonus and equipped armor."""
        level_bonus = (self._level - 1) * 1
        return self._base_defense + level_bonus + self.inventory.get_defense()

    @property
    def attack_power(self) -> int:
        """Effective attack power including weapon damage."""
        return self.strength + self.inventory.get_damage()

    @abstractmethod
    def char_class(self) -> str:
        """Return the character class label."""

    @abstractmethod
    def special_attack(self) -> tuple[str, int]:
        """Perform a class-specific special attack.

        Returns:
            Tuple of action name and damage dealt.
        """

    def take_damage(self, raw_damage: int) -> int:
        """Apply damage reduced by defense.

        Args:
            raw_damage: Incoming damage before mitigation.

        Returns:
            Actual damage applied to HP.
        """
        if raw_damage <= 0:
            return 0
        actual = max(0, raw_damage - self.defense)
        self.hp = self._hp - actual
        return actual

    def heal(self, amount: int) -> int:
        """Restore hit points up to ``max_hp``.

        Args:
            amount: HP to restore.

        Returns:
            Amount of HP actually restored.
        """
        if amount <= 0:
            return 0
        before = self.hp
        self.hp = self._hp + amount
        return self.hp - before

    def use_potion(self, potion: Potion) -> int:
        """Consume a potion from inventory and apply its effects.

        Args:
            potion: Potion instance to consume.

        Returns:
            Amount of HP restored.

        Raises:
            InvalidItemError: If ``potion`` is not in the inventory.
        """
        if not isinstance(potion, Potion):
            raise InvalidItemError(
                f"Cannot use {type(potion).__name__}; expected Potion."
            )
        if potion not in self.inventory:
            raise InvalidItemError(
                f"Potion {potion.name!r} is not in the inventory."
            )
        healed = self.heal(potion.heal_amount)
        if potion.mana_restore > 0 and hasattr(self, "mana"):
            self.mana = self.mana + potion.mana_restore
        self.inventory.remove(potion)
        return healed

    def gain_xp(self, amount: int) -> bool:
        """Add experience points and process level-ups.

        Args:
            amount: Experience points to add.

        Returns:
            True if at least one level-up occurred, otherwise False.
        """
        if amount <= 0:
            return False
        self._xp += amount
        leveled_up = False
        while self._xp >= self.XP_PER_LEVEL:
            self._xp -= self.XP_PER_LEVEL
            self._level += 1
            leveled_up = True
        return leveled_up

    def __repr__(self) -> str:
        """Return a developer-friendly representation with id, name, and level."""
        return (
            f"{self.__class__.__name__}(id={self._id}, name={self.name!r}, "
            f"level={self._level})"
        )

    def __str__(self) -> str:
        """Return a user-friendly summary of name, level, class, and HP."""
        return (
            f"{self.name} (Level {self._level} {self.char_class()}, "
            f"HP: {self.hp}/{self.max_hp})"
        )

    def __eq__(self, other: object) -> bool:
        """Compare characters by unique ``_id``."""
        if not isinstance(other, Character):
            return NotImplemented
        return self._id == other._id

    def __lt__(self, other: object) -> bool:
        """Order characters by level for sorting."""
        if not isinstance(other, Character):
            return NotImplemented
        return self._level < other._level


class Warrior(Character):
    """Melee fighter with high HP and strength."""

    HEROIC_STRIKE_BONUS: int = 10

    def __init__(self, name: str) -> None:
        """Create a warrior with high HP, strength, and defense."""
        super().__init__(name, max_hp=120, strength=14, defense=8)

    def char_class(self) -> str:
        """Return the warrior class label."""
        return "Warrior"

    def special_attack(self) -> tuple[str, int]:
        """Perform Heroic Strike for bonus physical damage."""
        return ("Heroic Strike", self.attack_power + self.HEROIC_STRIKE_BONUS)


class Mage(Character):
    """Spellcaster relying on mana for powerful attacks."""

    FIREBALL_COST: int = 25
    FIREBALL_DAMAGE: int = 40

    def __init__(self, name: str) -> None:
        """Create a mage with a mana pool for spellcasting."""
        super().__init__(name, max_hp=80, strength=8, defense=5)
        self._max_mana = 100
        self._mana = 100

    @property
    def mana(self) -> int:
        """Current mana pool."""
        return self._mana

    @mana.setter
    def mana(self, value: int) -> None:
        """Set mana with clamping to the range ``[0, max_mana]``."""
        self._mana = max(0, min(value, self._max_mana))

    @property
    def max_mana(self) -> int:
        """Maximum mana capacity."""
        return self._max_mana

    def char_class(self) -> str:
        """Return the mage class label."""
        return "Mage"

    def special_attack(self) -> tuple[str, int]:
        """Cast Fireball or fall back to a basic attack when mana is low."""
        if self.mana < self.FIREBALL_COST:
            return ("Basic Attack", self.attack_power)
        self.mana -= self.FIREBALL_COST
        return ("Fireball", self.FIREBALL_DAMAGE)


class Archer(Character):
    """Ranged fighter with balanced mobility and damage."""

    PIERCING_SHOT_BONUS: int = 12

    def __init__(self, name: str) -> None:
        """Create an archer with balanced ranged combat stats."""
        super().__init__(name, max_hp=90, strength=12, defense=6)

    def char_class(self) -> str:
        """Return the archer class label."""
        return "Archer"

    def special_attack(self) -> tuple[str, int]:
        """Perform Piercing Shot for bonus ranged damage."""
        return ("Piercing Shot", self.attack_power + self.PIERCING_SHOT_BONUS)


class Healer(Character):
    """Support class with healing abilities and holy damage."""

    HOLY_SMITE_COST: int = 20
    HOLY_SMITE_DAMAGE: int = 30
    HEAL_ALLY_MANA_COST: int = 15

    def __init__(self, name: str) -> None:
        """Create a healer with a mana pool for support abilities."""
        super().__init__(name, max_hp=100, strength=9, defense=7)
        self._max_mana = 120
        self._mana = 120

    @property
    def mana(self) -> int:
        """Current mana pool."""
        return self._mana

    @mana.setter
    def mana(self, value: int) -> None:
        """Set mana with clamping to the range ``[0, max_mana]``."""
        self._mana = max(0, min(value, self._max_mana))

    @property
    def max_mana(self) -> int:
        """Maximum mana capacity."""
        return self._max_mana

    def char_class(self) -> str:
        """Return the healer class label."""
        return "Healer"

    def special_attack(self) -> tuple[str, int]:
        """Cast Holy Smite or fall back to a basic attack when mana is low."""
        if self.mana < self.HOLY_SMITE_COST:
            return ("Basic Attack", self.attack_power)
        self.mana -= self.HOLY_SMITE_COST
        return ("Holy Smite", self.HOLY_SMITE_DAMAGE)

    def heal_ally(self, target: Character, amount: int = 40) -> int:
        """Heal an ally at the cost of mana.

        Args:
            target: Ally to heal.
            amount: HP to restore on the target.

        Returns:
            Amount of HP actually restored on the target.

        Raises:
            InsufficientStatsError: If there is not enough mana.
        """
        if self.mana < self.HEAL_ALLY_MANA_COST:
            raise InsufficientStatsError(
                f"Not enough mana for heal_ally "
                f"(have {self.mana}, need {self.HEAL_ALLY_MANA_COST})."
            )
        self.mana -= self.HEAL_ALLY_MANA_COST
        return target.heal(amount)
