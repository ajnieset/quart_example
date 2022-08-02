from dataclasses import asdict, dataclass

import bcrypt
from orm import NoMatch
from quart import Blueprint
from quart_schema import validate_request, validate_response

from quart_example.lib.errors import APIError
from quart_example.models.user import User

blueprint = Blueprint("users", __name__)


@dataclass
class UserIn:
    username: str
    email: str
    password: str


@dataclass
class UserData:
    id: int
    username: str
    email: str


@dataclass
class Users:
    users: list[UserData]


@blueprint.get("/users/<int:user_id>")
@validate_response(UserData, 200)
async def get_user(user_id):
    try:
        user: User = await User.objects.get(id=user_id)
    except NoMatch:
        raise APIError(404, "Not Found")
    return user.asdict(), 200


@blueprint.get("/users/")
@validate_response(Users)
async def get_users():
    users: list[User] = await User.objects.all()
    users = [UserData(**user.asdict()) for user in users]
    return users, 200


@blueprint.post("/users/")
@validate_request(UserIn)
@validate_response(UserData, 201)
async def create_user(data: UserIn):
    data.password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode()
    new_user: User = await User.objects.create(**asdict(data))
    return new_user.asdict(), 201


@blueprint.delete("/users/<int:user_id>")
async def delete_user(user_id):
    await User.objects.filter(id=user_id).delete()
    return {}, 204
