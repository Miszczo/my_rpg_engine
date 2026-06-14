"""Turn-based battle system with structured battle logs."""

from __future__ import annotations

from dataclasses import dataclass

from engine.characters import Character
from engine.exceptions import GameError


@dataclass
class BattleLog:
    """Structured record of a single battle action."""

    turn: int
    attacker: str
    action: str
    damage: int
    target: str
    target_hp_after: int


class Battle:
    """Turn-based combat between two characters."""

    _next_id: int = 1

    def __init__(self, attacker: Character, defender: Character) -> None:
        """Start a battle between two distinct characters.

        Args:
            attacker: Character who acts first.
            defender: Character who defends first.

        Raises:
            GameError: If ``attacker`` and ``defender`` are the same instance.
        """
        if attacker is defender:
            raise GameError("Attacker and defender cannot be the same character.")
        self._id = Battle._next_id
        Battle._next_id += 1
        self.attacker = attacker
        self.defender = defender
        self._fighters = (attacker, defender)
        self._turn = 1
        self.logs: list[BattleLog] = []

    @property
    def id(self) -> int:
        """Unique identifier assigned at creation time."""
        return self._id

    def execute_turn(self, use_special: bool = False) -> None:
        """Execute one turn: attack, log the result, then swap roles.

        Args:
            use_special: When True, the attacker uses ``special_attack()``
                instead of a basic attack.
        """
        if use_special:
            action, raw_damage = self.attacker.special_attack()
        else:
            action = "Attack"
            raw_damage = self.attacker.attack_power
            self._degrade_attacker_weapon()

        actual_damage = self.defender.take_damage(raw_damage)
        self.logs.append(
            BattleLog(
                turn=self._turn,
                attacker=self.attacker.name,
                action=action,
                damage=actual_damage,
                target=self.defender.name,
                target_hp_after=self.defender.hp,
            )
        )
        self.attacker, self.defender = self.defender, self.attacker
        self._turn += 1

    def auto_battle(self, max_turns: int = 20) -> Character:
        """Run turns automatically until one fighter falls or ``max_turns`` is reached.

        Args:
            max_turns: Maximum number of turns to execute.

        Returns:
            The winning character. If both survive after ``max_turns``, the
            one with higher HP wins; equal HP returns the initial attacker.
        """
        for _ in range(max_turns):
            if self.attacker.hp <= 0 or self.defender.hp <= 0:
                break
            self.execute_turn()

        return self._determine_winner()

    def __len__(self) -> int:
        return len(self.logs)

    def _degrade_attacker_weapon(self) -> None:
        """Reduce durability of the attacker's equipped weapon after a basic attack."""
        weapon = self.attacker.inventory.equipped_weapon
        if weapon is not None:
            weapon.degrade()

    def _determine_winner(self) -> Character:
        """Resolve the battle winner from the two combatants."""
        fighter_a, fighter_b = self._fighters

        if fighter_a.hp <= 0 and fighter_b.hp <= 0:
            return fighter_a if fighter_a.hp >= fighter_b.hp else fighter_b
        if fighter_a.hp <= 0:
            return fighter_b
        if fighter_b.hp <= 0:
            return fighter_a
        if fighter_a.hp > fighter_b.hp:
            return fighter_a
        if fighter_b.hp > fighter_a.hp:
            return fighter_b
        return fighter_a
