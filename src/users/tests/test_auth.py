# src/users/tests/test_auth.py

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

# Grab the custom User model we defined in users/models.py
User = get_user_model()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "role,expected_name",
    [
        # Each tuple = (role we assign to the user, expected redirect view name)
        ("student", "users:student_home"),
        ("teacher", "users:teacher_home"),
        ("admin", "users:admin_home"),
    ],
)
def test_login_redirects_by_role(client, role, expected_name):
    """
    GIVEN a user exists with a certain role (student/teacher/admin),
    WHEN they log in via the login form,
    THEN they should be redirected to the correct role-specific home page.
    """

    # 1) Create a user with the given role and a known password
    user = User.objects.create_user(
        email=f"{role}@ex.com",
        password="pass1234",
        role=role,
    )

    # 2) Build the login URL dynamically (users:login)
    login_url = reverse("users:login")

    # 3) Simulate posting login credentials using Django's test client.
    # Note: The login form expects "username" even though our model uses email,
    # because Django maps USERNAME_FIELD ("email") internally to that key.
    resp = client.post(
        login_url,
        {"username": user.email, "password": "pass1234"},
        follow=True,  # follow redirects so we end up at the landing page
    )

    # 4) Assert we were redirected at least once
    assert resp.redirect_chain

    # 5) Assert the final resolved view name matches the expected role mapping
    assert resp.resolver_match.view_name == expected_name
