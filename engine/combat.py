from engine.characters import Character
from engine.logger import EventLogger


class Battle:
    def __init__(self, fighter1: Character, fighter2: Character, logger: EventLogger):
        self.fighter1 = fighter1
        self.fighter2 = fighter2
        self.logger = logger

    def run(self) -> None:
        # TODO: Zaimplementuj pętlę while, w której postacie atakują się na zmianę
        # dopóki czyjeś health nie spadnie do 0.
        pass
