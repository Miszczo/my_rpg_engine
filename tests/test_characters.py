"""Character tests mapped to specification scenarios 1, 2, 7, 9, 10, 13, 14, 15."""

import pytest

from engine.characters import Archer, Character, Healer, Mage, Warrior
from engine.exceptions import InsufficientStatsError
from engine.items import Armor, Sword


def test_scenario_01_create_characters_different_classes(
    warrior, mage, archer, healer
):
    """Scenario 1: creating characters of different classes."""
    assert isinstance(warrior, Warrior)
    assert isinstance(mage, Mage)
    assert isinstance(archer, Archer)
    assert isinstance(healer, Healer)


def test_scenario_02_base_statistics(warrior, mage, archer, healer):
    """Scenario 2: verify default base statistics."""
    assert warrior.max_hp == 120 and warrior.strength == 14 and warrior.defense == 8
    assert mage.max_hp == 80 and mage.strength == 8 and mage.defense == 5
    assert mage.mana == 100
    assert archer.max_hp == 90 and archer.strength == 12 and archer.defense == 6
    assert healer.max_hp == 100 and healer.mana == 120


def test_scenario_07_insufficient_mana_raises_error(healer, warrior):
    """Scenario 7: insufficient mana raises InsufficientStatsError."""
    healer.mana = 5
    with pytest.raises(InsufficientStatsError):
        healer.heal_ally(warrior)


def test_scenario_09_take_damage_applies_defense(warrior):
    """Scenario 9: take_damage subtracts defense from raw damage."""
    warrior.hp = warrior.max_hp
    actual = warrior.take_damage(30)
    assert actual == 22
    assert warrior.hp == warrior.max_hp - 22


def test_scenario_10_effective_attack_power_and_defense(warrior):
    """Scenario 10: attack_power and defense include equipment bonuses."""
    base_attack = warrior.attack_power
    base_defense = warrior.defense

    sword = next(item for item in warrior.inventory if isinstance(item, Sword))
    armor = Armor("Test Armor", defense=6)
    warrior.inventory.add(armor)
    warrior.inventory.equip_weapon(sword)
    warrior.inventory.equip_armor(armor)

    assert warrior.attack_power == warrior.strength + sword.damage
    assert warrior.defense == base_defense + armor.defense
    assert warrior.attack_power > base_attack


def test_scenario_13_character_string_representations(warrior):
    """Scenario 13: __str__ and __repr__ provide readable representations."""
    text = str(warrior)
    assert warrior.name in text
    assert "Warrior" in text
    assert repr(warrior).startswith("Warrior(")


def test_scenario_14_polymorphic_special_attack(warrior, mage, archer):
    """Scenario 14: polymorphism via special_attack on heterogeneous list."""
    characters: list[Character] = [warrior, mage, archer]
    results = [character.special_attack() for character in characters]

    assert results[0][0] == "Heroic Strike"
    assert results[1][0] == "Fireball"
    assert results[2][0] == "Piercing Shot"
    assert all(isinstance(damage, int) and damage > 0 for _, damage in results)


def test_scenario_15_inheritance_isinstance_issubclass():
    """Scenario 15: inheritance checks with isinstance and issubclass."""
    warrior = Warrior("Check")
    assert isinstance(warrior, Warrior)
    assert isinstance(warrior, Character)
    assert issubclass(Warrior, Character)
    assert issubclass(Mage, Character)
    assert not issubclass(Character, Warrior)
