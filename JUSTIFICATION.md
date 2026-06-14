# JUSTIFICATION — decyzje projektowe

## 1. Pakiet `engine/` zamiast `src/game/` ze specyfikacji §9

Specyfikacja sugeruje strukturę `src/game/`, lecz repozytorium było już zorganizowane wokół pakietu `engine/` (Etap 2 szkieletu). Migracja katalogu zwiększałaby ryzyko regresji importów, ścieżek testów i dokumentacji zespołu bez korzyści funkcjonalnych.

**Decyzja:** zachowano `engine/` jako pakiet roboczy z mapowaniem 1:1 modułów do specyfikacji:

| Spec (§9)     | Implementacja        |
|---------------|----------------------|
| `exceptions.py` | `engine/exceptions.py` |
| `items.py`    | `engine/items.py`    |
| `inventory.py`| `engine/inventory.py`|
| `characters.py` | `engine/characters.py` |
| `battle.py`   | `engine/combat.py`   |
| `quest.py`    | `engine/quest.py`    |
| `game_world.py` | `engine/game_world.py` |

**Rozszerzenia poza szkieletem §3** (nie zmieniają API specyfikacji):

| Moduł | Rola |
|-------|------|
| `engine/factory.py` | `CharacterFactory` — szybkie tworzenie postaci z domyślnym ekwipunkiem (demo, testy) |
| `engine/logger.py` | `EventLogger` — formatowanie outputu w warstwie prezentacji |

Publiczne API pozostaje spójne ze specyfikacją §3 (nazwy metod: `hp`, `special_attack`, `add`, `execute_turn` itd.).

**Nazwa `combat.py` zamiast `battle.py`:** moduł powstał w Etapie 2 pod nazwą `combat.py` (mechanika walki). Klasa wewnątrz nadal nazywa się `Battle`, zgodnie ze specyfikacją. Zmiana nazwy pliku nie wnosiłaby korzyści funkcjonalnych, a wymagałaby aktualizacji importów w całym projekcie.

## 2. `EventLogger` wyłącznie w warstwie prezentacji

Specyfikacja Etapu 2 wiązała logowanie z metodami domenowymi (`attack(..., logger)`). W refaktoryzacji `EventLogger` (`engine/logger.py`) służy **wyłącznie** do formatowania outputu w `demo.py` — po wykonaniu logiki przez obiekty domenowe (`Battle.logs`, `GameWorld.report()`).

**Uzasadnienie (SRP):** silnik gry nie zależy od sposobu prezentacji (konsola, plik, GUI). Testy jednostkowe weryfikują logikę bez loggera; demo składa wynik w czytelny raport.

## 3. Rozstrzyganie remisu w `Battle.auto_battle()`

Gdy po `max_turns` obie postacie żyją, zwycięzca jest wybierany według kolejności:

1. Postać z HP > 0 wygrywa nad pokonaną (HP ≤ 0).
2. Jeśli obie żyją — wygrywa ta z **wyższym HP**.
3. Przy identycznym HP — zwracany jest **początkowy atakujący** (`fighter_a` z konstruktora).

Implementacja: `engine/combat.py:Battle._determine_winner`.

## 4. Założenia implementacyjne poza szkieletem §3

| Obszar | Przyjęta reguła | Test |
|--------|-----------------|------|
| Bonus obrony od poziomu | `(level - 1) * 1` | `tests/test_quest.py:test_scenario_08_gain_xp_and_level_up_via_quest` |
| `Item.__eq__` | porównanie po `_id` | `tests/test_items.py:test_scenario_11_item_comparison_dunder_methods` |
| `Inventory.remove` / brak przedmiotu | `InvalidItemError` | `tests/test_inventory.py:test_scenario_12_invalid_equip_raises_invalid_item_error` |
| `Mage.special_attack` przy braku many | fallback `"Basic Attack"` + `attack_power` | `tests/test_characters.py:test_scenario_07_insufficient_mana_raises_error` |
| `Staff.mana_cost` vs `Mage.FIREBALL_COST` | `mana_cost` na `Staff` to metadane przedmiotu (`use_description`); koszt Fireball w walce pochodzi ze stałej klasy `Mage` (25), zgodnie z pytaniem obrony §4.17 | (inspekcja kodu: `engine/characters.py:Mage.special_attack`) |
| `Healer.heal_ally` przy braku many | `InsufficientStatsError` | `tests/test_characters.py:test_scenario_07_insufficient_mana_raises_error` |
| `GameWorld.add_quest` | rejestracja questów (symetria do `add_character`) | `tests/test_quest.py:test_scenario_08_gain_xp_and_level_up_via_quest` |

