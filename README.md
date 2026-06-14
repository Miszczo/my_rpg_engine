## ⚔️ my_rpg_engine

## 1. Opis projektu

`my_rpg_engine` to tekstowy silnik symulujący rozgrywki i potyczki w stylu gier RPG. Umożliwia tworzenie bohaterów, zarządzanie ich ekwipunkiem oraz symulację turowych starć z automatycznym rozliczaniem obrażeń i efektów. Dla użytkownika system upraszcza testowanie kombinacji postaci i przedmiotów, dostarczając czytelny, szczegółowy dziennik wydarzeń (`EventLogger`). Dodatkowo wspiera mechanikę poziomów, questów oraz degradację sprzętu, co pozwala symulować progresję i zarządzanie zasobami.

## 2. Autorzy i podział pracy

| Imię i Nazwisko        | Zakres odpowiedzialności                                                                                                                                                                                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Michał Głowacki**    | Lider zespołu: projekt architektury, implementacja klas bazowych i abstrakcyjnych (`Item`, `Weapon`, `Character`), systemu ekwipunku (`Inventory`) oraz `EventLogger`.                                                                                                  |
| **Szymon Grzelak**     | Mechanika walki: implementacja `Battle`, klasy `Warrior`, `Sword`, logiki degradacji broni oraz testów jednostkowych dotyczących starć.                                                                                                                                |
| **Mateusz Rybczyński** | System magii i integracja: implementacja `Mage`, `Potion`, fabryki postaci (`CharacterFactory`), przygotowanie skryptu symulacji oraz testów jednostkowych fabryki.                                                                                                   |

## 3. Lista klas

