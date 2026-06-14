"""Combat tests mapped to specification scenario 6."""

import pytest

from engine.characters import Mage, Warrior
from engine.combat import Battle, BattleLog
from engine.exceptions import GameError


def test_scenario_06_special_attack_in_battle(
    warrior: Warrior, mage: Mage
) -> None:
    """Scenario 6: special_attack used through execute_turn in battle."""
    battle = Battle(warrior, mage)
    battle.execute_turn(use_special=True)

    assert len(battle) == 1
    log = battle.logs[0]
    assert isinstance(log, BattleLog)
    assert log.action == "Heroic Strike"
    assert log.damage >= 0
    assert log.target == mage.name

    with pytest.raises(GameError):
        Battle(warrior, warrior)

    capped_battle = Battle(mage, warrior)
    winner = capped_battle.auto_battle(max_turns=3)
    assert winner in (mage, warrior)
    assert len(capped_battle) <= 3
