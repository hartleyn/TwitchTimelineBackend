import pytest


def test_fetch_twitch_user_id(client):
  res = client.get('/timeline/nick_lenoir')
  assert res.status_code == 200
  