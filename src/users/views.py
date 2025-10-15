# src/users/views.py
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
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
from django.views import View

from .forms import RegisterForm

User = get_user_model()


def _redirect_for_role(user: User):
    """Map user.role → URL name (configured in settings.USERS_ROLE_REDIRECTS)."""
    mapping = getattr(settings, "USERS_ROLE_REDIRECTS", {})
    url_name = mapping.get(user.role, "users:student_home")
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
# Auth: register (optional)
# --------------------------
class RegisterView(View):
    """
    Simple registration. Hide the public link in templates if you don't want
    self-registration (admins can still create users in the admin).
    """

    template_name = "users/registration/register.html"

    def get(self, request):
        return render(request, self.template_name, {"form": RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data.get("role", User.Roles.STUDENT)
            user.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect(_redirect_for_role(user))
        return render(request, self.template_name, {"form": form})


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
