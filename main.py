"""
Demo entrypoint for the RPG engine.

This script runs a short battle simulation and outputs the event log.
"""

from __future__ import annotations

from typing import Optional

from engine.combat import Battle
from engine.factory import CharacterFactory
from engine.logger import EventLogger


def run_demo(
    hero_type: str = "warrior",
    enemy_type: str = "mage",
    hero_name: str = "Hero",
    enemy_name: str = "Enemy",
    log_path: str = "battle_log.txt",
) -> Optional[str]:
    """Run a short battle demo and return the winner name.

    :param hero_type: Type of hero character (e.g., ``"warrior"``).
    :param enemy_type: Type of enemy character (e.g., ``"mage"``).
    :param hero_name: Name of hero.
    :param enemy_name: Name of enemy.
    :param log_path: File path for saving the battle log.
    :return: Winner name, or ``None`` if battle stopped without winner.
    """

    logger = EventLogger()
    factory = CharacterFactory(logger=logger)

    hero = factory.create_character(char_type=hero_type, name=hero_name)
    enemy = factory.create_character(char_type=enemy_type, name=enemy_name)

    battle = Battle(hero=hero, enemy=enemy, logger=logger, hero_first=True, max_rounds=100)
    winner = battle.run()

    logger.save_to_file(path=log_path)

    # Printing is allowed outside engine classes (demo-only).
    for event in logger.get_events():
        print(event)

    if winner is None:
        print("No winner (battle stopped).")
        return None

    print(f"Winner: {winner.name}")
    return winner.name


def main() -> None:
    """Program entrypoint."""

    run_demo()


if __name__ == "__main__":
    main()

