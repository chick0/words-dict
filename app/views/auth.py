from os import environ
from datetime import datetime

from flask import Blueprint
from flask import session
from flask import request
from flask import redirect
from flask import url_for

from .. import db
from ..models import User
from ..utils import fail
from ..deco import login_not_required
from ..discord import get_auth_token
from ..discord import get_user_data_with_token

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("index.index"))


@bp.get("/login")
@login_not_required
def login():
    return redirect(
        "https://discord.com/api/oauth2/authorize"
        "?client_id=" + environ['CLIENT_ID'] +
        "&redirect_uri=" + environ['BASE_URL'] + url_for("auth.callback") +
        "&response_type=code"
        "&scope=identify"
    )


@bp.get("/callback")
@login_not_required
def callback():
    code = request.args.get("code", "")

    if len(code) == 0:
        return fail("로그인 요청이 올바르지 않습니다. 다시 한 번 시도해주세요.")

    token = get_auth_token(code)
    user_data = get_user_data_with_token(token)

    user: User = User.query.filter_by(
        discord_id=user_data.discord_id
    ).first()

    if user is None:
        return fail("등록된 사용자만 로그인 할 수 있습니다.")
    else:
        # 로그인 할 때 마다 값 업데이트
        user.username = user_data.username
        user.discriminator = user_data.discriminator
        user.avatar = user_data.avatar

    user.lastlogin = datetime.now()
    db.session.commit()

    session['user.id'] = user.id
    return redirect(url_for("index.index"))
