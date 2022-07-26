from dataclasses import asdict, dataclass

from orm import NoMatch
from quart import Blueprint
from quart_schema import validate_request, validate_response

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
    password: str


@dataclass
class Users:
    users: list[UserData]


@blueprint.get("/users/<int:user_id>")
@validate_response(UserData, 200)
async def get_user(user_id):
    try:
        user = await User.objects.get(id=user_id)
    except NoMatch:
        return {}, 404
    return UserData(**user.__dict__), 200


@blueprint.get("/users/")
@validate_response(Users)
async def get_users():
    users = await User.objects.all()
    users = [UserData(**user.__dict__) for user in users]
    return Users(users=users), 200


@blueprint.post("/users/")
@validate_request(UserIn)
@validate_response(UserData, 201)
async def create_user(data: UserIn):
    new_user: User = await User.objects.create(**asdict(data))
    return UserData(**new_user.__dict__), 201


@blueprint.delete("/users/<int:user_id>")
async def delete_user(user_id):
    await User.objects.filter(id=user_id).delete()
    return {}, 204
