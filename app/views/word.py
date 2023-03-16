from datetime import datetime

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from .. import db
from ..models import Word
from ..models import Category
from ..deco import login_required
from ..utils import ok
from ..utils import fail
from ..utils import get_category_name

bp = Blueprint("word", __name__, url_prefix="/word")


@bp.get("")
def index():
    word = Word.query.first()

    if word is None:
        return fail("등록된 단어가 없습니다!", "word.add")

    return redirect(url_for("word.get", category=get_category_name(word.category), word=word.word))


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
        word = request.form['word']
        meaning = request.form['meaning'].replace("<p>&nbsp;</p>", "").strip()
        category = request.form['category'].strip()
    except KeyError:
        return fail("단어 또는 설명을 입력하지 않았습니다.", "word.add")

    try:
        category = int(category)

        if Category.query.filter_by(
            id=category
        ).with_entities(
            Category.id
        ).first() is None:
            category = None
    except ValueError:
        category = None

    if Word.query.filter_by(
        word=word,
        category=category
    ).with_entities(
        Word.id
    ).first() is not None:
        return fail("한 카테고리안에 동일한 단어를 등록할 수 없습니다.")

    wd = Word()
    wd.author = user.id
    wd.category = category
    wd.word = word
    wd.meaning = meaning
    wd.created_at = datetime.now()

    db.session.add(wd)
    db.session.commit()

    ok("단어가 등록되었습니다.")
    return redirect(url_for("word.get", category=get_category_name(category), word=wd.word))


@bp.get("/<string:category>/<string:word>")
@login_required
def get(user, category: str, word: str):  # type: ignore
    if category == "-":
        category = None  # type: ignore
    else:
        category: Category = Category.query.filter_by(
            text=category
        ).first()

    if category is None:
        category_id = None
    else:
        category_id = category.id

    word: Word = Word.query.filter_by(
        category=category_id,
        word=word
    ).first()

    if word is None:
        return fail("등록된 단어가 아닙니다.<br>또는 카테고리가 변경되었습니다.", "word.add")

    return render_template(
        "word/get.jinja2",
        word=word
    )


@bp.get("/raw")
@login_required
def word_raw(user):
    word_id = request.args.get("id")

    word = Word.query.filter_by(
        id=word_id
    ).with_entities(
        Word.category,
        Word.word,
        Word.meaning
    ).first()

    if word is None:
        return {
            "status": False,
            "message": "등록된 단어가 아닙니다."
        }

    return {
        "status": True,
        "payload": {
            "category": word.category,
            "word": word.word,
            "meaning": word.meaning
        }
    }


@bp.get("/manage/<int:word_id>")
@login_required
def manage(user, word_id: int):
    return render_template(
        "word/manage.jinja2",
        category_list=Category.query.all(),
        word_id=word_id
    )


@bp.post("/manage/<int:word_id>")
@login_required
def manage_post(user, word_id: int):
    wd: Word = Word.query.filter_by(
        id=word_id
    ).first()

    if wd is None:
        return fail("등록된 단어가 아닙니다.")

    try:
        word = request.form['word']
        meaning = request.form['meaning'].replace("<p>&nbsp;</p>", "").strip()
        category = request.form['category'].strip()
    except KeyError:
        return fail("단어 또는 설명을 입력하지 않았습니다.", "word.add")

    try:
        category = int(category)

        if Category.query.filter_by(
            id=category
        ).with_entities(
            Category.id
        ).first() is None:
            category = None
    except ValueError:
        category = None

    if Word.query.filter_by(
        word=word,
        category=category
    ).filter(
        Word.id != word_id
    ).with_entities(
        Word.id
    ).first() is not None:
        return fail("한 카테고리안에 동일한 단어를 등록할 수 없습니다.")

    wd.author = user.id
    wd.category = category
    wd.word = word
    wd.meaning = meaning
    wd.updated_at = datetime.now()

    db.session.commit()

    ok("단어가 수정되었습니다.")
    return redirect(url_for("word.get", category=get_category_name(category), word=wd.word))


@bp.get("/delete/<int:word_id>")
@login_required
def delete(user, word_id: int):
    wd: Word = Word.query.filter_by(
        id=word_id
    ).with_entities(
        Word.category,
        Word.word
    ).first()

    if wd is None:
        return fail("등록된 단어가 아닙니다.")

    return render_template(
        "word/delete.jinja2",
        word=wd.word,
        href=url_for("word.get", category=get_category_name(wd.category), word=wd.word)
    )


@bp.post("/delete/<int:word_id>")
@login_required
def delete_post(user, word_id: int):
    Word.query.filter_by(
        id=word_id
    ).delete()

    db.session.commit()
    return ok("해당 단어가 삭제되었습니다.")
