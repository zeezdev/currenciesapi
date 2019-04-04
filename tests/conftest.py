import sys
import pytest

sys.path.append('..')
from app.create_app import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    yield app
    # finalize here something


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
