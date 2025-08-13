import os
import sys
import pathlib
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app as flask_app


@pytest.fixture(scope="session")
def app():
    # Configure for testing
    flask_app.config.update(
        TESTING=True,
        SECRET_KEY='test-secret',
    )
    return flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def app_context(app):
    with app.app_context():
        yield


