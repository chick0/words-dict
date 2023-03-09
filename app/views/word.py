from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from .. import db
from ..models import Word
from ..models import Category
from ..deco import login_required
from ..utils import fail

bp = Blueprint("word", __name__, url_prefix="/word")


@bp.get("")
def index():
    word = Word.query.first()

    if word is None:
        return fail("등록된 단어가 없습니다!", "word.add")

    return redirect(url_for("word.get", query=word.word))


@bp.get("/add")
@login_required
def add(user):
    return render_template(
        "word/add.jinja2",
        category_list=Category.query.all()
    )


@bp.post("/add")
@login_required
def add_post(user):
    try:
        word = Word()
        word.word = request.form['word']
        word.meaning = request.form['meaning'].replace("<p>&nbsp;</p>", "").strip()
    except KeyError:
        return fail("단어 또는 설명을 입력하지 않았습니다.", "word.add")

    db.session.add(word)
    db.session.commit()

    return redirect(url_for("word.get", query=word.word))


@bp.get("/<string:query>")
@login_required
def get(user, query: str):
    return query
