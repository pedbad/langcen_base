# langcen_base

Reusable Django + Tailwind scaffold for language centre projects.

This repo provides a clean starting point for building apps that need:
- Custom user model with roles (student, teacher, admin)
- Authentication (login, logout, register, password reset)
- Tailwind CSS v4 integration (via npm)
- Django Browser Reload for live dev refresh
- Pre-commit hooks with Black + Ruff
- Seed script for creating users from CSV files
- Basic pytest test suite

---

## Table of Contents
1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Development](#development)
4. [Seeding Students](#seeding-students)
5. [Testing](#testing)
6. [Contributing](#contributing)
7. [License](#license)

---

## Getting Started

### Clone and set up
```bash
git clone https://github.com/pedbad/langcen_base.git
cd langcen_base
```

### Python environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # for local dev helpers
```

### Frontend (Tailwind)
```bash
npm install
npm run tw:watch   # watch Tailwind for changes
```

### Database
```bash
python src/manage.py migrate
```

### Run server
```bash
python src/manage.py runserver
```

---

## Project Structure

```
langcen_base/
├── data/                          # seed CSVs (ignored in git except samples)
│   └── sample_students.csv
├── requirements.txt               # base dependencies
├── requirements-dev.txt           # dev-only dependencies
├── src/
│   ├── config/                    # Django project settings
│   ├── core/                      # base templates, public pages
│   ├── users/                     # custom user app
│   │   ├── management/commands/   # custom commands (e.g., seed_students)
│   │   ├── templates/             # auth templates
│   │   └── tests/                 # pytest suites
└── README.md
```

---

## Development

### Key dev dependencies
- `django-extensions` → shell_plus, show_urls, etc.
- `django-browser-reload` → live reload during Tailwind dev.
- `pre-commit` → lint + format hooks (Black + Ruff).

### Running pre-commit hooks manually
```bash
pre-commit run --all-files
```

---

## Seeding Students

You can bulk-create student users from a CSV file using the custom `seed_students` command.

**CSV format**:
```csv
email,first_name,last_name
alice@example.com,Alice,Anderson
bob@example.com,Bob,Barnes
charlie@example.com,Charlie,Chaplin
```

**Dry-run (preview only)**:
```bash
python src/manage.py seed_students data/sample_students.csv --default-password=ChangeMe123! --dry-run
```

**Seed for real**:
```bash
python src/manage.py seed_students data/sample_students.csv --default-password=ChangeMe123!
```

**Update existing users**:
```bash
python src/manage.py seed_students data/sample_students.csv --default-password=ChangeMe123! --update
```

Options:
- `--default-password` → applied if no per-row password is provided.
- `--dry-run` → safe preview mode (no writes).
- `--update` → update names/passwords of existing users.

---

## Testing

We use `pytest` with `pytest-django`.

Run the suite:
```bash
pytest -q
```

All core areas are tested:
- User model creation
- Authentication flows (login/logout/redirects)
- Password reset
- Seeding students (dry-run/create/update)

---

## Contributing

Pull requests are welcome.
For major changes, please open an issue first to discuss what you’d like to change.

Make sure to run:
```bash
pre-commit run --all-files
pytest -q
```
before submitting.

---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## Badges (optional)

You can add GitHub badges here for quick status:
- Python version
- Django version
- Build/CI status
- License

Example (to replace once CI/CD is set up):
```markdown
![Python](https://img.shields.io/badge/python-3.13-blue)
![Django](https://img.shields.io/badge/django-5.2-green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
```
