import pytest
from _pytest.monkeypatch import MonkeyPatch
from mongomock import MongoClient
import app
from app.config import TestingConfiguration


@pytest.fixture(scope="session")
def monkeysession(request):
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


# dummy class because mongomock.MongoClient has no "init__app" function
class PyMongoMock(MongoClient):
    def init_app(self, app):
        return super().__init__()


@pytest.fixture(scope="module")
def test_client(monkeysession):
    """yield the flask testing client
    """
    monkeysession.setattr(app.db, "pymongo", PyMongoMock())
    myapp = app.create_app(config_class=TestingConfiguration)
    # Create a test client using the Flask application configured for testing
    with myapp.test_client() as testing_client:
        # Establish an application context
        with myapp.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope="module")
def addModels(test_client):
    """add test data
    """
    pass


@pytest.fixture(scope="module")
def models(monkeysession):
    monkeysession.setattr(app.db, "pymongo", PyMongoMock())
