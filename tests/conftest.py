import pytest

from app import create_app
from app.config import TestingConfiguration


@pytest.fixture(scope="module")
def test_client():
    """yield the flask testing client

    :param config: Configuration class
    :type config: TestingConfiguration
    """

    app = create_app(config_class=TestingConfiguration)
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!
