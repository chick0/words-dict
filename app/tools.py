from .models import User
from .utils import get_avatar


def get_user_block(user_id: int) -> str:
    user: User = User.query.filter_by(
        id=user_id
    ).first()

    return f'<img class="rounded-circle me-2" width="32" src="{get_avatar(user)}" alt="{user.username}의 아바타">' + \
        f'<b>{user.username}</b><span class="text-muted">#{user.discriminator}</span>'
