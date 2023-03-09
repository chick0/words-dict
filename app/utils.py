from flask import Response
from flask import flash
from flask import redirect
from flask import url_for

from .models import User


def ok(message: str, move_to: str = "index.index", **values) -> Response:
    flash(message, "swal-success")
    return redirect(url_for(move_to, **values))  # type: ignore


def fail(message: str, move_to: str = "index.index", **values) -> Response:
    flash(message, "swal-error")
    return redirect(url_for(move_to, **values))  # type: ignore


def warning(message: str, move_to: str = "index.index", **values) -> Response:
    flash(message, "swal-warning")
    return redirect(url_for(move_to, **values))  # type: ignore


def get_avatar(user: User) -> str:
    return f"https://cdn.discordapp.com/avatars/{user.discord_id}/{user.avatar}.png"
