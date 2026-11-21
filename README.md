# MyFinder

A lost-and-found web system for MSU-IIT. Students, faculty, and staff sign in with a university email, post lost reports and found items, search listings, and submit claims. Found items are surrendered to SID, which logs them, verifies claimants, and records the release.

**Team:** Anti-Kamote Gang (CSC181)

**Maintainer:** _to be named by the team_

## Tech stack

- Python 3.11 or newer
- Django 5.2 (Django ORM and migrations; no SQLAlchemy)
- PostgreSQL 16, run in Docker
- django-allauth for Google sign-in (MSU-IIT accounts only)
- Bootstrap 5 (CDN) with Django templates

## Prerequisites

- Git
- Python 3.11 or newer
- Docker Desktop (with Docker Compose)

## Project structure

| App | Purpose | Stories |
|---|---|---|
| `accounts` | Custom user model, Google sign-in, SID role, role-based landing page | US-16 |
| `items` | `Item` (found items) and `LostReport`, photos, SID logging | US-01, US-02, US-03a, US-09 |
| `claims` | `Claim`, approval, release, private proof photos | US-07, US-08, US-11, US-17 |
| `listings` | Home page, search, status page | US-04, US-06 |

## Setup

1. Clone the repository and open the folder.

```bash
   git clone <your-repo-url> myfinder
   cd myfinder
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
   - `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`: see **Google sign-in setup** below.

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

   The superuser signs in to the admin site (http://127.0.0.1:8000/admin/) with a password.
   Everyone else signs in with Google.

   **SID staff:** in the admin site, add a user with the staff member's @g.msuiit.edu.ph email
   and set **Role** to "SID staff". When they sign in with Google, they are matched by email and
   land on the SID dashboard. Everyone else lands on Browse.

7. Run the app and open http://127.0.0.1:8000/.

```bash
   python manage.py runserver
```

## Google sign-in setup

Only `@g.msuiit.edu.ph` Google accounts can sign in (`ALLOWED_EMAIL_DOMAIN` in `.env`).
Other accounts are sent back to the sign-in page with an error.

1. Open the [Google Cloud console](https://console.cloud.google.com/), create a project, and
   configure the **OAuth consent screen**.
2. Go to **Credentials → Create credentials → OAuth client ID → Web application**.
3. Under **Authorized redirect URIs**, add:
   `http://127.0.0.1:8000/accounts/google/login/callback/`
   (and `http://localhost:8000/accounts/google/login/callback/` if you use localhost).
4. Copy the client ID and secret into `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `.env`.

Each teammate can use the same client ID for local development.
Never commit the secret.

## Uploads

- `media/`: public files, such as the blurred found-item photos on listings.
- `private_media/`: claim proof photos. These are never served from `/media/`. Only the
  claimant and SID staff can open them, through `/claims/<id>/proof-photo/`.

Both folders are in `.gitignore`.

## Tests

Run the tests (Django creates a temporary test database in the Postgres container):

```bash
python manage.py test
```

## Everyday commands

| Task | Command |
|---|---|
| Stop the database | `docker compose stop` |
| Start it again | `docker compose start` |
| Open a SQL shell | `docker compose exec db psql -U <POSTGRES_USER> -d <POSTGRES_DB>` |
| Reset the database (**deletes all data**) | `docker compose down -v` |

> After pulling changes that include new migrations, run `python manage.py migrate`.
> If `accounts.0002` fails with a duplicate email error, two local users share an email
> (often an empty one). Give each user a unique email in the admin site, or reset the database.
> After a change to the user model or a messy migration history, reset with
> `docker compose down -v`, `docker compose up -d`, then `python manage.py migrate`.

## Status

Sprint 1 in progress.