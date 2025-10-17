# users/utils.py
from django.conf import settings

from .constants import PWD_RESET_TPLS
from .forms_invite import InvitePasswordResetForm


def send_set_password(email, *, domain="localhost:8000", use_https=False, from_email=None):
    form = InvitePasswordResetForm({"email": email})
    if form.is_valid():
        form.save(
            from_email=from_email or getattr(settings, "DEFAULT_FROM_EMAIL", None),
            use_https=use_https,
            domain_override=domain,
            email_template_name=PWD_RESET_TPLS["email_txt"],
            subject_template_name=PWD_RESET_TPLS["subject"],
            html_email_template_name=PWD_RESET_TPLS.get("email_html"),
        )
        # Return True only if at least one user matched
        return True
    return False


def get_domain_and_scheme(request=None):
    """
    Returns (domain, use_https).
    - If request is provided: prefer request host + request.is_secure().
    - Else: fall back to settings.SITE_DOMAIN and assume https=False.
    """
    if request is not None:
        domain = getattr(settings, "SITE_DOMAIN", None) or request.get_host()
        use_https = request.is_secure()
        return domain, use_https

    # No request context (e.g., management command)
    domain = getattr(settings, "SITE_DOMAIN", "") or "localhost"
    return domain, False