| Nazwa klasy / Typ     | Krótki opis (1–2 zdania)                                                                                                      | Główne atrybuty (przykłady)                                         | Główne metody (przykłady)                                               |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `Character` (ABC)     | Abstrakcyjna baza dla wszystkich postaci; przechowuje HP, poziom, XP i ekwipunek oraz wspólne mechaniki żywotności i poziomów. | `name`, `_id`, `_level`, `_xp`, `max_hp`, `_base_strength`, `inventory` | `char_class()`, `special_attack()`, `take_damage()`, `heal()`, `gain_xp()` |
| `Warrior`             | Postać walcząca wręcz o podwyższonych wartościach HP i siły; koncentruje się na atakach fizycznych.                         | dziedziczy z `Character`, zwiększone `max_hp`, `strength`            | `special_attack()` (np. `Heroic Strike`)                                  |
| `Mage`                | Postać magiczna z pulą many; wykonuje potężne ataki magiczne kosztem many.                                                   | dziedziczy z `Character`, `mana`, `max_mana`                         | `special_attack()` (np. `Fireball`), `mana` property                      |
| `Archer`              | Postać dystansowa z balansem między siłą a mobilnością; korzysta ze sprzętu dystansowego.                                     | dziedziczy z `Character`, `range`, `dexterity`                       | `special_attack()` (np. `Piercing Shot`)                                  |
| `Healer`              | Postać wsparcia z umiejętnościami leczącymi i (opcjonalnie) pulą many; może leczyć sojuszników.                                | dziedziczy z `Character`, `mana`, `heal_power`                       | `special_attack()`, `heal_ally()`                                         |
| `Item` (ABC)          | Abstrakcyjna baza dla wszystkich przedmiotów; definiuje wspólny interfejs oraz metadane przedmiotu.                           | `name`, `value`, `rarity`, `weight`, `_id`                           | `item_type()`, `use_description()`, `__repr__()`, `__eq__()`               |
| `Weapon` (ABC)        | Broń z wartością obrażeń i mechaniką wytrzymałości wpływającą na zadawane obrażenia.                                         | `damage`, `_durability`, `weight`                                    | `is_broken` property, `degrade()`, `calculate_effective_damage()`         |
| `Sword`               | Konkretna broń biała (przykładowo `Iron Sword`) z domyślnymi parametrami obrażeń.                                             | dziedziczy z `Weapon`, domyślny `damage`                              | `use()`                                                                   |
| `Staff`               | Broń magiczna typu `Staff` z dodatkowym kosztem many przy użyciu specjalnych ataków.                                         | dziedziczy z `Weapon`, `mana_cost`                                    | `use()`                                                                   |
| `Armor`               | Zbroja zwiększająca obronę; ma przypisany slot (`head`, `chest`, `legs`).                                                   | `defense`, `slot`, `weight`                                           | `equip()`, `unequip()`                                                    |
| `Potion`              | Przedmiot konsumpcyjny przywracający HP lub manę (różne typy mikstur).                                                        | `heal_amount`, `mana_restore`, `rarity`                              | `use()`                                                                   |
| `Inventory`           | Kontener przedmiotów postaci z ograniczoną pojemnością; obsługuje zakładanie sprzętu.                                       | `_items` (lista), `capacity`, `equipped_weapon`, `equipped_armor`     | `add()`, `remove()`, `equip_weapon()`, `equip_armor()`, `get_defense()`, `get_damage()`, dundery (`__len__`, `__iter__`, `__contains__`, `__getitem__`) |
| `BattleLog` (@dataclass) | Struktura zapisu pojedynczej akcji w bitwie (ułatwia audyt i testowanie).                                                  | `turn`, `attacker`, `action`, `damage`, `target`, `target_hp_after`  | (dane strukturalne; brak metod specjalnych)                                |
| `Battle`              | Silnik turowej walki między dwoma `Character`; wykonuje tury, zapisuje `BattleLog` i rozstrzyga zwycięzcę.                    | `attacker`, `defender`, `turn`, `logs`                                | `execute_turn(use_special=False)`, `auto_battle(max_turns=20)`, `__len__()` |
| `QuestObjective` (@dataclass) | Cel questa z licznikiem postępu; ułatwia agregowanie wieloetapowych zadań.                                                | `description`, `target_count`, `current_count`                       | `advance(amount=1)`                                                       |
| `Quest`               | Reprezentuje zadanie z listą `QuestObjective`, statusem i nagrodami (XP/gold).                                                 | `title`, `objectives`, `status`, `xp_reward`, `gold_reward`          | `accept()`, `complete()`, `fail()`                                       |
| `Rarity` (Enum)       | Enumeracja opisująca rzadkość przedmiotów używana przy wycenie i generowaniu dropów.                                          | wartości: `COMMON`, `UNCOMMON`, `RARE`, `EPIC`, `LEGENDARY`           | —                                                                        |
| `QuestStatus` (Enum)  | Enumeracja stanu questa.                                                                                                      | wartości: `AVAILABLE`, `ACTIVE`, `COMPLETED`, `FAILED`               | —                                                                        |
| `GameError` (wyjątek) | Bazowy wyjątek projektu; punkt rozszerzeń dla specyficznych błędów domenowych.                                                | —                                                                   | —                                                                        |
| `InventoryFullError`, `InsufficientStatsError`, `InvalidItemError` | Specjalizowane wyjątki pochodne od `GameError` używane do walidacji operacji. | —                                                                   | —                                                                        |
| `CharacterFactory`    | Fabryka upraszczająca tworzenie postaci z domyślnym ekwipunkiem i ustawieniami startowymi.                                    | (metody statyczne/fabryczne)                                         | `create_warrior()`, `create_mage()`, `create_archer()`, `create_healer()` |
| `EventLogger`         | Centralny rejestr zdarzeń i komunikatów (separacja logiki od prezentacji).                                                   | `_logs`                                                              | `log()`, `get_logs()`                                                     |
| `GameWorld`           | Warstwa wyższego poziomu łącząca postacie, questy i bitwy; zarządza życiem świata gry i interakcjami.                          | `_characters`, `_quests`, `_battles`                                | `add_character()`, `start_battle()`, `complete_quest()`, `report()`, dundery (`__getitem__`, `__contains__`, `__len__`, `__iter__`) |

## 4. Relacje między klasami

- **Kompozycja — `Character` → `Inventory`:** `Inventory` jest tworzony wewnątrz `Character` i żyje wraz z nim; usunięcie postaci powoduje utratę jej ekwipunku, ponieważ plecak nie ma sensu bez właściciela.
- **Agregacja — `Inventory` ◇→ `Item`:** `Inventory` agreguje obiekty `Item`, które mogą istnieć niezależnie (np. przedmiot rzucony na ziemię). Usunięcie `Inventory` nie musi niszczyć samych `Item`ów.
- **Asocjacja — `Battle` — `Character`:** `Battle` tymczasowo odwołuje się do dwóch `Character` w celu przeprowadzenia walki, ale nie jest ich właścicielem; po zakończeniu bitwy postacie nadal istnieją.
- **Dziedziczenie — `Character` / `Item` → klasy potomne:** Wiele klas (np. `Warrior`, `Mage`, `Sword`, `Staff`) dziedziczy po abstrakcyjnych bazach, dzieląc interfejs i specjalizując zachowania. Usunięcie klasy bazowej nie ma sensu w czasie runtime — chodzi o projektową relację typów.

Każda relacja została dobrana wg znaczenia semantycznego: kompozycja dla silnego powiązania życiowego (`Inventory` jest częścią `Character`), agregacja gdy elementy mogą żyć osobno, asocjacja dla tymczasowych interakcji i dziedziczenie dla rozszerzalności interfejsu.

