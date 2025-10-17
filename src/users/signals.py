# users/signals.py
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import send_set_password

User = get_user_model()


@receiver(post_save, sender=User)
def send_invite_on_create(sender, instance, created, **kwargs):
    if not created:
        return

    # Policy: skip superusers; (optionally) skip staff if you only invite learners
    if getattr(instance, "is_superuser", False):
        return
    # If you DO want to invite staff, comment the next two lines:
    if getattr(instance, "is_staff", False):
        return

    domain = getattr(settings, "SITE_DOMAIN", "localhost:8000")
    use_https = getattr(settings, "SITE_USE_HTTPS", False)
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")

    def _send():
        # send once the transaction is safely committed
        send_set_password(
            instance.email,
            domain=domain,
            use_https=use_https,
            from_email=from_email,
        )

    transaction.on_commit(_send)
