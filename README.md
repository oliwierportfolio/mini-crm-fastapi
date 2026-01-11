# Mini CRM – FastAPI

Prosty backendowy projekt CRM napisany w Pythonie z użyciem FastAPI oraz SQLAlchemy. Projekt powstał jako część portfolio i skupia się na logice biznesowej, strukturze API oraz pracy z bazą danych.

---

## Technologie

* Python 3
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* bcrypt
* JWT (przygotowane – w trakcie rozwoju)

---

## Funkcjonalności

* Dodawanie leadów
* Pobieranie listy leadów
* Filtrowanie leadów po statusie oraz ID
* Zmiana statusu leada z walidacją logiki biznesowej
   np. status `client` możliwy tylko po `meeting`
* Historia zmian statusów leadów
* Obsługa użytkowników
* Role użytkowników (admin)
* Hashowanie haseł użytkowników (bcrypt)
* REST API
* Automatyczna dokumentacja API (Swagger / OpenAPI)

---

## Interfejs użytkownika (demo)

Projekt zawiera prosty interfejs HTML (index.html), który służy jako demonstracja
działania API.

Umożliwia on:
- dodawanie leadów
- wyświetlanie listy leadów
- filtrowanie leadów po statusie

Interfejs komunikuje się bezpośrednio z backendem za pomocą zapytań HTTP (fetch API)
i pełni rolę klienta testowego dla endpointów REST.

---

## Logika biznesowa

Projekt zawiera przykładowe reguły biznesowe, m.in.:

* brak możliwości przejścia leada bezpośrednio do statusu `client`
* zapisywanie każdej zmiany statusu w tabeli historii

---

## Autoryzacja

Projekt wykorzystuje prostą obsługę ról użytkowników (np. `admin`) przekazywaną w nagłówku zapytania.

Konfiguracja JWT (klucz, algorytm) została dodana jako podstawa do dalszego rozwoju projektu. Pełna autoryzacja oparta o JWT (logowanie, tokeny dostępu) jest planowana w kolejnych etapach.

---

## Dokumentacja API

FastAPI automatycznie generuje dokumentację API:

* Swagger UI: `/docs`
* ReDoc: `/redoc`

Dokumentacja umożliwia testowanie wszystkich endpointów bezpośrednio z poziomu przeglądarki.

---

## Uruchomienie projektu lokalnie

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Aplikacja dostępna pod adresem:

```
http://127.0.0.1:8000
```

---

## Struktura projektu

```
crm_api/
├── main.py
├── database.py
├── models.py
├── crm.db
├── static/
├── index.html
├── history.html
├── .gitignore
└── README.md
```

---

## Możliwe rozszerzenia (plan rozwoju)

* Pełna autoryzacja JWT (login, access token)
* Frontend (React / Vue)
* Testy jednostkowe
* Podział uprawnień użytkowników
* Deployment (Docker / cloud)

---

## Status projektu

Projekt rozwijany – kolejne funkcjonalności będą dodawane etapami.

---

## Autor

Projekt stworzony jako część portfolio programistycznego.
