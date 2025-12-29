from fastapi import Depends
from app.auth import get_current_user
from app.rate_limiter import rate_limit
from app.models import User


def status_rate_limit(
    current_user: User = Depends(get_current_user),
):
    rate_limit(
        key=f"status:{current_user.id}",
        limit=30,
        window_seconds=60,
    )


def check_now_rate_limit(
    current_user: User = Depends(get_current_user),
):
    rate_limit(
        key=f"check:{current_user.id}",
        limit=5,
        window_seconds=60,
    )
