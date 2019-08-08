
def test_get_user_timeline(flask_app_client):
  res = flask_app_client.get('/timeline/nick_lenoir')
  assert res.status_code == 200
