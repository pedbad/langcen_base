# langcen_base

![Python](https://img.shields.io/badge/python-3.13-blue)
![Django](https://img.shields.io/badge/django-5.2-green)
![Tailwind](https://img.shields.io/badge/tailwind-4.1-blueviolet)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Reusable **Django + Tailwind v4 + ShadCN‑Django** scaffold for Language Centre projects.

This repository provides a clean, modular starting point for building Django applications that need:

- Custom user model with roles (**student**, **teacher**, **admin**)
- Authentication (login, logout, register, password reset)
- Tailwind CSS v4 integration (via npm)
- ShadCN‑Django components (rendered by **django‑cotton**)
- Admin UI (Unfold) + Import/Export (**django-unfold** , **django-import-export**)
- Django Browser Reload for live development refresh
- Pre‑commit hooks (Black + Ruff)
- Seed script for creating users from CSV files
- Basic pytest suite for testing

---

## 🧭 Table of Contents

1. [Getting Started](#-getting-started)
2. [Project Structure](#-project-structure)
3. [Frontend (Tailwind + ShadCN‑Django)](#-frontend-tailwind--shadcn-django)
   - [Requirements](#requirements)
   - [Install & Init](#install--init)
   - [Tailwind input.css](#tailwind-inputcss)
   - [Using Components](#using-components)
   - [Installed Components](#installed-components)
   - [Troubleshooting](#troubleshooting)
4. [Development](#-development)
5. [Seeding Students](#-seeding-students)
6. [Testing](#-testing)
7. [License](#-license)
8. [Contributing](#-contributing)

---

<h2 id="getting-started">🚀 Getting Started</h2>

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

### Run server (two options)

```bash
# classic
python src/manage.py runserver

# or: run Django + Tailwind watcher together
npm run dev
```
> `npm run dev` uses `concurrently` to run Tailwind watcher and Django’s dev server.

---

<h2 id="project-structure">🧱 Project Structure</h2>

```
langcen_base/
├── data/                          # seed CSVs (ignored in git except samples)
│   └── sample_students.csv
├── requirements.txt               # base dependencies
├── requirements-dev.txt           # dev-only dependencies
├── templates/                     # shadcn-django component templates (django-cotton)
│   └── cotton/
│       └── … components live here
├── src/
│   ├── config/                    # Django project settings
│   ├── core/                      # base templates, partials, and public pages
│   │   └── static/core/css/       # Tailwind input.css → output.css
│   └── users/                     # custom user app
│       ├── management/commands/   # e.g., seed_students
│       ├── templates/             # auth templates
│       └── tests/                 # pytest suites
└── README.md
```

---

<h2 id="frontend-tailwind--shadcn-django">🎨 Frontend (Tailwind + ShadCN-Django)</h2>

ShadCN‑Django components are plain Django templates powered by **django‑cotton**. We vendor (commit) the component templates under `templates/cotton/`, so every clone has the exact same UI building blocks without extra per‑machine steps (aside from installing Python/Node deps).

### Requirements

| Tool | Purpose | Installed via |
|------|--------|----------------|
| TailwindCSS v4 | Core utility framework | `npm install` (from repo `package.json`) |
| django‑cotton | Component renderer | `pip install django-cotton` (in `requirements.txt`) |
| shadcn‑django (CLI) | Add/update components into `templates/cotton/` | optional: `pipx install shadcn-django` |

#### Settings required

Ensure these are present in **`src/config/settings.py`**:

```python
INSTALLED_APPS = [
    # … Django core apps …
    "core",
    "users",
    "django_cotton",  # ← required for shadcn-django components
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "core" / "templates",   # app/site templates
            BASE_DIR / "templates",            # ← shadcn-django components (templates/cotton/**)
        ],
        "APP_DIRS": True,
        "OPTIONS": { "context_processors": [
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]},
    },
]
```

> We commit the `templates/cotton/**` folder. Nothing else is needed at runtime besides installing Python/Node deps.

### Install & Init

If you want to **add more components** locally using the CLI:

```bash
# optional: install the CLI once
pipx install shadcn-django

# in the project root (where manage.py lives under src/)
shadcn_django init         # creates/updates shadcn.config.json if needed

# add components (one per command)
shadcn_django add button
shadcn_django add input
shadcn_django add card
# … etc.
```

> The CLI accepts **one component per command**. All generated files land in `templates/cotton/<component>/index.html`.

### Tailwind input.css

The Tailwind entry lives at **`src/core/static/core/css/input.css`** and is compiled to **`src/core/static/core/css/output.css`** by our npm scripts.

**Key lines (already in this repo):**

```css
/* Tell Tailwind where to scan for classes */
@source "./src/core/templates/**/*.html";
@source "./templates/cotton/**/*.html";   /* shadcn-django components */
@source "./src/**/*.py";

/* Core Tailwind */
@import "tailwindcss";

/* Optional animations plugin — only if you install it */
@import "tw-animate-css";

/* Dark-mode variant that components expect */
@custom-variant dark (&:is(.dark *));

/* Design tokens (Tailwind v4 @theme) */
@theme {
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.145 0 0);
  --color-card: oklch(1 0 0);
  --color-card-foreground: oklch(0.145 0 0);
  --color-popover: oklch(1 0 0);
  --color-popover-foreground: oklch(0.145 0 0);
  --color-primary: oklch(0.205 0 0);
  --color-primary-foreground: oklch(0.985 0 0);
  --color-secondary: oklch(0.97 0 0);
  --color-secondary-foreground: oklch(0.205 0 0);
  --color-muted: oklch(0.97 0 0);
  --color-muted-foreground: oklch(0.556 0 0);
  --color-accent: oklch(0.97 0 0);
  --color-accent-foreground: oklch(0.205 0 0);
  --color-destructive: oklch(0.577 0.245 27.325);
  --color-destructive-foreground: oklch(0.985 0 0);
  --color-border: oklch(0.922 0 0);
  --color-input: oklch(0.922 0 0);
  --color-ring: oklch(0.708 0 0);
  --radius: 0.625rem;
}

/* Base layer using tokens */
@layer base {
  * { @apply border-border outline-ring/50; }
  body { @apply bg-background text-foreground; }
}
```

**Build/watch:**

```bash
npm run tw:watch        # Tailwind watcher
# or
npm run dev             # Tailwind watcher + Django server
```

### Using Components

You can use components in **two equivalent ways**. Pick one style per block and don’t mix within the same component.

**Option A — Native tags (recommended, no `{% load %}` needed):**

```html
<div class="flex gap-2">
  <c-button variant="outline">Cancel</c-button>
  <c-button variant="destructive">Delete</c-button>
</div>

<c-card class="mt-4 max-w-md">
  <c-slot name="header">
    <h3 class="text-lg font-semibold leading-none">Sign in</h3>
    <p class="text-sm text-muted-foreground">Use your email and password.</p>
  </c-slot>
  <c-label for="email">Email</c-label>
  <c-input id="email" name="email" type="email" value="{{ user.email|default:'' }}" />
</c-card>
```

**Option B — Template tags (`{% c … %}{% endc %}`):**

```django
{% load _component _slot %}

<div class="flex gap-2">
  {% c button variant="outline" %}Cancel{% endc %}
  {% c button variant="destructive" %}Delete{% endc %}
</div>

{% c card class="mt-4 max-w-md" %}
  {% slot header %}
    <h3 class="text-lg font-semibold leading-none">Sign in</h3>
    <p class="text-sm text-muted-foreground">Use your email and password.</p>
  {% endslot %}
  {% c label for="email" %}Email{% endc %}
  {% c input id="email" name="email" type="email" value="{{ user.email|default:'' }}" %}
{% endc %}
```

> **Passing context is supported in both styles.** Use `{{ }}` for slotted content and plain attribute values for props (e.g., `value="{{ form.email.value }}"`).

### Installed Components

The repo currently includes (vendored under `templates/cotton/`):

```
a, accordion, alert, alert_dialog, badge, button, card, checkbox, combobox,
command, command_dialog, dialog, dropdown_menu, form, input, label,
navigation_menu, popover, progress, select, separator, sheet, table, tabs,
textarea, toast
```

You can add more anytime with `shadcn_django add <name>` and commit the new folder(s).

### Troubleshooting

- **`TemplateDoesNotExist: cotton/.../index.html`**
  Ensure `templates/` is listed in `TEMPLATES[0]["DIRS"]` and the component folder exists under `templates/cotton/`.

- **`Invalid block tag … expected 'endc'`**
  You’re mixing Option A and Option B. For `{% c … %}`, close with `{% endc %}` and use `{% slot … %}{% endslot %}`. For `<c-…>` style, just use HTML‑like tags.

- **Styles don’t look right**
  Confirm your `input.css` contains the `@source "./templates/cotton/**/*.html";` line and that `npm run tw:watch` is running. Regenerate the CSS if needed by saving a file or restarting the watcher.

- **Vendored JS libraries ignored by git**
  We keep third‑party JS (e.g., Alpine) under `src/core/static/core/js/lib/`. If you use a strict `.gitignore`, ensure it allows that path:
  ```gitignore
  !src/core/static/core/js/lib/
  !src/core/static/core/js/lib/**
  ```

---

<h2 id="development">🧑‍💻 Development</h2>

### Key dev dependencies

| Tool | Purpose |
|------|--------|
| django‑extensions | shell_plus, show_urls, etc. |
| django‑browser‑reload | auto‑reload for template/CSS changes |
| pre‑commit | auto lint + format on commit (Black + Ruff) |

**Run hooks manually:**

```bash
pre-commit run --all-files
```

---

<h2 id="seeding-students">📦 Seeding Students</h2>

Bulk‑create student users from a CSV file:

```bash
python src/manage.py seed_students
```

### CSV example

```csv
email,first_name,last_name,password
alice@example.com,Alice,Anderson,Secret123!
bob@example.com,Bob,Barnes,
charlie@example.com,Charlie,Chaplin,
```

### Dry‑run mode

```bash
python src/manage.py seed_students data/students_2025.csv \
  --default-password=ChangeMe123! --dry-run
```

### Create users for real

```bash
python src/manage.py seed_students data/students_2025.csv \
  --default-password=ChangeMe123!
```

### Update existing users

```bash
python src/manage.py seed_students data/students_2025.csv --update
```

### Send welcome emails

```bash
python src/manage.py seed_students data/students_2025.csv \
  --send-welcome --site-domain=127.0.0.1:8000
```

---

<h2 id="testing">🧪 Testing</h2>

We use **pytest** with **pytest‑django**.

```bash
pytest -q
```

Covers:
- User model creation
- Authentication flows
- Password reset
- Student seeding (dry‑run/create/update)

---

<h2 id="license">⚖️ License</h2>

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

<h2 id="contributing">🤝 Contributing</h2>

Pull requests are welcome! For major changes, please open an issue first.

Before submitting:

```bash
pre-commit run --all-files
pytest -q
```

---

## 🪄 Badges

![Python](https://img.shields.io/badge/python-3.13-blue)
![Django](https://img.shields.io/badge/django-5.2-green)
![Tailwind](https://img.shields.io/badge/tailwind-4.1-blueviolet)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

---
## 🔐 Auth & Email — Dev Quickstart

**Logout (Django 5):**
Logout is **POST-only**. Our view renders a logged-out page (no redirect).
```html
<form action="{% url 'users:logout' %}" method="post">{% csrf_token %}
  <button type="submit">Sign out</button>
</form>
```

**Password reset (dev):**
We use a file-based backend; emails are written to `tmp_emails/`.

```env
# .env (dev)
EMAIL_BACKEND=django.core.mail.backends.filebased.EmailBackend
EMAIL_FILE_PATH=/absolute/path/to/langcen_base/tmp_emails
DEFAULT_FROM_EMAIL=no-reply@langcen_base.com
SITE_DOMAIN=127.0.0.1:8000
SITE_USE_HTTPS=False
```

- Visit `/users/password-reset/`
- Open the newest file in `tmp_emails/`
- Click the `/users/reset/<uid>/<token>/` link to set a new password

**Invite-on-create (signals):**
Creating a non-staff, non-superuser `User` triggers an **invite email** (via password-reset flow) **after** DB commit:
- Handler: `users/signals.py` (uses `transaction.on_commit`)
- Sender: `users/utils.send_set_password()` (uses our email templates)
- Templates (namespaced):
  - `users/registration/password_reset_subject.txt`
  - `users/registration/password_reset_email.txt`
  - `users/registration/password_reset_email.html`

**Auth URLs (namespaced):**
- Login: `users:login` → `/users/login/`
- Logout (POST): `users:logout` → `/users/logout/`
- Password reset: `users:password_reset` → `/users/password-reset/`
- Confirm: `users:password_reset_confirm` → `/users/reset/<uid>/<token>/`
- Complete: `users:password_reset_complete` → `/users/reset/done/`

**Custom logic kept modular:**
- Views: `users/views.py` (email-only login, role redirects)
- Constants (template map): `users/constants.py` (`PWD_RESET_TPLS`)
- Utils: `users/utils.py` (`send_set_password`, `get_domain_and_scheme`)
- Signals: `users/signals.py` (invite on create; loaded in `users/apps.py`)
- Mixins: `users/mixins.py` (`AdminRequiredMixin`)


## 🧪 Running Tests

We use `pytest` + `pytest-django`.

```bash
# all tests
pytest -q

# focused
pytest -q src/users/tests/test_password_reset.py::test_password_reset_sends_email
pytest -q src/users/tests/test_register.py
```
**Suite status:** 17 tests passing.
Covers:
- Logout renders a page (POST-only)
- Password reset sends email (locmem/file backends)
- Register requires staff/admin; one invite email sent via signal
- Role-based redirects after login


## 🚀 Production Notes

Switch to SMTP in `.env` and enable HTTPS links in emails:

```env
ENV=prod
DEBUG=False
SITE_DOMAIN=langcen.cam.ac.uk
SITE_USE_HTTPS=True

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=***redacted***
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=no-reply@langcen.cam.ac.uk

ALLOWED_HOSTS=langcen.cam.ac.uk,www.langcen.cam.ac.uk
```

Optional security/timeouts:
```python
# settings.py
from datetime import timedelta
PASSWORD_RESET_TIMEOUT = int(timedelta(hours=24).total_seconds())
```


## 🧭 UI Refresh Checklist (snapshot)

> Source: `ui_refresh_checklist.md`. Quick snapshot for convenience.
>
> ---
# 🧭 LangCen UI Refresh — Quick Checklist

## ✅ DONE (Phase 1)

### 🔹 Navigation
- [x] Responsive navbar (desktop + mobile)
- [x] Active link highlighting via templatetag
- [x] Modular partials (`logo`, `theme_toggle`, `navbar`, `header`)
- [x] Proper order + alignment of theme toggle and icons

### 🔹 Branding
- [x] Logo swap (light/dark: `logo-cap.svg`, `logo-cap-blue.svg`)
- [x] Accessible dark/light toggling with Tailwind classes

### 🔹 Theming
- [x] Alpine store + `window.deferLoadingAlpine()` fix
- [x] Theme persistence via `localStorage`
- [x] Tailwind v4 tokens (`bg-background`, `text-foreground`, etc.)

### 🔹 Footer
- [x] University-style layout with Cambridge logo
- [x] Fully theme-aware (light/dark)
- [x] Responsive stacked/side-by-side design
- [x] Stable logo sizing using Tailwind height utilities

### 🔹 Cookie Banner
- [x] CIVIC integrated (`core/partials/scripts.html`)
- [x] CSRF-safe with `csrftoken` + `sessionid`
- [x] Stub ready for Analytics

### 🔹 Messages UI
- [x] Themed dismissible alerts
- [x] Accessible focus/hover states
- [x] Clean handling of empty or error states

### 🔹 Forms + Auth
- [x] Reusable field + error partials
- [x] Custom `add_attrs` filter (`form_extras.py`)
- [x] Login + Password Reset flow fully styled via Cotton
- [x] Registration link removed (admin-only policy)

### 🔹 Template System
- [x] Using `django-cotton` loader stack (Option B)
- [x] Loaders ordered: Cotton → filesystem → app_directories
- [x] Template dirs configured for `core/templates` + shared `/templates`

---

## 🚧 TODO (Phase 2)

### A. Auth polish
- [ ] Add `logged_out.html` (optional logout confirmation page)
- [ ] Verify SMTP for password reset emails
- [ ] Restrict `/register` route with `@staff_member_required`

### B. Footer finishing
- [ ] Replace placeholder links (T&C, Accessibility, Support)
- [ ] Finalize logo sizes (Cambridge + eLearning)

### C. Base layout & meta
- [ ] Add favicons + theme-color meta tags
- [ ] Add Open Graph / social meta
- [ ] Check header–main–footer spacing on mobile

### D. Mobile nav polish
- [ ] Add `x-transition` slide/fade animations
- [ ] (Optional) Persist menu open state in Alpine store

### E. Token QA
- [ ] Verify contrast + hover/focus states on About / Landing

### F. Error pages
- [ ] Create themed `core/404.html` + `core/500.html`

### G. Cookie banner analytics
- [ ] Implement `onAccept` / `onRevoke` hooks for GA or Matomo

---

## 🧪 Tests (Planned)
Add under `src/users/tests/`:

### `test_auth.py`
- [ ] Role-based redirect
- [ ] No "Create account" link on login
- [ ] Wrong password → error message
- [ ] Logout → redirects to login

### `test_password_reset.py`
- [ ] Form renders and sends email
- [ ] Complete flow with token (optional)

---

## 🧩 Tech Stack Summary
- Django + Tailwind v4 + Cotton (ShadCN-style templates)
- Alpine.js 3 store for theme & mobile nav
- CIVIC cookie banner integrated
- Theming via Tailwind design tokens
- Auth flows styled with `<c-card>` / `<c-button>`

> ---


## 🛠 Admin helper (optional)

Send an invite (set-password link) from shell:

```python
from users.utils import send_set_password
send_set_password("user@example.com", domain="langcen.cam.ac.uk", use_https=True)
```
