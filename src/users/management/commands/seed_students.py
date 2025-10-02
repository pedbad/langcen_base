# src/users/management/commands/seed_students.py
import csv
from pathlib import Path
from typing import Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Seed student users from a CSV.\n"
        "Columns supported: email[,first_name,last_name,password]\n"
        "Extra CSV columns are ignored safely.\n\n"
        "Examples:\n"
        "  python src/manage.py seed_students students.csv --dry-run\n"
        "  python src/manage.py seed_students students.csv --default-password=ChangeMe123!\n"
        "  python src/manage.py seed_students students.csv --default-password=ChangeMe123!"
        " --update\n"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_path",
            type=str,
            help="Path to CSV file. Must at least include the 'email' column.",
        )
        parser.add_argument(
            "--default-password",
            dest="default_password",
            default=None,
            help="If provided, rows without a password will use this value.",
        )
        parser.add_argument(
            "--update",
            action="store_true",
            help="Update first/last name and password for existing users with the same email.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and report without writing to the database.",
        )

    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"])
        default_password: Optional[str] = options["default_password"]
        update: bool = options["update"]
        dry_run: bool = options["dry_run"]

        if not csv_path.exists():
            raise CommandError(f"CSV not found: {csv_path}")

        # --- Pass 1: validate headers ----------------------------------------
        try:
            with csv_path.open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
        except Exception as exc:
            raise CommandError(f"Could not read CSV: {exc}") from exc

        if "email" not in headers:
            raise CommandError("CSV must include an 'email' column.")

        self.stdout.write(self.style.NOTICE("== seed_students starting =="))
        self.stdout.write(f"File: {csv_path}")
        self.stdout.write(f"Headers: {headers}")
        self.stdout.write(
            f"Options: default_password={'***' if default_password else None}, "
            f"update={update}, dry_run={dry_run}"
        )

        created = 0
        updated = 0
        skipped = 0
        invalid = 0
        rows = 0

        # --- Pass 2: process rows --------------------------------------------
        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows += 1

                # --- sanitize inputs -----------------------------------------
                raw_email = (row.get("email") or "").strip()
                email = raw_email.lower()  # normalize

                if not email:
                    skipped += 1
                    self.stdout.write(self.style.WARNING(f"[row {rows}] missing email → skip"))
                    continue

                try:
                    validate_email(email)
                except ValidationError:
                    invalid += 1
                    self.stdout.write(
                        self.style.WARNING(f"[row {rows}] invalid email '{raw_email}' → skip")
                    )
                    continue

                first_name = (row.get("first_name") or "").strip()
                last_name = (row.get("last_name") or "").strip()

                # password: CSV > --default > unusable (None)
                csv_pwd = (row.get("password") or "").strip()
                chosen_pwd = csv_pwd or (default_password or "")
                password_arg = chosen_pwd or None  # None → unusable

                # --- upsert logic --------------------------------------------
                try:
                    user = User.objects.get(email=email)
                    if update:
                        changed = False
                        if first_name and user.first_name != first_name:
                            user.first_name = first_name
                            changed = True
                        if last_name and user.last_name != last_name:
                            user.last_name = last_name
                            changed = True
                        if chosen_pwd:  # only reset password if we have a value
                            user.set_password(chosen_pwd)
                            changed = True

                        if changed:
                            if dry_run:
                                updated += 1
                                self.stdout.write(
                                    self.style.SUCCESS(f"[row {rows}] would update: {email}")
                                )
                            else:
                                user.save()
                                updated += 1
                                self.stdout.write(
                                    self.style.SUCCESS(f"[row {rows}] updated: {email}")
                                )
                        else:
                            skipped += 1
                            self.stdout.write(f"[row {rows}] no changes: {email}")
                    else:
                        skipped += 1
                        self.stdout.write(f"[row {rows}] exists → skip: {email}")

                except User.DoesNotExist:
                    if dry_run:
                        created += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"[row {rows}] would create: {email} (student)")
                        )
                    else:
                        User.objects.create_user(
                            email=email,
                            password=password_arg,  # manager handles hashing/unusable
                            role=User.Roles.STUDENT,
                            first_name=first_name,
                            last_name=last_name,
                            is_active=True,
                        )
                        created += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"[row {rows}] created: {email} (student)")
                        )

        # --- Summary ---------------------------------------------------------
        self.stdout.write(
            self.style.NOTICE(
                f"rows={rows} created={created} updated={updated} "
                f"skipped={skipped} invalid_email={invalid} dry_run={dry_run}"
            )
        )

        self.stdout.write(self.style.SUCCESS("Done."))