## 5. Planowane funkcjonalności

- Tworzenie postaci czterech archetypów: `Warrior`, `Mage`, `Archer`, `Healer` z domyślnymi statystykami.
- System ekwipunku: dodawanie/usuwanie przedmiotów, zakładanie broni i zbroi, ograniczona pojemność (`Inventory`).
- Przedmioty: `Weapon` z degradacją (`durability`), `Armor` z bonusem do obrony, `Potion` przywracające HP/mana.
- Walka turowa: `Battle` wykonuje tury, `execute_turn()` i `auto_battle(max_turns=20)` oraz logowanie akcji w `BattleLog`.
- Special attacks: kosztowe umiejętności (`special_attack()`) różniące się między klasami; fallbacki przy braku zasobów (np. niewystarczająca mana).
- System poziomów: XP, `gain_xp()`, automatyczne awanse i bonusy do statystyk.
- Questy: `Quest` z `QuestObjective`, statusy (`QuestStatus`), mechanizmy `accept()`, `complete()`, `fail()` oraz nagrody (`xp_reward`, `gold_reward`).
- Game world: `GameWorld` do agregacji postaci, zarządzania questami i inicjowania bitew.
- Centralne logowanie zdarzeń i historii rozgrywki (`EventLogger`).

## 6. User Stories

1. Jako narrator rozgrywki chcę mieć szczegółowy dziennik (`EventLogger`) zawierający każdą akcję, żeby móc odtworzyć i przeanalizować przebieg bitwy bez manualnego śledzenia zmian stanów.
2. Jako zarządca ekwipunku chcę, aby broń traciła wytrzymałość przy użyciu i mogła się zepsuć, żeby symulacja realistycznie odzwierciedlała zużycie sprzętu i wymuszała podejmowanie decyzji o naprawie lub wymianie.
3. Jako twórca scenariuszy chcę szybko generować gotowe postacie z domyślnym uzbrojeniem przy pomocy `CharacterFactory`, żeby od razu uruchomić testy i symulacje bez ręcznego konfigurowania każdej postaci.

## 7. Mechanizmy OOP

| Mechanizm                | Gdzie (klasa/metoda)                                      | Krótkie zastosowanie                                                                                       |
| ------------------------ | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Abstrakcja**           | `Character` (metody `char_class()`, `special_attack()`)    | Wymusza wspólny interfejs dla różnych klas postaci.                                                       |
| **Enkapsulacja**         | `Weapon` (`_durability`), `Character` (`_xp`, `_level`)    | Ukrywanie stanu i kontrolowany dostęp przez property/settery i metody (walidacja, clamp HP).              |
| **Dziedziczenie**        | `Character` → `Warrior`/`Mage`/`Archer`/`Healer`           | Dziedziczenie cech i zachowań, możliwość nadpisania metod (override).                                     |
| **Polimorfizm**          | `Battle` wywołuje `attack()`/`special_attack()`            | Ta sama metoda wywoływana na różnych typach obiektów, różne implementacje realizują specyficzne zachowania. |
| **Przeciążanie operatorów / dundery** | `Inventory` (`__len__`, `__iter__`, `__contains__`, `__getitem__`) | Ułatwia użycie kolekcji jak natywnych typów Pythona (len, iteracja, sprawdzanie zawartości).               |
| **Wyjątki**              | `GameError` i podklasy (`InventoryFullError`, `InvalidItemError`) | Definiowanie i obsługa błędów domenowych, walidacja operacji i komunikacja o nieprawidłowościach.         |
| **Enumy**                | `Rarity`, `QuestStatus`                                   | Bezpieczne, czytelne i jednoznaczne reprezentowanie stałych stanów i kategorii w systemie.                |
| **Dataclasses**          | `BattleLog`, `QuestObjective`                              | Proste, deklaratywne struktury danych do zapisu stanu i logiki postępu questa/bitwy.                      |

## 8. Uruchomienie

### Wymagania

- Python 3.10+
- Zależności z pliku `requirements.txt`

### Instalacja

```bash
pip install -r requirements.txt
```

### Demo

```bash
python demo.py
```

Alternatywnie:

```bash
python main.py
```

(`main.py` deleguje do `demo.main()`.)

### Testy

```bash
pytest
```

## Historia zmian

- Zaktualizowano `README.md` (pełna przebudowa treści) w celu pełnej zgodności z `README_wytyczne.md` oraz włączenia szczegółów ze specyfikacji `Projekt_C_RPG_Game_Engine.md`.


