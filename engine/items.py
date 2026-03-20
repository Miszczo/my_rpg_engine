from engine.base import Weapon, Item, Character


class Sword(Weapon):
    # TODO: Zaimplementuj konstruktor (__init__) i wywołaj super() z odpowiednimi parametrami

    def use(self, target: Character) -> None:
        # TODO: Zaimplementuj logikę ataku mieczem
        pass


class Potion(Item):
    # TODO: Zaimplementuj konstruktor

    def use(self, target: Character) -> None:
        # TODO: Zaimplementuj logikę leczenia postaci
        pass
