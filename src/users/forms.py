# src/users/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    # We’ll expose role for now (default student). You can remove later.
    role = forms.ChoiceField(choices=User.Roles.choices, initial=User.Roles.STUDENT)

    class Meta(UserCreationForm.Meta):
        model = User
        # UserCreationForm expects a "username" field by default; our model uses email.
        # So we override fields to include "email" explicitly.
        fields = ("email",)
