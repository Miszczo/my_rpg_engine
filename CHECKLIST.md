# CHECKLIST — mechanizmy OOP

> Lokalizacje: `plik:metoda` lub `plik:linia`. Zgodnie z sekcją 6.1 specyfikacji projektu.

## Podstawy klas

- [x] **Klasy i obiekty** — `engine/characters.py:Warrior`, `engine/items.py:Sword`, `demo.py:main`
- [x] **Konstruktor `__init__`** — `engine/characters.py:Character.__init__`, `engine/inventory.py:Inventory.__init__`
- [x] **Atrybuty instancji** — `engine/characters.py` (`_hp`, `_base_strength`), `engine/items.py` (`name`, `value`)
- [x] **Atrybuty klasy** — `engine/characters.py:Character._next_id`, `engine/items.py:Item._next_id`, `engine/combat.py:Battle._next_id`
- [x] **Metody instancji** — `engine/characters.py:take_damage`, `engine/inventory.py:add`, `engine/quest.py:Quest.accept`

## Enkapsulacja i metody specjalne

- [x] **Prywatne atrybuty (`_`)** — `engine/characters.py:_hp`, `engine/items.py:_durability`, `engine/inventory.py:_items`
- [x] **`@property` gettery** — `engine/characters.py:hp`, `engine/items.py:Weapon.durability`, `engine/inventory.py:equipped_weapon`
- [x] **`@property.setter`** — `engine/characters.py:hp.setter`, `engine/characters.py:Mage.mana.setter`, `engine/items.py:Weapon.durability.setter`
- [x] **`__str__()`** — `engine/characters.py:Character.__str__`
- [x] **`__repr__()`** — `engine/characters.py:Character.__repr__`, `engine/items.py:Item.__repr__`, `engine/quest.py:Quest.__repr__`
- [x] **`__eq__()`** — `engine/characters.py:Character.__eq__`, `engine/items.py:Item.__eq__`
- [x] **Dodatkowe dundery** — `engine/items.py:Item.__lt__`, `engine/inventory.py:__len__/__iter__/__contains__/__getitem__`, `engine/game_world.py:__getitem__/__contains__/__len__/__iter__`

## Dziedziczenie

- [x] **Klasa bazowa** — `engine/characters.py:Character`, `engine/items.py:Item`
- [x] **Klasy pochodne (≥3 + ≥3)** — Character: `Warrior`, `Mage`, `Archer`, `Healer`; Item: `Weapon`, `Armor`, `Potion` (+ `Sword`, `Staff`)
- [x] **`super()`** — `engine/characters.py:Warrior.__init__`, `engine/items.py:Sword.__init__`
- [x] **Override metody** — `engine/characters.py:Warrior.special_attack`
- [x] **`isinstance` / `issubclass`** — `tests/test_characters.py:test_scenario_15_inheritance_isinstance_issubclass`

## Polimorfizm

- [x] **Polimorfizm** — `engine/characters.py` (`special_attack` w 4 podklasach), `tests/test_characters.py:test_scenario_14_polymorphic_special_attack`
- [x] **Duck typing** — `tests/test_characters.py:test_scenario_14_polymorphic_special_attack` (lista `Character`)

## Kompozycja i agregacja

- [x] **Kompozycja** — `engine/characters.py:Character.__init__` tworzy `Inventory`
- [x] **Agregacja** — `engine/inventory.py:Inventory._items` przechowuje referencje do `Item`

## Klasy abstrakcyjne i operatory

- [x] **Klasa abstrakcyjna (ABC)** — `engine/characters.py:Character`, `engine/items.py:Item`
- [x] **`@abstractmethod`** — `engine/characters.py:char_class`, `engine/items.py:item_type`
- [x] **Przeciążanie operatorów** — `engine/items.py:Item.__lt__` (operator `<`)

## Wyjątki

- [x] **Własny wyjątek bazowy** — `engine/exceptions.py:GameError`
- [x] **Hierarchia (≥2 specjalizowane)** — `InventoryFullError`, `InsufficientStatsError`, `InvalidItemError`
- [x] **`raise` w metodach** — `engine/inventory.py:add`, `engine/characters.py:Healer.heal_ally`
- [x] **Obsługa `try-except`** — `demo.py:main` (scenario 4, `InventoryFullError`)

## Testowanie i dokumentacja

- [x] **Testy pytest (15)** — `tests/test_*.py` (15 funkcji `test_scenario_*`)
- [x] **Docstringi** — wszystkie publiczne klasy/metody w `engine/`
- [x] **Type hints** — parametry i zwracane typy w `engine/`
