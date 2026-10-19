import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env", override=False)


class Config:
    def __init__(self) -> None:
        self.SECRET_KEY = os.environ.get("SECRET_KEY")
        self.SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        # init_command pins every connection to UTC so NOW()/CURRENT_TIMESTAMP
        # store UTC values (ADR-0010).
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_recycle": 3600,
            "connect_args": {"init_command": "SET time_zone = '+00:00'"},
        }
        self.SESSION_LIFETIME_MINUTES = int(os.environ.get("SESSION_LIFETIME_MINUTES", "10080"))
        self.SESSION_LIFETIME = timedelta(minutes=self.SESSION_LIFETIME_MINUTES)
        self.DEBUG = False
        self.TESTING = False

    def validate_required(self) -> None:
        required = ("SECRET_KEY", "SQLALCHEMY_DATABASE_URI")
        missing = [name for name in required if not getattr(self, name)]
        if missing:
            raise RuntimeError(
                f"Missing required environment variable(s): {', '.join(missing)}. "
                "Copy backend/.env.example to backend/.env and set them."
            )


class DevelopmentConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.DEBUG = True


class TestingConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.TESTING = True
        self.SECRET_KEY = self.SECRET_KEY or "testing-secret-key"


class ProductionConfig(Config):
    pass


_CONFIGS = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(env: str | None = None) -> Config:
    env = (env or os.environ.get("FLASK_ENV", "development")).lower()
    config_cls = _CONFIGS.get(env)
    if config_cls is None:
        raise ValueError(f"Unknown FLASK_ENV '{env}' (expected one of: {', '.join(_CONFIGS)})")
    config = config_cls()
    config.validate_required()
    return config
