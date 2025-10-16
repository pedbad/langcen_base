# users/views.py

# Standard library imports
# (none in this case)

# Django imports
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

# Local imports
from .forms import RegisterForm
from .mixins import AdminRequiredMixin

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
    next_page = None  # render a template instead of redirecting
    template_name = "users/registration/logged_out.html"


# --------------------------
# Auth: register
# --------------------------
class RegisterView(AdminRequiredMixin, CreateView):
    template_name = "users/registration/register.html"
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy("users:student_home")  # fallback; we’ll override redirect below

    def form_valid(self, form):
        user = form.save(commit=False)
        # Default to student unless admin selected a different role in the form
        user.role = form.cleaned_data.get("role", User.Roles.STUDENT)
        user.save()
        login(self.request, user)
        messages.success(self.request, "Welcome! Your account has been created.")
        return redirect(_redirect_for_role(user))


# --------------------------
# Password reset flow
# --------------------------
class PasswordResetStartView(PasswordResetView):
    template_name = "users/registration/password_reset_form.html"
    email_template_name = "users/registration/password_reset_email.txt"
    subject_template_name = "users/registration/password_reset_subject.txt"
    success_url = reverse_lazy("users:password_reset_done")


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/registration/password_reset_done.html"


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/registration/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/registration/password_reset_complete.html"


# --------------------------
# Simple role home placeholders
# --------------------------
def student_home(request):
    return render(request, "users/student_home.html")


def teacher_home(request):
    return render(request, "users/teacher_home.html")


def admin_home(request):
    return render(request, "users/admin_home.html")
