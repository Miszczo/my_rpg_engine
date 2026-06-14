"""Combat tests mapped to specification scenario 6."""

from engine.combat import Battle, BattleLog


def test_scenario_06_special_attack_in_battle(warrior, mage):
    """Scenario 6: special_attack used through execute_turn in battle."""
    battle = Battle(warrior, mage)
    battle.execute_turn(use_special=True)

    assert len(battle) == 1
    log = battle.logs[0]
    assert isinstance(log, BattleLog)
    assert log.action == "Heroic Strike"
    assert log.damage >= 0
    assert log.target == mage.name
