# Face Value

Web interface for rating twisty puzzles.

Face Value is a Django-based platform for twisty puzzle enthusiasts to catalog, rate, and review puzzles (e.g., Rubik’s Cube, Megaminx, Pyraminx).

This project aims to:
- Provide an intuitive UI for browsing and managing puzzle collections.
- Enable registered users to submit ratings and written reviews.
- Support searching reviews by attributes (brand, type, rating, user).

## Current Features
- Homepage with base template and navigation bar.
- User authentication (signup, login, logout) via the accounts app.
- User listing page displaying all registered users.
- Unit tests covering signup, login, and homepage views.
- Basic UI templates and static assets pipeline configured.

## Setup (local development)

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Apply database migrations and start the development server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# TODO: add more about setup when that is more defined
```

- Visit http://127.0.0.1:8000/ to browse puzzles and reviews.
- Visit http://127.0.0.1:8000/admin/ to manage puzzles and users.
- Visit http://127.0.0.1:8000/accounts/signup/ to create a new user account.
- Visit http://127.0.0.1:8000/accounts/login/ to log in.
- Use the logout link in the site navigation to log out.

## New Features
- Slug fields for puzzles for SEO-friendly URLs.
- Puzzle tagging support with a `Tag` model.
- Automatic aggregate fields (`avg_rating`, `review_count`) on puzzles.
- Rating restricted to 1–5 with choices and validators.
- Nested (threaded) comments with parent-child relations.
- `updated_at` timestamps on reviews and comments.
- One review per user constraint enforced at the database level.

## AGENTS.md
There is an AGENTS.md file which contains additional instructions and information that agents should consider and maintain