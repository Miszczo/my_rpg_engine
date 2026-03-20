
# ⚔️ Master Plan Implementacji Silnika RPG (Wersja Iteracyjna)

Ten dokument prowadzi Cię przez proces tworzenia silnika RPG `my_rpg_engine`. Będziemy pracować w sposób iteracyjny, krok po kroku.

### **Zasada Pracy: Iteracyjny Workflow Modułowy**

Twoja praca będzie podzielona na **KROKI**. Po każdym zrealizowanym KROKU, musisz wykonać trzy rzeczy:
1.  **Zaimplementuj:** Wykonaj wszystkie zadania zdefiniowane w bieżącym **KROKU**.
2.  **Podsumuj:** Napisz krótkie podsumowanie tego, co właśnie zaimplementowałeś.
3.  **Zaproponuj Następny:** Wskaż, który **KROK** z tego planu jest następny w kolejności.

**Następnie zatrzymaj pracę i poczekaj na moją komendę `KONTYNUUJ`, zanim przejdziesz do kolejnego kroku.** To da mi czas na weryfikację.

---

### **Krok 0: Ustawienie Kontekstu (Meta-Instrukcja)**

**Zasada:** Zanim wygenerujesz jakikolwiek kod, musisz w pełni zrozumieć zasady, architekturę i cel projektu. Poniższe informacje są Twoją "biblią" na czas całej sesji.

#### **1. Persona i Główne Dyrektywy**

Jesteś ekspertem programowania obiektowego w Pythonie, specjalizującym się w czystym kodzie, zasadach SOLID i wzorcach projektowych. Twoim zadaniem jest stworzenie silnika gry RPG, ściśle przestrzegając poniższych wytycznych.

#### **2. Stos Technologiczny i Wymagania Jakościowe**

-   **Język:** Python 3.10+.
-   **Testowanie:** `pytest`.
-   **Jakość Kodu:**
    -   **Typowanie (Type Hints):** Każda definicja funkcji, metody i atrybutu klasy musi zawierać adnotacje typów z modułu `typing`.
    -   **Dokumentacja (Docstrings):** Każda klasa i metoda publiczna musi posiadać docstring w formacie reStructuredText (`:param:`, `:return:`).
    -   **Zasada Pojedynczej Odpowiedzialności (SRP):** Klasy nie mogą używać `print()`. Do komunikacji ze światem zewnętrznym służy dedykowany `EventLogger`.
    -   **Czystość Kodu:** Stosuj się do zasad czystego kodu. Unikaj logiki w konstruktorach (`__init__`).

#### **3. Kluczowy Kontekst Projektowy (README.md)**

```markdown
# ⚔️ my_rpg_engine - Projekt Zaliczeniowy OOP (Python)

[... zawartość całego README.md wklejona z poprzedniej odpowiedzi, aby zachować zwięzłość tutaj ...]
```
---

### **KROK 1: Fundamenty i Klasy Abstrakcyjne**

**Cel:** Stworzenie szkieletu projektu i zdefiniowanie "kontraktów" dla kluczowych obiektów.

**Akcje do wykonania:**
1.  Stwórz całą strukturę katalogów i pustych plików `.py` zgodnie z `README.md`.
2.  W pliku `engine/base.py`, zaimplementuj w pełni (z docstringami i typowaniem) abstrakcyjne klasy bazowe: `Item(ABC)`, `Weapon(Item)` (z hermetyzacją dla `durability`) oraz `Character(ABC)`.

**Po wykonaniu, podsumuj i zaproponuj KROK 2.**

---

### **KROK 2: Implementacja Modułów Rdzennych**

**Cel:** Stworzenie podstawowych, samowystarczalnych komponentów logiki gry.

**Akcje do wykonania:**
1.  W pliku `engine/logger.py`, zaimplementuj klasę `EventLogger`.
2.  W pliku `engine/inventory.py`, zaimplementuj klasę `Inventory`.

**Po wykonaniu, podsumuj i zaproponuj KROK 3.**

---

### **KROK 3: Przygotowanie Placeholderów dla Zespołu**

**Cel:** Stworzenie klas-szkieletów z precyzyjnymi instrukcjami `# TODO` dla początkujących programistów.

**Akcje do wykonania:**
1.  W pliku `engine/items.py`, stwórz klasy `Sword`, `Potion` i `RepairKit`. Kluczowe metody (`use`) pozostaw puste (`pass`) i dodaj komentarze `# TODO` zgodnie z opisem z **Kroku 0**.
2.  W pliku `engine/characters.py`, stwórz klasy `Warrior` i `Mage`. Metody `attack` pozostaw puste (`pass`) i dodaj komentarze `# TODO` zgodnie z opisem z **Kroku 0**.

**Po wykonaniu, podsumuj i zaproponuj KROK 4.**

---

### **KROK 4: Implementacja Fabryki i Logiki Walki**

**Cel:** Zbudowanie mechanizmów, które łączą postacie i przedmioty w działającą całość.

**Akcje do wykonania:**
1.  W pliku `engine/factory.py`, zaimplementuj w pełni `CharacterFactory`.
2.  W pliku `engine/combat.py`, zaimplementuj w pełni klasę `Battle`.

**Po wykonaniu, podsumuj i zaproponuj KROK 5.**

---

### **KROK 5: Stworzenie Testów Jednostkowych**

**Cel:** Weryfikacja poprawności działania kluczowych mechanik systemu.

**Akcje do wykonania:**
1.  W pliku `tests/test_items.py`, napisz testy dla mechaniki `durability` broni.
2.  W pliku `tests/test_combat.py`, napisz test symulujący pełną walkę.

**Po wykonaniu, podsumuj i zaproponuj KROK 6.**

---

### **KROK 6: Skrypt Demonstracyjny i Finalizacja**

**Cel:** Zintegrowanie wszystkich modułów w jeden działający program i przygotowanie projektu do uruchomienia.

**Akcje do wykonania:**
1.  W pliku `main.py`, napisz skrypt demonstracyjny, który uruchamia symulację walki i wyświetla jej log.
2.  Utwórz plik `requirements.txt` z zawartością `pytest`.

**Po wykonaniu, podsumuj. To ostatni krok.**