# langcen_base

Reusable Django + Tailwind base for eLearning projects with three roles (student, teacher, admin).

## Status
Base project scaffolded with Django 5.2, Tailwind v4, and development tooling.

## Why
Clone → rename → add new apps (e.g., exams, assessments) without redoing auth, layout, and tooling.

## Stack (planned)
- Django 5.2 LTS (Python 3.13)
- Tailwind v4 via npm (CLI)
- pyenv for Python versions
- Pre-commit hooks (Black, Ruff)

## Getting Started (Development)

### Prerequisites
- [pyenv](https://github.com/pyenv/pyenv) installed
- Python 3.13.2 (pinned in `.python-version`)
- Git + npm

### Setup
Clone and enter the project folder:

```bash
git clone git@github.com:pedbad/langcen_base.git
cd langcen_base
```

Install the pinned Python version and set it locally:

```bash
pyenv install 3.13.3   # if not already installed
pyenv local 3.13.3
```

Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate
```

Upgrade pip:

```bash
pip install --upgrade pip
```

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

Install npm packages:

```bash
npm install
```

## Development Tooling

This project uses [pre-commit](https://pre-commit.com/), [Black](https://black.readthedocs.io/), and [Ruff](https://docs.astral.sh/ruff/) to keep the codebase consistent and clean.

### One-time setup
After creating and activating your `venv`:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

### Running checks
On every git commit, pre-commit will:

- Strip trailing whitespace
- Fix EOF newlines
- Run Black (Python formatter)
- Run Ruff (linter & import sorter)

To run checks manually on all files:
```bash
pre-commit run --all-files
```

## Tailwind Setup

### CSS entrypoint
Tailwind v4 is configured via `@source` in `src/core/static/core/css/input.css`:

```css
@source "./src/core/templates/**/*.html";
@source "./src/**/*.py";

@import "tailwindcss";
```

### Build scripts
`package.json` contains:

```json
{
  "scripts": {
    "tw:build": "tailwindcss -i src/core/static/core/css/input.css -o src/core/static/core/css/output.css -m",
    "tw:watch": "tailwindcss -i src/core/static/core/css/input.css -o src/core/static/core/css/output.css -w",
    "dev": "concurrently -k \"npm:tw:watch\" \"venv/bin/python src/manage.py runserver\""
  }
}
```

### Usage
- One-off build:
  ```bash
  npm run tw:build
  ```

- Watch (rebuild on change):
  ```bash
  npm run tw:watch
  ```

- Run Django + Tailwind watcher together:
  ```bash
  npm run dev
  ```
  This starts Django on port **8000** and Tailwind watch in parallel.

## Live Reload

This project uses [django-browser-reload](https://github.com/adamchainz/django-browser-reload) in **development only**.

- Installed in `requirements-dev.txt`
- Enabled only when `DEBUG=True`
- Injects a reload script via `scripts.html`

When you save templates or Tailwind recompiles, the browser refreshes automatically.

---

### Development workflows

**Option A (classic Django):**
```bash
source venv/bin/activate
python src/manage.py runserver
npm run tw:watch   # run separately in another terminal
```

**Option B (all-in-one):**
```bash
npm run dev
```
Runs Django + Tailwind watcher with live reload.

---

## Next Steps
- Add base templates/partials (head, header, footer, scripts)
- Create `users` app for authentication & role-based redirects
- Expand core pages (landing, about)
