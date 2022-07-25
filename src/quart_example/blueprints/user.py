from dataclasses import asdict, dataclass
from typing import List

from orm import NoMatch
from quart import Blueprint
from quart_schema import validate_request, validate_response

from quart_example.models.user import User as UserModel

blueprint = Blueprint("users", __name__)


@dataclass
class UserIn:
    username: str
    email: str
    password: str


@dataclass
class User(UserIn):
    id: int


@dataclass
class Users:
    users: List[User]


@blueprint.get("/users/")
@validate_response(Users, 200)
async def get_users():
    users = await UserModel.objects.all()
    users = [user.__dict__ for user in users]
    return Users(users=users), 200


@blueprint.get("/users/<int:user_id>")
@validate_response(User, 200)
async def get_user(user_id):
    try:
        user = await UserModel.objects.get(id=user_id)
    except NoMatch:
        return {}, 404
    return User(**user.__dict__), 200


@blueprint.post("/users/")
@validate_request(UserIn)
@validate_response(User, 201)
async def create_user(data: UserIn):
    new_user: UserModel = await UserModel.objects.create(**asdict(data))
    return User(**new_user.__dict__), 201


@blueprint.delete("/users/<int:user_id>")
async def delete_user(user_id):
    await UserModel.objects.filter(id=user_id).delete()
    return {}, 204
