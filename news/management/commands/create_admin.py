import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update the Render admin superuser."


class Command(BaseCommand):
    help = "Create or update the Render admin superuser."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("ADMIN_USERNAME", "").strip()
        password = os.environ.get("ADMIN_PASSWORD", "").strip()

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "ADMIN_USERNAME or ADMIN_PASSWORD is not set. "
                    "Skipping admin setup."
                )
            )
            return

        # Find the requested admin by username.
        user = User.objects.filter(username=username).first()

        if user is None:
            # If the username does not exist, create the admin.
            user = User.objects.create_user(
                username=username,
                password=password,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin user '{username}' created successfully."
                )
            )

        else:
            # Existing admin: update password and permissions.
            user.set_password(password)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin user '{username}' updated successfully."
                )
            )

        # Always make sure the configured account has full admin access.
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(
            update_fields=[
                "password",
                "is_staff",
                "is_superuser",
                "is_active",
            ]
        )