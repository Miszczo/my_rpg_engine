"""Item tests mapped to specification scenario 11."""

from engine.items import Item, Potion, Rarity, Sword


def test_scenario_11_item_comparison_dunder_methods():
    """Scenario 11: item comparison via __eq__ and __lt__."""
    cheap = Potion(name="Minor Potion", value=10)
    expensive = Sword(name="Steel Sword", value=50)
    duplicate_id = cheap

    assert cheap == duplicate_id
    assert cheap != expensive
    assert cheap < expensive
    assert sorted([expensive, cheap], key=lambda item: item.value)[0] is cheap
    assert issubclass(Sword, Item)
    assert cheap.rarity is Rarity.COMMON
