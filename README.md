# ⚔️ my_rpg_engine

## 1. Opis projektu

System to tekstowy silnik symulujący potyczki w realiach gier RPG, pozwalający na obserwację turowych walk pomiędzy wygenerowanymi bohaterami. Rozwiązuje on problem żmudnego, ręcznego rozliczania statystyk i rzutów kośćmi, automatyzując mechanikę starć, obliczanie obrażeń oraz zarządzanie ekwipunkiem. Z perspektywy gracza jest to interaktywne narzędzie, które w przejrzysty sposób raportuje każde wydarzenie na arenie, ułatwiając śledzenie losów poszukiwaczy przygód oraz stanu ich rynsztunku.

## 2. Autorzy i podział pracy


| Imię i Nazwisko        | Zakres odpowiedzialności                                                                                                                                                                                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Michał Głowacki**    | Lider zespołu, zarządzanie projektem i podział zadań. Opracowanie głównych założeń architektonicznych, implementacja klas abstrakcyjnych i bazowych (`Item`, `Weapon`, `Character`), systemu ekwipunku (`Inventory`) oraz mechanizmu logowania (`EventLogger`).           |
| **Szymon Grzelak**     | Implementacja mechaniki walki. Zaprogramowanie pętli starcia (klasa `Battle`), stworzenie klasy `Warrior` i przedmiotu `Sword` wraz z logiką psucia się oręża, oraz napisanie testów jednostkowych starć w frameworku pytest.                                             |
| **Mateusz Rybczyński** | Implementacja systemu magii, wzorca kreacyjnego oraz integracja. Stworzenie klasy `Mage` i przedmiotu leczniczego `Potion`, zaprogramowanie fabryki postaci (`CharacterFactory`), przygotowanie głównego skryptu symulacji (`main.py`) oraz testów jednostkowych fabryki. |


## 3. Lista klas z opisami


| Nazwa klasy        | Opis                                                                                                                                | Główne atrybuty                 | Główne metody                                                    |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- | ---------------------------------------------------------------- |
| `Item`             | Abstrakcyjna klasa bazowa dla wszystkich przedmiotów w grze. Definiuje wspólny interfejs dla rzeczy, które można posiadać i używać. | `name`                          | `__init__()`, `use()`                                            |
| `Weapon`           | Abstrakcyjna klasa bazowa dla broni palnej i białej. Wprowadza mechanikę wytrzymałości, która wpływa na efektywność przedmiotu.     | `name`, `damage`, `_durability` | `calculate_effective_damage()`, `decrease_durability()`, `use()` |
| `Sword`            | Konkretna implementacja broni białej. Służy do zadawania obrażeń fizycznych przeciwnikowi w trakcie walki.                          | Dziedziczone z `Weapon`         | `use()`                                                          |
| `Potion`           | Konkretny przedmiot użytkowy (konsumpcyjny). Służy do przywracania punktów zdrowia postaciom w krytycznych momentach.               | `heal_amount`                   | `use()`                                                          |
| `Character`        | Abstrakcyjna klasa bazowa postaci. Reprezentuje dowolną żywą jednostkę biorącą udział w symulacji, posiadającą zdrowie i ekwipunek. | `name`, `health`, `inventory`   | `__init__()`, `take_damage()`, `attack()`                        |
| `Warrior`          | Konkretna implementacja bohatera walczącego wręcz. Specjalizuje się w wykorzystywaniu broni do zadawania ciosów.                    | Dziedziczone z `Character`      | `attack()`                                                       |
| `Mage`             | Konkretna implementacja bohatera posługującego się magią. Potrafi leczyć się miksturami lub zadawać magiczne obrażenia.             | Dziedziczone z `Character`      | `attack()`                                                       |
| `Inventory`        | Zarządca ekwipunku pojedynczej postaci. Przechowuje przedmioty, pozwalając na ich dodawanie i usuwanie.                             | `_items`                        | `add_item()`, `remove_item()`, `get_items()`                     |
| `EventLogger`      | Niezależny system rejestrujący historię wydarzeń. Służy do oddzielenia warstwy informacyjnej (wyświetlania) od logiki gry.          | `_logs`                         | `log()`, `get_logs()`                                            |
| `Battle`           | Silnik pojedynczego starcia turowego. Nadzoruje przebieg walki pomiędzy dwoma bohaterami do momentu śmierci jednego z nich.         | `hero`, `enemy`, `logger`       | `run()`, `_execute_turn()`                                       |
| `CharacterFactory` | Fabryka generująca gotowych do gry bohaterów. Automatycznie przypisuje im odpowiedni sprzęt startowy.                               | Brak (metody statyczne)         | `create_warrior()`, `create_mage()`                              |


