from functools import wraps
from typing import Optional

from flask import session

from .models import User
from .utils import fail


def get_user(user_id: int) -> Optional[User]:
    return User.query.filter_by(
        id=user_id,
    ).first()


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            user_id = session['user.id']
        except KeyError:
            return fail("로그인이 필요합니다.")

        user = get_user(user_id)

        if user is None:
            return fail("삭제된 계정입니다.")

        return f(*args, **kwargs, user=user)

    return decorator


def login_not_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            user_id = session['user.id']
        except KeyError:
            return f(*args, **kwargs)

        user = get_user(user_id)

        if user is None:
            del session['user.id']
            return f(*args, **kwargs)

        return fail("해당 메뉴는 로그인 상태로 접근 할 수 없습니다.")

    return decorator
