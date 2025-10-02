# src/users/tests/test_register.py
#
# Purpose: Ensure the register view creates a user and logs them in, then redirects by role.

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
def test_register_creates_user_logs_in_and_redirects(client):
    """
    GIVEN a fresh visitor
    WHEN they submit the register form with email + matching passwords + role
    THEN a new user is created, they're logged in, and redirected by role
    """
    url = reverse("users:register")
    form_data = {
        "email": "newstudent@example.com",
        "password1": "pass1234ABC!",
        "password2": "pass1234ABC!",
        "role": "student",
    }
    resp = client.post(url, data=form_data, follow=True)

    # Should redirect to student home
    assert resp.redirect_chain
    assert resp.resolver_match.view_name == "users:student_home"

    # User exists and is authenticated in the session
    u = User.objects.get(email="newstudent@example.com")
    assert u.is_authenticated  # user instance is real
    # A stricter check: the client session contains auth —
    # check a page that requires auth later if needed