## 4. Relacje między klasami

- **Kompozycja:** Pomiędzy klasą `Character` a `Inventory`. Ekwipunek jest nierozłączną częścią bohatera – jeśli obiekt postaci zostanie usunięty lub zniszczony, jej zarządzający plecak (`Inventory`) również przestaje istnieć, ponieważ nie ma racji bytu bez właściciela.
- **Agregacja:** Pomiędzy klasą `Inventory` a `Item`. Plecak gromadzi przedmioty, jednak obiekty typu `Item` mogą istnieć niezależnie w świecie gry. Po usunięciu obiektu `Inventory`, same przedmioty nie muszą zostać usunięte z pamięci (mogą leżeć na ziemi).
- **Asocjacja:** Pomiędzy klasą `Battle` a klasami `Character`. Bitwa tymczasowo korzysta z dwóch postaci w celu przeprowadzenia interakcji (walki), ale nie jest ich właścicielem. Gdy bitwa się zakończy i obiekt `Battle` zostanie usunięty, obiekty walczących postaci (szczególnie zwycięzcy) nadal istnieją.
- **Dziedziczenie:** Klasy `Warrior` i `Mage` dziedziczą po abstrakcyjnej klasie `Character`, a `Sword` i `Potion` po `Item` (oraz `Weapon`). Klasy pochodne przejmują interfejs klas bazowych (np. atrybut `health`), ale rozbudowują je o unikalne zachowania specjalistyczne (np. różne sposoby ataku).

## 5. Planowane funkcjonalności

- Automatyczne tworzenie i inicjalizowanie postaci ze startowym rynsztunkiem na podstawie wybranego archetypu (Wojownik/Mag).
- Symulacja automatycznej walki turowej pomiędzy dwiema postaciami na zamkniętej arenie, kontynuowana aż do osiągnięcia zera punktów zdrowia przez jednego z nich.
- Zarządzanie ekwipunkiem postaci, obejmujące przechowywanie, dobywanie oraz używanie przedmiotów w trakcie walki.
- Dynamiczne śledzenie wytrzymałości uzbrojenia – obniżanie atrybutu `_durability` przy każdym ataku oraz drastyczne zmniejszenie obrażeń po zniszczeniu broni.
- Scentralizowane logowanie wszystkich wydarzeń, akcji bohaterów i zmian statystyk bez ingerencji w stan wewnętrzny modeli.

## 6. User Stories

1. Jako strateg chcę śledzić niezależny dziennik wydarzeń tekstowych z całej bitwy, żeby dokładnie przeanalizować historię wykonanych akcji i przebieg starcia bez zaglądania w kod.
2. Jako zarządca ekwipunku chcę, aby wytrzymałość broni spadała z każdym atakiem bohatera, żeby mechanika gry realistycznie symulowała zużycie sprzętu w trakcie jego używania.
3. Jako twórca symulacji chcę szybko generować gotowe postacie z domyślnym uzbrojeniem, żeby móc od razu rozpocząć testowanie pętli walki bez ręcznego tworzenia przedmiotów.

## 7. Mechanizmy OOP


| Mechanizm      | Gdzie zastosowano                                      | Opis działania                                                                     |
| -------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| **Abstrakcja** | Moduł `base.py` (klasy `Item`, `Weapon`, `Character`). | Narzuca "kontrakt" używając modułu `abc`. Metody takie jak `use()` są wymuszone za |


