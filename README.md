# langcen_base

Reusable Django + Tailwind base for eLearning projects with three roles (student, teacher, admin).

## Status
Initial scaffolding. Next step: add `.gitignore` (macOS, Python/Django, npm) and project conventions.

## Why
Clone → rename → add new apps (e.g., exams, assessments) without redoing auth, layout, and tooling.

## Stack (planned)
- Django 5.2 LTS (Python 3.13)
- Tailwind via npm (CLI)
- pyenv for Python versions

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
pyenv install 3.13.2   # if not already installed
pyenv local 3.13.2
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

Install npm packages:

```bash
npm install
```
