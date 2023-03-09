from flask import redirect
from flask import url_for
from flask import render_template


class LetsGo(Exception):
    def __init__(self, target: str = "index.index") -> None:
        super().__init__()
        self.target = target


def lets_go_handler(error: LetsGo):
    return redirect(url_for(error.target))


def not_found_handler(error):
    return render_template(
        "404.jinja2"
    )
