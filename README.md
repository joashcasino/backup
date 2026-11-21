# MyFinder

A lost-and-found web system for MSU-IIT. Students, faculty, and staff sign in with a university email, post lost reports and found items, search listings, and submit claims. Found items are surrendered to SID, which logs them, verifies claimants, and records the release.

**Team:** Anti-Kamote Gang (CSC181)

**Maintainer:** _to be named by the team_

## Tech stack

- Python 3.11 or newer
- Django 5.2
- PostgreSQL 16, run in Docker

## Prerequisites

- Git
- Python 3.11 or newer
- Docker Desktop (with Docker Compose)

## Project structure

| App | Purpose | Stories |
|---|---|---|
| `accounts` | Custom user model, sign-in, SID role | US-16 |
| `items` | Item model, lost/found posts, photos, SID logging | US-01, US-02, US-03a, US-09 |
| `claims` | Claims, approval, release | US-07, US-08, US-11, US-17 |
| `listings` | Home page, search, status page | US-04, US-06 |

## Setup

1. Clone the repository and open the folder.

```bash
   git clone https://github.com/jjmmontemayor/csc181-g12.git
   cd csc181-g12
```

2. Create and activate a virtual environment.

```powershell
   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1
```

```bash
   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
```

3. Install the dependencies.

```bash
   python -m pip install -r requirements.txt
```

4. Create your local settings file, then open `.env` and replace every `change-me`.

```powershell
   # Windows (PowerShell)
   Copy-Item .env.example .env
```

```bash
   # macOS / Linux
   cp .env.example .env
```

   - `DJANGO_SECRET_KEY`: generate one with
     `python -c "import secrets; print(secrets.token_urlsafe(50))"`
   - `POSTGRES_PASSWORD`: choose a password (letters, digits, and underscores only).
     Set it before the first `docker compose up`. The database stores the password when it is first created.

   Never commit `.env`. It is listed in `.gitignore`.

5. Start the database.

```bash
   docker compose up -d
```

   The database listens on host port **5433** to avoid clashing with a local PostgreSQL on 5432.

6. Create the database tables and an admin account.

```bash
   python manage.py migrate
   python manage.py createsuperuser
```

   SID staff accounts are created by an admin in the admin site (http://127.0.0.1:8000/admin/). Open the user and set **Role** to "SID staff".

7. Run the app and open http://127.0.0.1:8000/.

```bash
   python manage.py runserver
```

## Everyday commands

| Task | Command |
|---|---|
| Stop the database | `docker compose stop` |
| Start it again | `docker compose start` |
| Open a SQL shell | `docker compose exec db psql -U <POSTGRES_USER> -d <POSTGRES_DB>` |
| Reset the database (**deletes all data**) | `docker compose down -v` |

> After pulling changes that include new migrations, run `python manage.py migrate`.
> After a change to the user model or a messy migration history, reset with
> `docker compose down -v`, `docker compose up -d`, then `python manage.py migrate`.

## Status

Sprint 1 in progress.