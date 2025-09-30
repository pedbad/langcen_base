# langcen_base

Reusable Django + Tailwind base for eLearning projects with three roles (student, teacher, admin).

## Status
Initial scaffolding. Next step: add `.gitignore` (macOS, Python/Django, npm) and project conventions.

## Why
Clone → rename → add new apps (e.g., exams, assessments) without redoing auth, layout, and tooling.

## Stack (planned)
- Django 5.2 LTS (Python 3.13)
- Tailwind via npm (CLI + Tailwind UI/Plus components)
- pyenv for Python version management

## Getting Started (Development)

### Prerequisites
- [pyenv](https://github.com/pyenv/pyenv) installed
- Python 3.13.2 (pinned in `.python-version`)
- Git
- npm (for Tailwind)

### Setup
Clone and enter the project folder:

```bash
# SSH clone
git clone git@github.com:pedbad/langcen_base.git
# or HTTPS clone
git clone https://github.com/pedbad/langcen_base.git

cd langcen_base
```

Install the pinned Python version and set it locally:

```bash
pyenv install 3.13.2   # if not already installed
pyenv local 3.13.2
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Upgrade pip:

```bash
pip install --upgrade pip
```

## Tailwind Setup

We’ll use the official Tailwind CLI via npm.

```bash
# initialize npm in the project
npm init -y

# install Tailwind + PostCSS + Autoprefixer
npm install -D tailwindcss postcss autoprefixer

# generate default Tailwind + PostCSS configs
npx tailwindcss init -p
```

This creates `tailwind.config.js` and `postcss.config.js`.

We’ll later configure Tailwind to scan Django templates and output a compiled CSS file under `core/static/css`.

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
