"""Tests for implementation rules documented in JUSTIFICATION.md §4."""

import pytest

from engine.exceptions import InvalidItemError
from engine.items import Potion, Sword


def test_justification_defense_level_bonus(warrior):
    """Defense increases by 1 per level above 1 (JUSTIFICATION §4)."""
    base_defense = warrior.defense
    warrior.gain_xp(warrior.XP_PER_LEVEL)
    assert warrior.level == 2
    assert warrior.defense == base_defense + 1


def test_justification_item_eq_by_id():
    """Item equality is based on unique _id, not value or name (JUSTIFICATION §4)."""
    first = Potion(name="Alpha", value=10)
    second = Potion(name="Alpha", value=10)
    third = Sword(name="Beta", value=10)

    assert first == first
    assert first.id != second.id
    assert first != second
    assert first != third


def test_justification_inventory_remove_missing_item(warrior):
    """Removing an item not in inventory raises InvalidItemError (JUSTIFICATION §4)."""
    outside_potion = Potion(name="Not In Bag")
    with pytest.raises(InvalidItemError):
        warrior.inventory.remove(outside_potion)


def test_justification_mage_special_attack_fallback(mage):
    """Mage falls back to Basic Attack when mana is below Fireball cost (JUSTIFICATION §4)."""
    mage.mana = 10
    mana_before = mage.mana
    action, damage = mage.special_attack()

    assert action == "Basic Attack"
    assert damage == mage.attack_power
    assert mage.mana == mana_before
