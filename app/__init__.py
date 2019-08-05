from flask import Flask, make_response


def create_app():
  """
  Flask app factory function.
  """
  app = Flask(__name__)

  @app.route('/timeline/<username>')
  def fetch_twitch_timeline(username):
    res = make_response({'success': True}, 200)
    return res
  
  return app
