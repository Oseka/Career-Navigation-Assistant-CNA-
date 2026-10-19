from flask import Flask

from app.config import get_config


def create_app(env: str | None = None) -> Flask:
    app = Flask("cna")
    app.config.from_object(get_config(env))

    from app.extensions import db, migrate

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  # noqa: F401  (registers models on db.metadata)
    from app.errors import register_error_handlers
    from app.seed import register_seed_commands

    register_error_handlers(app)
    register_seed_commands(app)

    from app.api import register_blueprints

    register_blueprints(app)

    return app
