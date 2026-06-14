"""Shared pytest fixtures for the RPG engine test suite."""

import pytest

from engine.characters import Archer, Healer, Mage, Warrior
from engine.factory import CharacterFactory
from engine.game_world import GameWorld
from engine.inventory import Inventory
from engine.items import Potion
from engine.quest import Quest, QuestObjective


@pytest.fixture
def warrior() -> Warrior:
    """Warrior with a sword in inventory."""
    return CharacterFactory.create_warrior("TestWarrior")


@pytest.fixture
def mage() -> Mage:
    """Mage with a staff in inventory."""
    return CharacterFactory.create_mage("TestMage")


@pytest.fixture
def archer() -> Archer:
    """Archer with a sword in inventory."""
    return CharacterFactory.create_archer("TestArcher")


@pytest.fixture
def healer() -> Healer:
    """Healer with a health potion in inventory."""
    return CharacterFactory.create_healer("TestHealer")


@pytest.fixture
def full_inventory(mage: Mage) -> Inventory:
    """Inventory filled to capacity (includes the mage's starting staff)."""
    while len(mage.inventory) < mage.inventory.capacity:
        mage.inventory.add(Potion(name=f"Filler-{len(mage.inventory)}"))
    return mage.inventory


@pytest.fixture
def game_world(warrior: Warrior, mage: Mage, archer: Archer) -> GameWorld:
    """Game world with three characters and two quests."""
    world = GameWorld("Test Realm")
    world.add_character(warrior)
    world.add_character(mage)
    world.add_character(archer)

    quest_slain = Quest(
        "Slay Goblins",
        objectives=[QuestObjective("Defeat goblins", target_count=3)],
    )
    quest_herbs = Quest(
        "Gather Herbs",
        objectives=[QuestObjective("Collect herbs", target_count=2)],
    )
    world.add_quest(quest_slain)
    world.add_quest(quest_herbs)
    return world
