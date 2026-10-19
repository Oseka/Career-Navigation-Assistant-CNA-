import click
from flask import Flask


def register_seed_commands(app: Flask) -> None:
    @app.cli.command("seed")
    def seed_all():
        """Run all seed scripts (skills, assessment content, admin account)."""
        from app.seed.admin import seed_admin
        from app.seed.assessment import seed_assessment
        from app.seed.skills import seed_skills

        skills = _invoke(seed_skills)
        click.echo(f"skills: inserted {skills['inserted']}, already present {skills['skipped']}")

        assessment = _invoke(seed_assessment)
        click.echo(
            f"assessment: categories inserted {assessment['categories_inserted']}, "
            f"questions inserted {assessment['questions_inserted']}, "
            f"options inserted {assessment['options_inserted']}"
        )

        admin = _invoke(seed_admin)
        state = "created" if admin["created"] else "refreshed"
        click.echo(f"admin: {state} {admin['email']}")

    @app.cli.command("seed-skills")
    def seed_skills_command():
        """Seed the skills catalogue (insert-only, idempotent)."""
        from app.seed.skills import seed_skills

        result = _invoke(seed_skills)
        click.echo(f"skills: inserted {result['inserted']}, already present {result['skipped']}")

    @app.cli.command("seed-assessment")
    def seed_assessment_command():
        """Seed assessment categories, questions, and options (insert-only, idempotent)."""
        from app.seed.assessment import seed_assessment

        result = _invoke(seed_assessment)
        click.echo(
            f"assessment: categories inserted {result['categories_inserted']}, "
            f"questions inserted {result['questions_inserted']}, "
            f"options inserted {result['options_inserted']}"
        )

    @app.cli.command("seed-admin")
    def seed_admin_command():
        """Create or refresh the bootstrap admin from ADMIN_EMAIL/ADMIN_PASSWORD."""
        from app.seed.admin import seed_admin

        result = _invoke(seed_admin)
        state = "created" if result["created"] else "refreshed"
        click.echo(f"admin: {state} {result['email']}")


def _invoke(fn):
    try:
        return fn()
    except RuntimeError as exc:
        raise click.ClickException(str(exc)) from exc
