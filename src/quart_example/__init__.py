from dataclasses import dataclass
from sqlite3 import dbapi2
from typing import List

from quart import Quart, g
from quart_schema import QuartSchema, validate_request, validate_response

app = Quart(__name__)
QuartSchema(app)


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


app.config.update(
    {
        "DATABASE": app.root_path / "user.db",
    }
)


def _connect_db():
    engine = dbapi2.connect(app.config["DATABASE"])
    engine.row_factory = dbapi2.Row
    return engine


def init_db():
    db = _connect_db()
    with open(app.root_path / "schema.sql", mode="r") as file_:
        db.cursor().executescript(file_.read())
    db.commit()


def _get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = _connect_db()
    return g.sqlite_db


@app.get("/users/")
@validate_response(Users, 200)
async def get_users():
    db = _get_db()
    cur = db.execute("""SELECT * FROM user ORDER BY id DESC""")

    rows = cur.fetchall()
    users = [User(**row) for row in rows]
    return Users(users=users), 200


@app.get("/users/<int:user_id>")
@validate_response(User, 200)
async def get_user(user_id):
    db = _get_db()
    cur = db.execute("SELECT * FROM user WHERE id = ? ORDER BY id DESC", [user_id])

    user = cur.fetchone()
    if user is None:
        return {}, 404
    return User(**user), 200


@app.post("/users/")
@validate_request(UserIn)
@validate_response(User, 201)
async def create_user(data: User) -> User:
    db = _get_db()
    cur = db.execute(
        "INSERT INTO user (username, email, password) VALUES (?, ?, ?)",
        [data.username, data.email, data.password],
    )
    db.commit()
    user_id = cur.lastrowid
    return User(id=user_id, username=data.username, email=data.email, password=data.password), 201


@app.delete("/users/<int:user_id>")
async def delete_user(user_id):
    db = _get_db()
    db.execute("DELETE FROM user WHERE id = ?", [user_id])
    db.commit()
    return {}, 204


@app.get("/health")
async def health():
    return {"status": "healthy"}


def run() -> None:
    app.run()
