from quart import Quart, ResponseReturnValue
from quart_schema import QuartSchema

from quart_example.blueprints.users import blueprint as users_blueprint
from quart_example.lib.errors import APIError
from quart_example.models.user import models

schema = QuartSchema(convert_casing=True)


def create_app() -> Quart:
    app = Quart(__name__)
    schema.init_app(app)

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    app.register_blueprint(users_blueprint)

    # Define Error Handler
    @app.errorhandler(APIError)  # type: ignore
    async def handle_api_error(error: APIError) -> ResponseReturnValue:
        return {"detail": error.detail}, error.status_code

    @app.before_serving
    async def migrate() -> None:
        await models.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
