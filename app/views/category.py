from typing import Optional

from flask import Blueprint
from flask import request
from flask import render_template

from .. import db
from ..models import Category
from ..models import Word
from ..deco import login_required
from ..utils import ok
from ..utils import fail

bp = Blueprint("category", __name__, url_prefix="/category")


@bp.get("")
@login_required
def get_category_list(user):
    return [
        {
            "id": category.id,
            "text": category.text,
            "parent": category.parent
        } for category in Category.query.all()
    ]


@bp.get("/<int:catogory_id>/detail")
@login_required
def get_category_detail(user, catogory_id: int):
    category = Category.query.filter_by(
        id=catogory_id
    ).first()

    if category is None:
        return {}

    return {
        "id": category.id,
        "text": category.text,
        "parent": category.parent
    }


def is_that_category_can_be_parent(category_id: int):
    category = Category.query.filter_by(
        id=category_id
    ).first()

    if category is None:
        return None

    return category.parent is None


@bp.get("/<int:category_id>/parent-able")
@login_required
def check_parent_able(user, category_id: int):
    return {
        "result": is_that_category_can_be_parent(category_id)
    }


@bp.get("/control")
@login_required
def control(user):
    return render_template(
        "category/control.jinja2",
        category_list=Category.query.all()
    )


@bp.post("/control")
@login_required
def control_post(user):
    json: dict = request.get_json(silent=True)  # type: ignore

    try:
        category_id = json['id']

        if category_id != "new":
            category_id = int(category_id)
    except KeyError:
        return {
            "status": False,
            "message": "카테고리 식별자가 누락되었습니다."
        }
    except (ValueError, TypeError):
        return {
            "status": False,
            "message": "카테고리 식별자 값이 올바르지 않습니다."
        }

    category: Category = Category()

    if category_id != "new":
        category = Category.query.filter_by(
            id=category_id
        ).first()

        if category is None:
            return {
                "status": False,
                "message": "해당 카테고리는 등록된 카테고리가 아닙니다."
            }

    try:
        text = json['text'].strip()

        if text == "-":
            return {
                "status": False,
                "message": "해당 카테고리 이름은 사용할 수 없습니다.<br>시스템이 사용중인 카테고리 입니다."
            }
    except KeyError:
        return {
            "status": False,
            "message": "카테고리 이름이 누락되었습니다."
        }

    if len(text) == 0:
        if category_id == "new":
            return {
                "status": False,
                "message": "카테고리 이름을 입력해야 새 카테고리를 생성할 수 있습니다."
            }

        # 1단계) 해당 카테고리를 사용하는 단어가 없는지 확인
        searched_word = Word.query.filter_by(
            category=category_id
        ).with_entities(
            Word.word
        ).first()

        if searched_word is not None:
            return {
                "status": False,
                "message": f"해당 카테고리는 삭제될 수 없습니다.<br>{searched_word.word!r} 단어가 해당 카테고리를 사용하고 있습니다."
            }

        # 2단계) 해당 카테고리를 상위 카테고리로 사용하는 경우가 없는지 확인
        first_child = Category.query.filter_by(
            parent=category_id
        ).with_entities(
            Category.text
        ).first()

        if first_child is not None:
            return {
                "status": False,
                "message": f"해당 카테고리는 삭제될 수 없습니다.<br>{first_child.text!r} 카테고리가 해당 카테고리를 상위 카테고리로 설정하고 있습니다."
            }

        db.session.delete(category)
        db.session.commit()

        ok("해당 카테고리가 삭제되었습니다.")
        return {"status": True}

    try:
        parent = int(json['parent'].strip())
    except KeyError:
        return {
            "status": False,
            "message": "상위 카테고리 속성이 누락되었습니다."
        }
    except (ValueError, TypeError):
        return {
            "status": False,
            "message": "상위 카테고리 식별자 값이 올바르지 않습니다."
        }

    if parent < 0:
        # 상위 카테고리 없음
        parent = None
    else:
        if parent == category_id:
            return {
                "status": False,
                "message": "자기 자신을 상위 카테고리로 설정 할 수 없습니다.<br>다른 카테고리를 선택해주세요."
            }

        parent_able = is_that_category_can_be_parent(parent)

        if parent_able is not True:
            return {
                "status": False,
                "message": "해당 카테고리는 상위 카테고리가 될 수 없습니다.<br>다른 카테고리를 선택해주세요."
            }

    if category_id != "new" and category.parent is None and parent is not None:
        # 상위 카테고리가 상위 카테고리를 설정하는 상황임
        # 하위 카테고리를 상위 카테고리로 선택한다면 거부하기
        if Category.query.filter_by(
            parent=category_id
        ).count() != 0:
            return {
                "status": False,
                "message": "상위 카테고리는 하위 카테고리가 될 수 없습니다."
            }

    if Category.query.filter_by(
        text=text
    ).filter(
        Category.id != category_id
    ).with_entities(
        Category.id
    ).first() is not None:
        return {
            "status": False,
            "message": "이름이 동일한 카테고리는 생성할 수 없습니다."
        }

    category.text = text
    category.parent = parent

    if category_id == "new":
        db.session.add(category)

    db.session.commit()

    ok("변경사항이 저장되었습니다.")
    return {"status": True}


@bp.get("/area/<string:category_text>")
@bp.get("/area/<string:category_text>/<string:subcategory_text>")
@login_required
def area(user, category_text: str, subcategory_text: Optional[str] = None):
    if category_text == "-":
        return render_template(
            "category/area.jinja2",
            category=None,
            word_list=Word.query.filter_by(
                category=None
            ).all()
        )

    parent = Category.query.filter_by(
        text=category_text
    ).first()

    if parent is None:
        return fail("등록된 카테고리가 아닙니다.")

    if subcategory_text is None:
        cd = parent
    else:
        cd = Category.query.filter_by(
            text=subcategory_text,
            parent=parent.id
        ).first()

        if cd is None:
            return fail("등록된 카테고리가 아닙니다.")

    return render_template(
        "category/area.jinja2",
        category=cd,
        word_list=Word.query.filter_by(
            category=cd.id
        ).all()
    )
