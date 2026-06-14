"""Game world orchestration for characters, quests, and battles."""

from __future__ import annotations

from collections.abc import Iterator

from engine.characters import Character
from engine.combat import Battle
from engine.exceptions import GameError
from engine.quest import Quest


class GameWorld:
    """High-level container managing characters, quests, and battle history."""

    def __init__(self, name: str = "Realm of AHE") -> None:
        """Create an empty game world.

        Args:
            name: Display name of the world.
        """
        self.name = name
        self._characters: dict[int, Character] = {}
        self._quests: dict[int, Quest] = {}
        self._battles: list[Battle] = []

    def add_character(self, character: Character) -> None:
        """Register a character in the world by its id.

        Args:
            character: Character instance to register.

        Raises:
            GameError: If a character with the same id is already registered.
        """
        if character._id in self._characters:
            raise GameError(
                f"Character with id {character._id} is already registered."
            )
        self._characters[character._id] = character

    def add_quest(self, quest: Quest) -> None:
        """Register a quest in the world by its id.

        Args:
            quest: Quest instance to register.

        Raises:
            GameError: If a quest with the same id is already registered.
        """
        if quest._id in self._quests:
            raise GameError(f"Quest with id {quest._id} is already registered.")
        self._quests[quest._id] = quest

    def start_battle(self, attacker: Character, defender: Character) -> Battle:
        """Create and record a battle between two registered characters.

        Args:
            attacker: Character who acts first.
            defender: Character who defends first.

        Returns:
            The created ``Battle`` instance.

        Raises:
            GameError: If either character is not registered in this world.
        """
        self._ensure_character_registered(attacker)
        self._ensure_character_registered(defender)
        battle = Battle(attacker, defender)
        self._battles.append(battle)
        return battle

    def complete_quest(
        self, quest: Quest, character: Character
    ) -> tuple[int, int]:
        """Complete a quest and grant XP to the character.

        Args:
            quest: Quest to complete.
            character: Character receiving quest rewards.

        Returns:
            Tuple of ``(xp_reward, gold_reward)`` from the quest.

        Raises:
            GameError: If the quest or character is not registered in this world.
        """
        self._ensure_quest_registered(quest)
        self._ensure_character_registered(character)
        xp_reward, gold_reward = quest.complete()
        character.gain_xp(xp_reward)
        return (xp_reward, gold_reward)

    def report(self) -> str:
        """Return a text summary of the world state."""
        lines = [
            f"World: {self.name}",
            f"Characters ({len(self._characters)}):",
        ]
        for character in self._characters.values():
            lines.append(f"  - {character}")
        lines.append(f"Quests ({len(self._quests)}):")
        for quest in self._quests.values():
            lines.append(f"  - {quest.title} [{quest.status.value}]")
        lines.append(f"Battles fought: {len(self._battles)}")
        return "\n".join(lines)

    def __getitem__(self, char_id: int) -> Character:
        """Return a registered character by id."""
        try:
            return self._characters[char_id]
        except KeyError as exc:
            raise GameError(
                f"No character registered with id {char_id}."
            ) from exc

    def __contains__(self, obj: object) -> bool:
        """Return True when a character or quest is registered in this world."""
        if isinstance(obj, Character):
            return obj._id in self._characters
        if isinstance(obj, Quest):
            return obj._id in self._quests
        return False

    def __len__(self) -> int:
        """Return the number of registered characters."""
        return len(self._characters)

    def __iter__(self) -> Iterator[Character]:
        """Iterate over registered characters."""
        return iter(self._characters.values())

    def _ensure_character_registered(self, character: Character) -> None:
        if character._id not in self._characters:
            raise GameError(
                f"Character {character.name!r} is not registered in this world."
            )

    def _ensure_quest_registered(self, quest: Quest) -> None:
        if quest._id not in self._quests:
            raise GameError(
                f"Quest {quest.title!r} is not registered in this world."
            )
