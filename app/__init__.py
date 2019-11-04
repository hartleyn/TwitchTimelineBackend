from flask import Flask, make_response, request
from flask_cors import CORS
#from flask_ask import Ask, statement, question
from .twitch_operations import TwitchClient
from .helpers import convert_date_string_to_datetime, build_follow_duration_string


#ask = Ask()

def create_app():
  """
  Flask app factory function.
  """
  app = Flask(__name__)
  #ask.init_app(app)
  CORS(app, resources={r'/*': {'origins': [
    'http://localhost:3000', 
    'https://competent-hugle-41176c.netlify.com', 
    'https://api.twitch.tv/helix'
  ]}})

  twitch_client = TwitchClient()

  @app.route('/timeline/<username>')
  def fetch_twitch_timeline(username):
    user_id = twitch_client.fetch_user_id(username)
    # Return 404 if username search returns no result
    if not user_id:
      res = make_response({'error': 'No user found.'}, 404)
      return res
    follow_list = twitch_client.fetch_user_follow_list(user_id)
    for user in follow_list:
      user['follow_duration'] = build_follow_duration_string(user['followed_at'])
      user['followed_at'] = convert_date_string_to_datetime(user['followed_at']).__str__()
    # Earliest follow first
    follow_list.reverse()
    res = make_response({'data': {'total': len(follow_list), 'follow_list': follow_list}}, 200)
    return res

  @app.route('/webhooks/subscriber', methods=['GET', 'POST'])
  def receive_webhook_message():
    if request.method == 'POST':
      print(request.data)
      res = make_response({'success': True}, 200)
    else:
      challenge_token = request.args.get('hub.challenge')
      res = make_response(challenge_token, 200)
    return res

  '''
  @ask.launch
  def start_skill():
    msg = 'Hello, can I find something on Twitch for you?'
    return question(msg)
  '''

  return app
