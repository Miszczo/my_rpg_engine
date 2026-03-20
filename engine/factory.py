"""
CharacterFactory implementation (Factory Method).
"""

from __future__ import annotations

from typing import Optional

from engine.characters import Mage, Warrior
from engine.inventory import Inventory
from engine.items import Potion, RepairKit, Sword
from engine.base import Character
from engine.logger import EventLogger


class CharacterFactory:
    """Factory responsible for creating characters with initial equipment.

    :param logger: Optional logger used for event tracking.
    """

    _logger: Optional[EventLogger]

    def __init__(self, logger: Optional[EventLogger] = None) -> None:
        """Create a new character factory.

        :param logger: Optional event logger instance.
        :return: None
        """

        self._logger = logger

    def create_character(self, char_type: str, name: str) -> Character:
        """Create a new character of the given type.

        :param char_type: Character type, e.g. ``\"warrior\"`` or ``\"mage\"``.
        :param name: Character name.
        :return: Created character instance.
        :raises ValueError: If ``char_type`` is unknown.
        """

        normalized = char_type.strip().lower()
        inventory = Inventory(logger=self._logger)

        if normalized == "warrior":
            character = Warrior(name=name, health=100, inventory=inventory)
            # Base equipment for the warrior
            inventory.add_item(Sword(damage=12, durability=5))
            inventory.add_item(Potion(heal_amount=20))
            inventory.add_item(RepairKit(repair_amount=3))
        elif normalized == "mage":
            character = Mage(name=name, health=90, inventory=inventory)
            # Base equipment for the mage (slightly different parameters)
            inventory.add_item(Sword(damage=10, durability=6))
            inventory.add_item(Potion(heal_amount=25))
            inventory.add_item(RepairKit(repair_amount=2))
        else:
            raise ValueError(f"Unknown character type: {char_type}")

        if self._logger is not None:
            self._logger.log(f"Created character: {name} ({normalized})")

        return character

