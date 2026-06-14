"""Factory helpers for creating characters with default equipment."""

from engine.characters import Archer, Healer, Mage, Warrior
from engine.items import Potion, Staff, Sword


class CharacterFactory:
    """Create playable characters pre-equipped for demos and tests."""

    @staticmethod
    def create_warrior(name: str) -> Warrior:
        """Create a warrior with an iron sword in the inventory."""
        warrior = Warrior(name)
        warrior.inventory.add(Sword())
        return warrior

    @staticmethod
    def create_mage(name: str) -> Mage:
        """Create a mage with an oak staff in the inventory."""
        mage = Mage(name)
        mage.inventory.add(Staff())
        return mage

    @staticmethod
    def create_archer(name: str) -> Archer:
        """Create an archer with an iron sword in the inventory."""
        archer = Archer(name)
        archer.inventory.add(Sword())
        return archer

    @staticmethod
    def create_healer(name: str) -> Healer:
        """Create a healer with a health potion in the inventory."""
        healer = Healer(name)
        healer.inventory.add(Potion())
        return healer
