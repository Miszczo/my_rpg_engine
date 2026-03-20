"""
Concrete character classes.

This module contains placeholder implementations of hero types.
"""

from __future__ import annotations

from engine.base import Character


class Warrior(Character):
    """A warrior character type.

    This is a placeholder until combat integration is implemented.
    """

    def __init__(self, name: str, health: int, inventory: "Inventory") -> None:
        """Create a warrior.

        :param name: Character name.
        :param health: Starting health.
        :param inventory: Inventory instance (composition).
        :return: None
        """

        super().__init__(name=name, health=health, inventory=inventory)

    def attack(self, target: Character) -> None:
        """Attack a target character.

        :param target: Character to attack.
        :return: None
        """

        # TODO: implement warrior attack behavior and durability consumption.
        pass


class Mage(Character):
    """A mage character type.

    This is a placeholder until combat integration is implemented.
    """

    def __init__(self, name: str, health: int, inventory: "Inventory") -> None:
        """Create a mage.

        :param name: Character name.
        :param health: Starting health.
        :param inventory: Inventory instance (composition).
        :return: None
        """

        super().__init__(name=name, health=health, inventory=inventory)

    def attack(self, target: Character) -> None:
        """Attack a target character.

        :param target: Character to attack.
        :return: None
        """

        # TODO: implement mage attack behavior (e.g., mana in later steps).
        pass

