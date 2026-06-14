"""Demonstration script for the RPG engine (spec sections 2.5 and 4)."""

from __future__ import annotations

from engine.characters import Character, Mage, Healer
from engine.combat import Battle
from engine.exceptions import InventoryFullError
from engine.factory import CharacterFactory
from engine.game_world import GameWorld
from engine.items import Armor, Potion, Sword
from engine.logger import EventLogger
from engine.quest import Quest, QuestObjective


def _log_character_stats(logger: EventLogger, character: Character, label: str) -> None:
    """Log core stats for a character."""
    parts = [
        f"{label}: {character}",
        f"STR={character.strength}",
        f"DEF={character.defense}",
        f"ATK={character.attack_power}",
    ]
    if isinstance(character, (Mage, Healer)):
        parts.append(f"MANA={character.mana}/{character.max_mana}")
    logger.log(" | ".join(parts))


def _log_battle(logger: EventLogger, battle: Battle, winner: Character) -> None:
    """Log structured battle entries and the resolved winner."""
    for entry in battle.logs:
        logger.log(
            f"Turn {entry.turn}: {entry.attacker} -> {entry.action} -> "
            f"{entry.target} ({entry.damage} dmg, HP={entry.target_hp_after})"
        )
    logger.log(f"Winner: {winner.name} ({winner.char_class()})")


def main() -> None:
    """Run demonstration scenarios from the project specification."""
    logger = EventLogger()
    world = GameWorld()

    logger.log("=== 1. Creating characters ===")
    warrior = CharacterFactory.create_warrior("Conan")
    mage = CharacterFactory.create_mage("Merlin")
    archer = CharacterFactory.create_archer("Legolas")
    for character in (warrior, mage, archer):
        world.add_character(character)

    logger.log("=== 2. Initial statistics ===")
    for character in (warrior, mage, archer):
        _log_character_stats(logger, character, character.name)

    logger.log("=== 3. Equipping items ===")
    _log_character_stats(logger, warrior, f"{warrior.name} before equip")
    sword = next(item for item in warrior.inventory if isinstance(item, Sword))
    warrior.inventory.equip_weapon(sword)
    armor = Armor("Leather Vest", defense=5)
    warrior.inventory.add(armor)
    warrior.inventory.equip_armor(armor)
    _log_character_stats(logger, warrior, f"{warrior.name} after equip")

    logger.log("=== 4. Full inventory exception ===")
    filler = CharacterFactory.create_mage("Packrat")
    while len(filler.inventory) < filler.inventory.capacity:
        filler.inventory.add(Potion(name=f"Filler #{len(filler.inventory) + 1}"))
    try:
        filler.inventory.add(Potion(name="Overflow Potion"))
    except InventoryFullError as exc:
        logger.log(f"Expected InventoryFullError: {exc}")

    logger.log("=== 5. Turn-based battle (with potion mid-fight) ===")
    battle_potion = Potion(name="Battle Flask", heal_amount=40)
    warrior.inventory.add(battle_potion)
    battle = world.start_battle(warrior, mage)

    for turn_index in range(6):
        if warrior.hp <= 0 or mage.hp <= 0:
            break
        use_special = battle.attacker is mage
        battle.execute_turn(use_special=use_special)

    if warrior.hp < warrior.max_hp:
        potion_name = battle_potion.name
        healed = warrior.use_potion(battle_potion)
        logger.log(
            f"Mid-battle: {warrior.name} used {potion_name}, "
            f"healed {healed} HP (now {warrior.hp}/{warrior.max_hp})"
        )

    winner = battle.auto_battle(max_turns=20)
    _log_battle(logger, battle, winner)

    logger.log("=== 6. Experience and level up ===")
    level_before = warrior.level
    leveled_up = warrior.gain_xp(150)
    logger.log(
        f"{warrior.name}: level {level_before} -> {warrior.level}, "
        f"leveled_up={leveled_up}"
    )

    logger.log("=== 7. Polymorphism - special_attack on heterogeneous list ===")
    party: list[Character] = [warrior, mage, archer]
    for character in party:
        action, damage = character.special_attack()
        logger.log(
            f"{character.name} ({character.char_class()}): "
            f"{action} -> {damage} dmg"
        )

    logger.log("=== 8. Quest lifecycle ===")
    quest = Quest(
        "Defeat the Bandits",
        objectives=[QuestObjective("Defeat bandits", target_count=2)],
        xp_reward=100,
        gold_reward=50,
    )
    world.add_quest(quest)
    quest.accept()
    logger.log(f"Quest accepted: {quest.title} [{quest.status.value}]")
    quest.objectives[0].advance(2)
    mage_level_before = mage.level
    xp_reward, gold_reward = world.complete_quest(quest, mage)
    logger.log(
        f"Quest completed: +{xp_reward} XP, +{gold_reward} gold, "
        f"{mage.name} level {mage_level_before} -> {mage.level}"
    )

    logger.log("=== World report ===")
    logger.log(world.report())

    print("\n".join(logger.get_events()))


if __name__ == "__main__":
    main()
