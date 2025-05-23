# Face Value

Web interface for rating twisty puzzles.

Face Value is a Django-based platform for twisty puzzle enthusiasts to catalog, rate, and review puzzles (e.g., Rubik’s Cube, Megaminx, Pyraminx).

This project aims to:
- Provide an intuitive UI for browsing and managing puzzle collections.
- Enable registered users to submit ratings and written reviews.
- Support searching reviews by attributes (brand, type, rating, user).

### Technology stack
- Python 3.x
- Django
- SQLite (Development; configurable for PostgreSQL in production)

## Setup (local development)

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Apply database migrations and start the development server
python manage.py migrate
python manage.py runserver

# TODO: add more about setup when that is more defined
```

- Visit http://127.0.0.1:8000/ to browse puzzles and reviews.
- Visit http://127.0.0.1:8000/admin/ to manage puzzles and users.

## AGENTS.md
There is an AGENTS.md file which contains additional instructions and information that agents should consider and maintain