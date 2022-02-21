from __future__ import annotations

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to migrate the database."""

    help = "Remove virtual organization of the helmholtz AAI without users."

    def add_arguments(self, parser):
        """Add connection arguments to the parser."""

        parser.add_argument(
            "-e",
            "--exclude",
            help=(
                "Exclude VOs that match the following pattern. This argument "
                "can be specified multiple times."
            ),
            action="append",
            default=[],
        )

        parser.add_argument(
            "-y",
            "--yes",
            action="store_true",
            dest="without_confirmation",
            help="Remove the VOs without asking for confirmation.",
        )

        parser.add_argument(
            "-db",
            "--database",
            help=(
                "The Django database identifier (see settings.py), "
                "default: %(default)s"
            ),
            default="default",
        )

    def handle(
        self,
        *args,
        database: str = "default",
        exclude: list[str] = [],
        without_confirmation: bool = False,
        **options,
    ):
        """Migrate the database."""
        from django_helmholtz_aai import models

        models.HelmholtzVirtualOrganization.objects.using(
            database
        ).remove_empty_vos(
            exclude=exclude, without_confirmation=without_confirmation
        )
