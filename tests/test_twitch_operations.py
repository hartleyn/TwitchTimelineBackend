import pytest
from app.twitch_operations import TwitchClient


def test_fetch_twitch_user_id(twitch_client):
  user_id = twitch_client.fetch_user_id('nick_lenoir')  
  assert user_id == '59156455'

def test_fetch_user_follow_list(twitch_client):
  follow_list = twitch_client.fetch_user_follow_list('59156455')
  assert len(follow_list) > 0
  if twitch_client.user_follow_list_count > 0:
    assert len(twitch_client.pagination_cursor) > 0

def test_reset_user(twitch_client):
  twitch_client.fetch_user_follow_list('59156455')
  twitch_client._reset_user()
  assert len(twitch_client.user_follow_list) == 0

@pytest.mark.parametrize('key_in_string, value_list, key_in_list, expected_string', (
  (
    'user_id', 
    (
      {'from_id': '59156455', 'from_name': 'nick_lenoir', 'to_id': '195166073', 'to_name': 'HAchubby', 'followed_at': '2019-09-19T05:17:16Z'},
      {'from_id': '59156455', 'from_name': 'nick_lenoir', 'to_id': '79122704', 'to_name': 'Javion', 'followed_at': '2019-09-12T08:44:40Z'},
      {'from_id': '59156455', 'from_name': 'nick_lenoir', 'to_id': '52326616', 'to_name': 'Sunny', 'followed_at': '2019-09-04T12:26:18Z'},
      {'from_id': '59156455', 'from_name': 'nick_lenoir', 'to_id': '193785576', 'to_name': '콩만한정은이', 'followed_at': '2019-08-30T13:08:55Z'},
      {'from_id': '59156455', 'from_name': 'nick_lenoir', 'to_id': '157970655', 'to_name': 'Myrilliaa', 'followed_at': '2019-08-28T18:15:39Z'},
    ), 
    'to_id',
    'user_id=195166073&user_id=79122704&user_id=52326616&user_id=193785576&user_id=157970655',
  ),
  (
    'id',
    (
      '101',
      '202',
      '303',
    ),
    None,
    'id=101&id=202&id=303',
  ),
))
def test_build_url_parameter_string(twitch_client, key_in_string, value_list, key_in_list, expected_string):
  url_paramater_string = twitch_client._build_url_parameter_string(key_in_string, value_list, key_in_list)
  assert url_paramater_string == expected_string
