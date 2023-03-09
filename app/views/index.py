from flask import Blueprint
from flask import session
from flask import redirect
from flask import url_for
from flask import render_template

bp = Blueprint("index", __name__, url_prefix="/")


@bp.get("")
def index():
    if "user.id" in session:
        return redirect(url_for("word.index"))

    return render_template(
        "index/index.jinja2"
    )
