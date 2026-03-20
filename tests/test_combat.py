"""
Unit tests for combat mechanics.
"""

from __future__ import annotations

from engine.base import Character
from engine.inventory import Inventory
from engine.items import Sword
from engine.logger import EventLogger
from engine.characters import Warrior
from engine.combat import Battle


def test_battle_consumes_weapon_durability_until_death() -> None:
    """Battle should reduce durability each time a weapon hits."""

    logger = EventLogger()

    hero_inventory = Inventory(logger=logger)
    hero_inventory.add_item(Sword(damage=10, durability=1))
    hero = Warrior(name="Hero", health=5, inventory=hero_inventory)

    enemy_inventory = Inventory(logger=logger)
    enemy = Warrior(name="Enemy", health=11, inventory=enemy_inventory)  # no weapon => hits for 1

    battle = Battle(hero=hero, enemy=enemy, logger=logger, hero_first=True, max_rounds=10)
    winner = battle.run()

    assert winner is hero
    assert enemy.health == 0

    sword = next(item for item in hero.inventory.items if isinstance(item, Sword))
    assert sword.durability == 0

    events = logger.get_events()
    assert any("--- Round " in e for e in events)
    assert any("attacks" in e for e in events)

