from engine.base import Character
from engine.logger import EventLogger


class Warrior(Character):
    def attack(self, target: Character, logger: EventLogger) -> None:
        # TODO: Zaimplementuj atak wojownika. Pamiętaj o logger.log(),
        # zużyciu durability broni i zadaniu obrażeń (take_damage)
        pass


class Mage(Character):
    def attack(self, target: Character, logger: EventLogger) -> None:
        # TODO: Zaimplementuj atak maga (lub użycie przedmiotu). Pamiętaj o loggerze!
        pass
