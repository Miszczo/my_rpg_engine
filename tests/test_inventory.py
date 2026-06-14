"""Inventory tests mapped to specification scenarios 3, 4, 5, 12."""

import pytest

from engine.exceptions import InvalidItemError, InventoryFullError
from engine.items import Armor, Potion, Sword


def test_scenario_03_equip_and_remove_items(warrior):
    """Scenario 3: equipping and removing items from inventory."""
    sword = next(item for item in warrior.inventory if isinstance(item, Sword))
    armor = Armor("Chain Mail", defense=4)

    warrior.inventory.add(armor)
    warrior.inventory.equip_weapon(sword)
    warrior.inventory.equip_armor(armor)

    assert warrior.inventory.equipped_weapon is sword
    assert warrior.inventory.equipped_armor is armor

    warrior.inventory.remove(armor)
    assert armor not in warrior.inventory
    assert warrior.inventory.equipped_armor is None


def test_scenario_04_stats_change_after_equipping(warrior):
    """Scenario 4: equipping items changes effective combat stats."""
    sword = next(item for item in warrior.inventory if isinstance(item, Sword))
    armor = Armor("Plate", defense=5)
    warrior.inventory.add(armor)

    attack_before = warrior.attack_power
    defense_before = warrior.defense

    warrior.inventory.equip_weapon(sword)
    warrior.inventory.equip_armor(armor)

    assert warrior.attack_power == attack_before + sword.damage
    assert warrior.defense == defense_before + armor.defense


def test_scenario_05_full_inventory_raises_inventory_full_error(full_inventory):
    """Scenario 5: adding to a full inventory raises InventoryFullError."""
    with pytest.raises(InventoryFullError):
        full_inventory.add(Potion(name="Overflow"))


def test_scenario_12_invalid_equip_raises_invalid_item_error(warrior):
    """Scenario 12: invalid equip operations raise InvalidItemError."""
    potion = Potion()
    warrior.inventory.add(potion)

    with pytest.raises(InvalidItemError):
        warrior.inventory.equip_weapon(potion)

    outside_sword = Sword()
    with pytest.raises(InvalidItemError):
        warrior.inventory.equip_weapon(outside_sword)
