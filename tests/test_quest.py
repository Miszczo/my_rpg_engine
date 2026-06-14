"""Quest and GameWorld tests mapped to specification scenario 8."""

from engine.quest import Quest, QuestObjective, QuestStatus


def test_scenario_08_gain_xp_and_level_up_via_quest(game_world, warrior):
    """Scenario 8: completing a quest grants XP and triggers level-up."""
    quest = Quest(
        "Epic Task",
        xp_reward=150,
        objectives=[QuestObjective("Finish task", target_count=1)],
    )
    game_world.add_quest(quest)
    quest.accept()
    quest.objectives[0].advance()

    level_before = warrior.level
    xp_reward, gold_reward = game_world.complete_quest(quest, warrior)

    assert xp_reward == 150
    assert gold_reward > 0
    assert quest.status is QuestStatus.COMPLETED
    assert warrior.level > level_before
