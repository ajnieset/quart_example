import orm
from databases import Database

database = Database("sqlite:///db.sqlite")
models = orm.ModelRegistry(database=database)


class User(orm.Model):
    tablename = "users"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "username": orm.String(max_length=100),
        "email": orm.String(max_length=100),
        "password": orm.String(max_length=100),
    }
