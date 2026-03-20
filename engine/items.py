"""
Concrete item classes.

This module provides placeholder implementations of items required by the
project plan. Core gameplay behavior will be added in later steps.
"""

from __future__ import annotations

from typing import Optional

from engine.base import Character, Item, Weapon


class Sword(Weapon):
    """A basic sword weapon.

    :param damage: Base damage dealt when the weapon is not broken.
    :param durability: Starting durability (0 means broken).
    """

    def __init__(self, damage: int, durability: int, name: str = "Sword") -> None:
        """Create a sword.

        :param damage: Base damage.
        :param durability: Starting durability.
        :param name: Display name.
        :return: None
        """

        super().__init__(name=name, damage=damage, durability=durability)

    def use(self, target: Character) -> None:
        """Use the sword on the target.

        :param target: Character to apply the weapon effect to.
        :return: None

        .. note::
           Placeholder implementation. Real attack/durability consumption
           will be integrated in ``engine/combat.py`` in KROK 4.
        """

        # TODO: integrate sword attack/durability consumption logic.
        pass


class Potion(Item):
    """A healing potion item.

    :param heal_amount: Amount of health restored when used.
    """

    heal_amount: int

    def __init__(self, heal_amount: int, name: str = "Potion") -> None:
        """Create a potion.

        :param heal_amount: Health restored when used.
        :param name: Display name.
        :return: None
        """

        super().__init__(name=name)
        self.heal_amount = max(0, heal_amount)

    def use(self, target: Character) -> None:
        """Use potion on a character.

        :param target: Character to heal.
        :return: None
        """

        # TODO: apply healing and log event in later steps.
        pass


class RepairKit(Item):
    """A kit that repairs broken or worn weapons.

    :param repair_amount: Durability amount added to a target weapon.
    """

    repair_amount: int

    def __init__(self, repair_amount: int, name: str = "RepairKit") -> None:
        """Create a repair kit.

        :param repair_amount: Amount of durability to restore.
        :param name: Display name.
        :return: None
        """

        super().__init__(name=name)
        self.repair_amount = max(0, repair_amount)

    def use(self, target: Character) -> None:
        """Use repair kit on a character.

        :param target: Character whose equipped weapon should be repaired.
        :return: None
        """

        # TODO: implement weapon repair behavior (later integrated with Inventory/Weapon).
        pass