Reguły z kolumny „Test” są pokryte dedykowanymi testami. Pozostałe założenia (np. remis w `auto_battle`) weryfikowane przez inspekcję kodu i `demo.py`.

## 5. `CharacterFactory` — fabryka postaci

Specyfikacja §3 nie przewiduje fabryki; postacie tworzone są bezpośrednio (`Warrior("Conan")`). W demo i testach powtarzała się jednak ta sama konfiguracja startowa (postaci + domyślny ekwipunek), co prowadziło do duplikacji kodu.

**Decyzja:** dodano `CharacterFactory` (`engine/factory.py`) ze statycznymi metodami `create_warrior()`, `create_mage()`, `create_archer()`, `create_healer()`. Fabryka:

- nie zastępuje konstruktorów klas postaci — nadal można tworzyć obiekty bezpośrednio;
- upraszcza `demo.py` i fixture'y testowe (`tests/conftest.py`);
- nie zmienia publicznego API wymaganego w §3 (metody domenowe pozostają na `Character`).

**Uzasadnienie (DRY + czytelność demo):** jeden punkt tworzenia „gotowych” postaci do symulacji, bez mieszania logiki ekwipunku z logiką walki.

## 6. `GameWorld.add_quest()` — rejestracja questów

Szkielet §3 definiuje `GameWorld.complete_quest(quest, character)`, ale nie metodę rejestracji questów. Bez jawnej rejestracji quest nie jest częścią świata gry, a `report()` nie mógłby go uwzględnić.

**Decyzja:** dodano `add_quest(quest)` jako symetrię do `add_character()` — quest otrzymuje identyfikator w `_quests`, co umożliwia:

- spójne zarządzanie obiektami w `GameWorld` (dundery, `report()`);
- pełny cykl questa w `demo.py` (utworzenie → `add_quest` → `accept` → `complete_quest`);
- test scenariusza 8 (`tests/test_quest.py`).

Publiczne API §3 (`accept`, `complete`, `fail` na `Quest`) pozostaje niezmienione; `add_quest` to rozszerzenie warstwy orkiestracji, nie logiki questa.

## 7. Brak `__hash__` przy zdefiniowanym `__eq__`

Klasy `Character` i `Item` definiują `__eq__` porównując unikalne `_id`, lecz **nie** implementują `__hash__`.

**Uzasadnienie:**

- obiekty są **mutowalne** (HP, durability, poziom, stan ekwipunku);
- po nadpisaniu `__eq__` bez `__hash__` Python ustawia `__hash__ = None` — obiekty stają się niehashowalne;
- celowo **nie** używamy postaci ani przedmiotów jako kluczy słownika ani elementów `set`; identyfikacja w logice gry odbywa się przez `_id` lub referencję obiektu.

**Odpowiedź do obrony:** `__eq__` określa, kiedy dwa obiekty są logicznie równe, a `__hash__` pozwala używać ich w strukturach haszujących, takich jak `set` i klucze `dict`. Jeżeli klasa nadpisuje `__eq__`, ale obiekty są mutowalne, bezpieczniej nie definiować `__hash__`, bo zmienny stan mógłby naruszyć kontrakt struktur haszujących. W tym projekcie `Character` i `Item` są porównywane po stabilnym `_id`, ale pozostają mutowalne, dlatego świadomie pozostają niehashowalne.

Implementacja: `engine/characters.py:Character.__eq__`, `engine/items.py:Item.__eq__`.

## 8. Jeden aktywny `Armor` w `Inventory`

`Armor` waliduje slot (`head`, `chest`, `legs`), ale `Inventory` przechowuje jeden aktywny pancerz w `_equipped_armor`.

**Uzasadnienie:** wymagane API specyfikacji definiuje `equip_armor()` oraz `get_defense()` jako prostą sumę bonusu z założonego sprzętu, bez obowiązku równoczesnego wyposażenia wielu slotów. Slot pozostaje walidowanym metadatum przedmiotu i przygotowuje model pod ewentualne rozszerzenie, ale obecna wersja celowo ogranicza mechanikę do jednego aktywnego armor, żeby utrzymać projekt edukacyjny w czytelnej formie.

Implementacja: `engine/items.py:Armor.__init__`, `engine/inventory.py:Inventory.equip_armor`, `engine/inventory.py:Inventory.get_defense`.
