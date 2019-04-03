import mongoengine

from app import app
from app import resources


def create_app(**kwargs):
    """
    Initialize Flask applicaton
    """
    app.config.from_object('app.settings')
    app.config.update(**kwargs)

    mongoengine.connect(
        app.config['DATABASE_NAME'],
        host=app.config['DATABASE_HOST'],
        port=app.config['DATABASE_PORT'],
    )

    return app
