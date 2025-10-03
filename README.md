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


# 📦 Seeding Students

You can bulk-create student users from a CSV file using the custom Django management command:

```bash
python src/manage.py seed_students
```

## 1. Prepare Your CSV

Place your CSV file inside the `data/` folder (kept out of version control). Example:

`data/students_2025.csv`
```csv
email,first_name,last_name,password
alice@example.com,Alice,Anderson,Secret123!
bob@example.com,Bob,Barnes,
charlie@example.com,Charlie,Chaplin,
```

Notes:
- `email` is **required**.
- `first_name` and `last_name` are optional but recommended.
- `password` column is optional:
  - If provided, that value is used for the student’s initial password.
  - If blank, the `--default-password` value is applied.
  - If missing entirely (no `password` column in the CSV), a warning will be logged and password updates will be skipped.

---

## 2. Preview Before Writing (Dry-Run)

Safe mode — shows what *would* happen but makes no changes:

```bash
python src/manage.py seed_students data/students_2025.csv   --default-password=ChangeMe123!   --dry-run
```

Example output:
```
== seed_students starting ==
File: data/students_2025.csv
Headers: ['email', 'first_name', 'last_name', 'password']
Options: default_password=***, update=False, dry_run=True
[row 1] would create: alice@example.com (student)
[row 2] would create: bob@example.com (student)
[row 3] would create: charlie@example.com (student)
rows=3 created=3 updated=0 skipped=0 invalid_email=0 dry_run=True
Done.
```

---

## 3. Create Users for Real

```bash
python src/manage.py seed_students data/students_2025.csv   --default-password=ChangeMe123!
```

This creates students with the given names and passwords. If no `password` in CSV, each gets `ChangeMe123!`.

---

## 4. Updating Existing Students

You can rerun with `--update` to modify existing users:

```bash
# Update names only
python src/manage.py seed_students data/students_2025.csv --update

# Update with new per-row passwords
python src/manage.py seed_students data/students_update.csv --update --send-welcome --site-domain=127.0.0.1:8000
```

Update rules:
- Names are updated if different.
- Passwords are updated **only** if the CSV includes a `password` column and value.
- `--default-password` is ignored during updates to prevent accidental mass resets.

---

## 5. Sending Welcome Emails

Use `--send-welcome` to send (or preview) welcome emails containing the login info and a password reset link:

```bash
python src/manage.py seed_students data/students_2025.csv   --default-password=ChangeMe123!   --send-welcome --site-domain=127.0.0.1:8000
```

Options:
- `--site-domain` → required with `--send-welcome`. e.g. `127.0.0.1:8000` or `portal.example.edu`
- `--use-https` → force https links (default: http)
- `--from-email` → override sender address (default: `settings.DEFAULT_FROM_EMAIL`)

Preview with dry-run:
```bash
python src/manage.py seed_students data/students_2025.csv   --default-password=ChangeMe123!   --send-welcome --site-domain=127.0.0.1:8000 --dry-run
```

Output:
```
[row 1] would create: alice@example.com (student)
    would email: alice@example.com
```

---

## 6. Summary of Options

- `--default-password=PWD` → used for new accounts without a CSV password
- `--update` → update names and (if provided) passwords for existing users
- `--dry-run` → preview changes without touching the DB
- `--send-welcome` → send (or preview) welcome emails
- `--site-domain=HOST:PORT` → required with `--send-welcome`
- `--use-https` → generate https links (default is http)
- `--from-email=addr` → custom sender address

---

👉 With this guide in the README, someone new can:
1. Drop a CSV into `data/`
2. Run a dry-run preview
3. Seed for real
4. Optionally update or send welcome emails


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
