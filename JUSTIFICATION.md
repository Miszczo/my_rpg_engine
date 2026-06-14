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
| Bonus obrony od poziomu | `(level - 1) * 1` | `tests/test_justification.py:test_justification_defense_level_bonus` |
| `Item.__eq__` | porównanie po `_id` | `tests/test_justification.py:test_justification_item_eq_by_id` |
| `Inventory.remove` / brak przedmiotu | `InvalidItemError` | `tests/test_justification.py:test_justification_inventory_remove_missing_item` |
| `Mage.special_attack` przy braku many | fallback `"Basic Attack"` + `attack_power` | `tests/test_justification.py:test_justification_mage_special_attack_fallback` |
| `Healer.heal_ally` przy braku many | `InsufficientStatsError` | `tests/test_characters.py:test_scenario_07_insufficient_mana_raises_error` |
| `GameWorld.add_quest` | rejestracja questów (symetria do `add_character`) | `tests/test_quest.py:test_scenario_08_gain_xp_and_level_up_via_quest` |

Reguły z kolumny „Test” są pokryte dedykowanymi testami. Pozostałe założenia (np. remis w `auto_battle`) weryfikowane przez inspekcję kodu i `demo.py`.
