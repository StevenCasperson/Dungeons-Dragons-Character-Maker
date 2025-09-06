import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# package‐level extension
db = SQLAlchemy()

def create_app():
    # determine project root (one level up from this file)
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )

    # point Flask at root‐level templates/ and static/ directories
    app = Flask(
        __name__,
        template_folder=os.path.join(project_root, "templates"),
        static_folder=os.path.join(project_root, "static")
    )

    # --- inject getattr/attribute into Jinja globals here ---
    app.jinja_env.globals['getattr']   = getattr
    app.jinja_env.globals['attribute'] = getattr

    # core configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-replace-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        os.environ.get("DATABASE_URL")
        or f"sqlite:///{os.path.join(project_root, 'dnd_builder.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # initialize extensions
    db.init_app(app)

    # register blueprints
    from .characters import bp as characters_bp
    from .encounters import bp as encounter_bp
    from .download   import bp as download_bp

    app.register_blueprint(characters_bp, url_prefix="/characters")
    app.register_blueprint(encounter_bp, url_prefix="/inn")
    app.register_blueprint(download_bp,  url_prefix="/download")

    # jinja filter for coin formatting
    @app.template_filter("format_coins")
    def format_coins_filter(coins: dict) -> str:
        parts = []
        for denom in ("pp", "gp", "sp", "cp"):
            count = coins.get(denom, 0)
            if count:
                parts.append(f"{count} {denom}")
        return ", ".join(parts) or "0 cp"

    return app
