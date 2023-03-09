from flask import Blueprint
from flask import render_template

from ..models import Category
from ..deco import login_required


bp = Blueprint("category", __name__, url_prefix="/category")


@bp.get("/control")
@login_required
def control(user):
    return render_template(
        "category/control.jinja2",
        category_list=Category.query.all()
    )
