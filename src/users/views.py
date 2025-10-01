# src/users/views.py
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
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
    mapping = getattr(settings, "USERS_ROLE_REDIRECTS", {})
    url_name = mapping.get(user.role, "users:student_home")
    return reverse(url_name)


class EmailLoginView(LoginView):
    """
    Uses Django's LoginView but redirects based on role after login.
    Templates under registration/login.html by convention.
    """

    template_name = "registration/login.html"

    def get_success_url(self):
        return _redirect_for_role(self.request.user)


class EmailLogoutView(LogoutView):
    next_page = reverse_lazy("users:login")


class RegisterView(View):
    """
    Minimal register view to create a user (default student), then log them in.
    In production you might restrict this to admins only.
    """

    template_name = "registration/register.html"

    def get(self, request):
        return render(request, self.template_name, {"form": RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Ensure role from form (defaults to student)
            user.role = form.cleaned_data.get("role", User.Roles.STUDENT)
            user.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect(_redirect_for_role(user))
        return render(request, self.template_name, {"form": form})


# --- Placeholder dashboards so redirects resolve now ------------------------
def student_home(request):
    return render(request, "users/student_home.html")


def teacher_home(request):
    return render(request, "users/teacher_home.html")


def admin_home(request):
    return render(request, "users/admin_home.html")


# src/users/views.py (add below your admin_home)
def logout_then_login(request):
    """
    Log out regardless of current auth state, then go to the login page.
    Works even if the user is anonymous or hits this via GET.
    """
    logout(request)
    return redirect("users:login")


# --- Password reset wrappers (custom templates) -----------------------------
class PasswordResetStartView(PasswordResetView):
    email_template_name = "registration/password_reset_email.txt"
    subject_template_name = "registration/password_reset_subject.txt"
    template_name = "registration/password_reset_form.html"
    success_url = reverse_lazy("users:password_reset_done")


class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"
