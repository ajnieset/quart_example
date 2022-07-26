from quart import Quart
from quart_schema import QuartSchema

from quart_example.blueprints.user import blueprint as user_blueprint
from quart_example.models.user import models

schema = QuartSchema(convert_casing=True)


def create_app() -> Quart:
    app = Quart(__name__)
    schema.init_app(app)

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    app.register_blueprint(user_blueprint)

    @app.before_serving
    async def migrate() -> None:
        await models.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
