# dnd_builder/encounters.py
from flask import Blueprint, render_template

bp = Blueprint("encounter", __name__, url_prefix="/inn")

@bp.route("/")
def inn_landing():
    return render_template("inn.html")

# … all your other /hearth, /bar, /board, etc. routes …
