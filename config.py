import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ── Segurança ──────────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-mude-em-producao"

    SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutos

    # ── Banco de dados ────────────────────────────────────────────────────
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///agenorconect.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── WTForms / CSRF ────────────────────────────────────────────────────
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
