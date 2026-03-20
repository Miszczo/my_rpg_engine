"""
Combat engine for executing turn-based battles.
"""

from __future__ import annotations

from typing import Optional

from engine.base import Character, Weapon
from engine.logger import EventLogger


class Battle:
    """Perform a turn-based battle between two characters.

    :param hero: First participant.
    :param enemy: Second participant.
    :param logger: Optional event logger.
    :param hero_first: If True, hero attacks first.
    :param max_rounds: Safety limit to prevent infinite battles.
    """

    hero: Character
    enemy: Character
    logger: Optional[EventLogger]

    def __init__(
        self,
        hero: Character,
        enemy: Character,
        logger: Optional[EventLogger] = None,
        hero_first: bool = True,
        max_rounds: int = 1000,
    ) -> None:
        """Create a battle instance.

        :param hero: Hero character instance.
        :param enemy: Enemy character instance.
        :param logger: Optional event logger.
        :param hero_first: Whether hero attacks first.
        :param max_rounds: Maximum number of rounds to execute.
        :return: None
        """

        self.hero = hero
        self.enemy = enemy
        self.logger = logger
        self._hero_first = hero_first
        self._max_rounds = max_rounds
        self._round = 0

    def _log(self, message: str) -> None:
        """Write message to the logger if present."""

        if self.logger is not None:
            self.logger.log(message)

    def _get_primary_weapon(self, character: Character) -> Optional[Weapon]:
        """Find the first equipped weapon in the inventory.

        :param character: Character to inspect.
        :return: Weapon instance if found, otherwise None.
        """

        for item in character.inventory.items:
            if isinstance(item, Weapon):
                return item
        return None

    def _attack(self, attacker: Character, defender: Character) -> None:
        """Execute a single attack from attacker to defender.

        This method consumes durability on a weapon when available.

        :param attacker: Attacking character.
        :param defender: Defending character.
        :return: None
        """

        weapon = self._get_primary_weapon(attacker)
        if weapon is None:
            damage = 1
            defender.take_damage(damage)
            self._log(f"{attacker.name} hits {defender.name} for {damage} (no weapon)")
            return

        damage = weapon.calculate_effective_damage()
        defender.take_damage(damage)

        # Each attack consumes durability by 1.
        weapon.decrease_durability(1)

        self._log(
            f"{attacker.name} attacks {defender.name} with {weapon.name}: "
            f"damage={damage}, durability={weapon.durability}"
        )

    def execute_turn(self) -> Optional[Character]:
        """Execute one battle round (attacks from both sides).

        Hero and enemy attack sequentially. If one participant reaches
        0 health during the round, the battle ends immediately.

        :return: Winner character if battle ended, otherwise None.
        """

        if self.hero.health <= 0:
            self._log(f"{self.hero.name} is defeated.")
            return self.enemy
        if self.enemy.health <= 0:
            self._log(f"{self.enemy.name} is defeated.")
            return self.hero

        if self._round >= self._max_rounds:
            self._log("Battle stopped due to max_rounds limit.")
            return None

        self._round += 1
        self._log(f"--- Round {self._round} ---")

        if self._hero_first:
            self._attack(self.hero, self.enemy)
            if self.enemy.health <= 0:
                self._log(f"{self.enemy.name} is defeated.")
                return self.hero

            self._attack(self.enemy, self.hero)
            if self.hero.health <= 0:
                self._log(f"{self.hero.name} is defeated.")
                return self.enemy
        else:
            self._attack(self.enemy, self.hero)
            if self.hero.health <= 0:
                self._log(f"{self.hero.name} is defeated.")
                return self.enemy

            self._attack(self.hero, self.enemy)
            if self.enemy.health <= 0:
                self._log(f"{self.enemy.name} is defeated.")
                return self.hero

        return None

    def run(self) -> Optional[Character]:
        """Run the battle until completion.

        :return: Winner character, or None if stopped by max_rounds.
        """

        while True:
            winner = self.execute_turn()
            if winner is not None:
                return winner
            if self.hero.health <= 0 or self.enemy.health <= 0:
                return self.hero if self.enemy.health <= 0 else self.enemy
            if self._round >= self._max_rounds:
                return None

