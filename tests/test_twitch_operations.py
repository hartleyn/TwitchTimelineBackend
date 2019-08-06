from app.twitch_operations import TwitchClient


def test_fetch_twitch_user_id(twitch_client):
  user_id = twitch_client.fetch_user_id('nick_lenoir')  
  assert user_id == '59156455'

def test_fetch_user_follow_list(twitch_client):
  follow_list = twitch_client.fetch_user_follow_list('59156455')
  assert len(follow_list) > 0
  if twitch_client.user_follow_list_count > 0:
    assert len(twitch_client.pagination_cursor) > 0
