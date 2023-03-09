from os import environ
from typing import NamedTuple

from flask import url_for
from requests import get
from requests import post

from .const import DISCORD_API_BASE_URL as BASE_URL
from .utils import fail
from .error import LetsGo


class DiscordUserData(NamedTuple):
    discord_id: str
    username: str
    discriminator: str
    avatar: str


def get_auth_token(code: str) -> str:
    response = post(
        f"{BASE_URL}/oauth2/token",
        data={
            "client_id": environ['CLIENT_ID'],
            "client_secret": environ['CLIENT_SECRET'],
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": environ['BASE_URL'] + url_for("auth.callback")
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    if response.status_code != 200:
        fail("로그인에 실패했습니다. 다시 시도해주세요.")
        raise LetsGo

    json = response.json()
    access_token = json.get("access_token", "")

    return access_token


def get_user_data_with_token(access_token: str) -> DiscordUserData:
    response = get(
        f"{BASE_URL}/users/@me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    if response.status_code != 200:
        fail("유저 정보를 불러오는데 실패했습니다. 다시 로그인해주세요.")
        raise LetsGo

    json = response.json()

    return DiscordUserData(
        discord_id=json['id'],
        username=json['username'],
        discriminator=json['discriminator'],
        avatar=json['avatar']
    )
