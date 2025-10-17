# users/views.py

# Django imports
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

# Local imports
from .constants import PWD_RESET_TPLS  # ← centralised template names
from .forms import RegisterForm
from .mixins import AdminRequiredMixin
from .utils import get_domain_and_scheme

User = get_user_model()


def _redirect_for_role(user: AbstractBaseUser) -> str:
    """Map user.role → URL name (configured in settings.USERS_ROLE_REDIRECTS)."""
    mapping = getattr(settings, "USERS_ROLE_REDIRECTS", {})
    url_name = mapping.get(getattr(user, "role", None), "users:student_home")
    return reverse(url_name)


# --------------------------
# Auth: login / logout
# --------------------------
class EmailLoginView(LoginView):
    template_name = "users/registration/login.html"

    def get_success_url(self):
        return _redirect_for_role(self.request.user)


class EmailLogoutView(LogoutView):
    # render a page instead of redirecting
    next_page = None
    template_name = "users/registration/logged_out.html"


# --------------------------
# Auth: register
# --------------------------
class RegisterView(AdminRequiredMixin, CreateView):
    template_name = "users/registration/register.html"
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy("users:student_home")  # fallback

    @transaction.atomic
    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = form.cleaned_data.get("role", User.Roles.STUDENT)

        # Ensure first-time set-password flow is required
        user.set_unusable_password()
        user.save()

        # ✅ derive domain + scheme from the current request (or fallback)
        domain, use_https = get_domain_and_scheme(self.request)

        # Note:
        # The password-set ("invite") email is NOT sent here directly.
        # A post_save signal in users/signals.py automatically sends the invite
        # whenever a new non-staff, non-superuser User is created.
        # This avoids duplicate emails and keeps all invite logic in one place.
        messages.success(
            self.request,
            f"User {user.email} created. An invite email will be sent automatically.",
        )

        return redirect(_redirect_for_role(user))


# --------------------------
# Password reset flow (centralised via PWD_RESET_TPLS)
# --------------------------
class PasswordResetStartView(PasswordResetView):
    template_name = PWD_RESET_TPLS["form"]
    email_template_name = PWD_RESET_TPLS["email_txt"]
    subject_template_name = PWD_RESET_TPLS["subject"]
    html_email_template_name = PWD_RESET_TPLS.get("email_html")
    success_url = reverse_lazy("users:password_reset_done")


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = PWD_RESET_TPLS["done"]


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = PWD_RESET_TPLS["confirm"]
    success_url = reverse_lazy("users:password_reset_complete")


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = PWD_RESET_TPLS["complete"]


# --------------------------
# Simple role home placeholders
# --------------------------
def student_home(request):
    return render(request, "users/student_home.html")


def teacher_home(request):
    return render(request, "users/teacher_home.html")


def admin_home(request):
    return render(request, "users/admin_home.html")
