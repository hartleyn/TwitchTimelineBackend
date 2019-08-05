import pytest
from app import create_app, twitch_operations


@pytest.fixture
def flask_app_client():
  app = create_app()
  with app.test_client() as client:
    client.testing = True
    yield client

@pytest.fixture(scope='module')
def twitch_client():
  client = twitch_operations.TwitchClient()
  return client
