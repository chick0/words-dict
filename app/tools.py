from datetime import datetime
from datetime import timedelta

from flask import render_template_string
from jinja2 import Undefined
from mistune import html

from .models import User
from .utils import get_avatar


def markdown_to_html(markdown: str) -> str:
    return html(render_template_string(markdown))


def get_date(date: datetime) -> str:
    if date is None or isinstance(date, Undefined):
        return "-"

    return date.strftime("%Y년 %m월 %d일")


def timedelta_to_string(delta: timedelta) -> str:
    seconds = delta.total_seconds()
    display = ""

    h = int(seconds / 60 / 60)
    m = int((seconds / 60) % 60)
    s = int(seconds % 60)

    d = int(h / 24)

    if d > 0:
        h -= d * 24
        display += f"{d}일 "

    if h > 0:
        display += f"{h}시간 "

    if m > 0:
        display += f"{m}분 "

    if s > 0:
        display += f"{s}초"

    return display


def get_avatar_from_user(user: User) -> str:
    return get_avatar(user)
