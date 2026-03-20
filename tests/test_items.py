"""
Unit tests for item mechanics.
"""

from __future__ import annotations

from engine.items import Sword


def test_sword_effective_damage_with_zero_durability() -> None:
    """When durability is 0, effective damage degrades to minimum."""

    sword = Sword(damage=10, durability=0)
    assert sword.durability == 0
    assert sword.calculate_effective_damage() == Sword.MIN_DAMAGE


def test_sword_durability_decrease_is_clamped() -> None:
    """Durability should never go below 0."""

    sword = Sword(damage=10, durability=2)
    sword.decrease_durability(1)
    assert sword.durability == 1

    sword.decrease_durability(5)
    assert sword.durability == 0
    assert sword.calculate_effective_damage() == Sword.MIN_DAMAGE

