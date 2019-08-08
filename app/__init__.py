from flask import Flask, make_response
from flask_cors import CORS
from .twitch_operations import TwitchClient
from .helpers import convert_date_string_to_datetime, build_follow_duration_string


def create_app():
  """
  Flask app factory function.
  """
  app = Flask(__name__)
  CORS(app, resources={r'/*': {'origins': 'http://localhost:3000'}})

  twitch_client = TwitchClient()

  @app.route('/timeline/<username>')
  def fetch_twitch_timeline(username):
    user_id = twitch_client.fetch_user_id(username)
    follow_list = twitch_client.fetch_user_follow_list(user_id)
    for user in follow_list:
      user['follow_duration'] = build_follow_duration_string(user['followed_at'])
      user['followed_at'] = convert_date_string_to_datetime(user['followed_at']).__str__()
    # Earliest follow first
    follow_list.reverse()
    res = make_response({'data': {'total': len(follow_list), 'follow_list': follow_list}}, 200)
    return res
  
  return app
