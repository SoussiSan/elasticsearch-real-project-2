import dataclasses
from typing import TYPE_CHECKING
from .models import User
import datetime
import jwt
from django.conf import settings

if TYPE_CHECKING:
    from .models import User


@dataclasses.dataclass
class UserDataClass:
    first_name: str
    last_name: str
    username: str
    country: str
    password: str = None
    email: str = None
    id: int = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            username=user.username,
            country=user.country,
            # id=user.id
        )


def create_user(user_dc: "UserDataClass") -> "UserDataClass":
    instance = User(
        first_name=user_dc.first_name,
        last_name=user_dc.last_name,
        email=user_dc.email,
        username=user_dc.username,
        country=user_dc.country,
    )
    if user_dc.password is not None:
        instance.set_password(user_dc.password)
    instance.save()
    return UserDataClass.from_instance(instance)


def user_username_selector(username: str) -> "User":
    user = User.objects.filter(username=username).first()
    return user


def create_token(user_id: str) -> str:
    payload = dict(
        id=user_id,
        exp=(datetime.datetime.utcnow() + datetime.timedelta(hours=24)).timestamp(),
        iot=(datetime.datetime.utcnow()).timestamp()
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token


