
# langcen_base

Reusable Django + Tailwind + ShadCN-Django scaffold for Language Centre projects.

This repository provides a clean, modular starting point for building Django applications that need:
- Custom user model with roles (student, teacher, admin)
- Authentication (login, logout, register, password reset)
- Tailwind CSS v4 integration (via npm)
- ShadCN-Django components (via django-cotton)
- Django Browser Reload for live development refresh
- Pre-commit hooks (Black + Ruff)
- Seed script for creating users from CSV files
- Basic pytest suite for testing

---

## 🧭 Table of Contents
1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Frontend (Tailwind + ShadCN-Django)](#frontend-tailwind--shadcn-django)
4. [Development](#development)
5. [Seeding Students](#seeding-students)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [License](#license)

---

## 🚀 Getting Started

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
pip install -r requirements-dev.txt
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

## 🧱 Project Structure

```
langcen_base/
├── data/                          # seed CSVs (ignored in git except samples)
│   └── sample_students.csv
├── requirements.txt               # base dependencies
├── requirements-dev.txt           # dev-only dependencies
├── src/
│   ├── config/                    # Django project settings
│   ├── core/                      # base templates, partials, and public pages
│   ├── users/                     # custom user app
│   │   ├── management/commands/   # custom commands (e.g., seed_students)
│   │   ├── templates/             # auth templates
│   │   └── tests/                 # pytest suites
└── README.md
```

---

## 🎨 Frontend (Tailwind + ShadCN-Django)

This scaffold integrates **Tailwind CSS v4** with **ShadCN-Django** components via `django-cotton`.

| Tool | Purpose | Installed via |
|------|----------|----------------|
| TailwindCSS v4 | Core utility framework | `npm install tailwindcss postcss autoprefixer` |
| django-cotton | Renders ShadCN component templates | `pip install django-cotton` |
| shadcn-django | CLI for managing ShadCN components | `pipx install shadcn-django` |

### Initial setup
```bash
# install Tailwind deps
npm install
npx tailwindcss init -p

# install shadcn-django CLI
pipx install shadcn-django

# initialize config and add components
shadcn_django init
shadcn_django add button input card
```

### Folder locations
```
templates/
└── cotton/
    └── button/
        └── index.html
src/core/static/core/css/input.css
src/core/static/core/css/output.css
```

### Example component usage
```html
{% load component from django_cotton %}
<div class="flex gap-2">
  {% c button variant="outline" %}Cancel{% endc %}
  {% c button variant="destructive" %}Delete{% endc %}
</div>
```

### Development commands
```bash
npm run tw:watch        # watch Tailwind for changes
npm run dev             # run Django + Tailwind concurrently
```

---

## 🧑‍💻 Development

### Key dev dependencies
| Tool | Purpose |
|------|----------|
| django-extensions | shell_plus, show_urls, etc. |
| django-browser-reload | auto-reload for template/CSS changes |
| pre-commit | auto lint + format on commit (Black + Ruff) |

### Run pre-commit manually
```bash
pre-commit run --all-files
```

---

## 📦 Seeding Students

You can bulk-create student users from a CSV file:

```bash
python src/manage.py seed_students
```

### CSV example
```
email,first_name,last_name,password
alice@example.com,Alice,Anderson,Secret123!
bob@example.com,Bob,Barnes,
charlie@example.com,Charlie,Chaplin,
```

### Dry-run mode
```bash
python src/manage.py seed_students data/students_2025.csv --default-password=ChangeMe123! --dry-run
```

### Create users for real
```bash
python src/manage.py seed_students data/students_2025.csv --default-password=ChangeMe123!
```

### Update existing users
```bash
python src/manage.py seed_students data/students_2025.csv --update
```

### Send welcome emails
```bash
python src/manage.py seed_students data/students_2025.csv --send-welcome --site-domain=127.0.0.1:8000
```

---

## 🧪 Testing

We use **pytest** with **pytest-django**.

```bash
pytest -q
```

Test coverage includes:
- User model creation
- Authentication flows
- Password reset
- Student seeding commands

---

## 🤝 Contributing

Pull requests are welcome!
For major changes, open an issue first.

Before submitting:
```bash
pre-commit run --all-files
pytest -q
```

---

## ⚖️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🪄 Badges (optional)

[Python](https://img.shields.io/badge/python-3.13-blue)
[Django](https://img.shields.io/badge/django-5.2-green)
[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
