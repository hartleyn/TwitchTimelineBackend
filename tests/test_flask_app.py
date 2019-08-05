
def test_fetch_twitch_user_id(flask_app_client):
  res = flask_app_client.get('/timeline/nick_lenoir')
  assert res.status_code == 200
