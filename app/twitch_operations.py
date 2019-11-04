import requests
from environs import Env


class TwitchClient:
  """
  Twitch API client class.
  
  Methods:
    fetch_token
    fetch_user_id
    fetch_user_follow_list
    fetch_follow_list_streams
    subscribe_to_webhook
    fetch_webhook_subscriptions
  """
  def __init__(self):
    env = Env()
    env.read_env()

    self.BASE_URL = 'https://api.twitch.tv/helix'
    self.AUTH_URL = 'https://id.twitch.tv'
    self.TOKEN = env('TOKEN')
    self.HEADERS = {'Authorization': f'Bearer {self.TOKEN}'}
    self.CLIENT_ID = env('CLIENT_ID')
    self.CLIENT_SECRET = env('CLIENT_SECRET')
    self.GRANT_TYPE = 'client_credentials'
    self.user_follow_list_count = 0
    self.user_follow_list = []
    self.pagination_cursor = ''

  def _reset_user(self):
    self.user_follow_list_count = 0
    self.user_follow_list = []
    self.pagination_cursor = ''

  def fetch_token(self):
    url = f'{self.AUTH_URL}/oauth2/token?client_id={self.CLIENT_ID}&client_secret={self.CLIENT_SECRET}&grant_type={self.GRANT_TYPE}'
    res = requests.post(url)
    self.TOKEN = res.json()['access_token']

  def fetch_user_id(self, username):
    url = f'{self.BASE_URL}/users?login={username}'
    res = requests.get(url, headers=self.HEADERS)
    # If token is expired, get a new token and try again
    if res.status_code == 401:
      self.fetch_token()
      self.fetch_user_id(username)
    data = res.json()['data']
    # If no user is found
    if len(data) == 0:
      return False
    return data[0]['id']

  def fetch_user_follow_list(self, user_id, new_user=True):
    if new_user:
      self._reset_user()
    url = f'{self.BASE_URL}/users/follows?from_id={user_id}&first=100'
    if self.pagination_cursor != '':
      url = f'{url}&after={self.pagination_cursor}'
    res = requests.get(url, headers=self.HEADERS)
    # If token is expired, get a new token and try again
    if res.status_code == 401:
      self.fetch_token()
      self.fetch_user_follow_list(user_id)
    data = res.json()
    # Set count to the 'total' response value, on first page only
    if self.pagination_cursor == '':
      self.user_follow_list_count = data['total']
    self.user_follow_list_count -= 100
    self.user_follow_list.extend(data['data'])
    try:
      self.pagination_cursor = data['pagination']['cursor']
    except KeyError:
      pass

    if self.user_follow_list_count > 0:
      self.fetch_user_follow_list(user_id, False)
    return self.user_follow_list

  def fetch_follow_list_streams(self):
    streams = []
    self.pagination_cursor = ''
    start_index = 0
    stop_index = 100 if len(self.user_follow_list) > 100 else len(self.user_follow_list) - 1
    while start_index == 0 or stop_index < len(self.user_follow_list) - 1:
      parameter_string = self._build_url_parameter_string('user_id', self.user_follow_list[start_index:stop_index], 'to_id')
      url = f'{self.BASE_URL}/streams?{parameter_string}&first=100'
      if self.pagination_cursor != '':
        url += f'&after={self.pagination_cursor}'
      res = requests.get(url, headers=self.HEADERS)
      data = res.json()
      self.pagination_cursor = data['pagination']['cursor']
      streams.extend(data['data'])
      start_index += 100
      stop_index += 100
    self._fetch_stream_game_names(streams)
    self._replace_non_ascii_usernames(streams)
    return streams

  def _replace_non_ascii_usernames(self, streams):
    non_ascii_username_ids = []
    for stream in streams:
      try:
        stream['user_name'].encode('utf-8').decode('ascii')
      except UnicodeDecodeError:
        non_ascii_username_ids.append(stream['user_id'])
    if len(non_ascii_username_ids) > 0:
      users_dict = {}
      start_index = 0
      stop_index = 100
      while start_index == 0 or stop_index < len(non_ascii_username_ids) - 1:
        parameter_string = self._build_url_parameter_string('id', non_ascii_username_ids[start_index:stop_index])
        url = f'{self.BASE_URL}/users?{parameter_string}'
        res = requests.get(url, headers=self.HEADERS)
        data = res.json()['data']
        for user in data:
          users_dict[user['id']] = user['login']
        start_index += 100
        stop_index += 100
      for stream in streams:
        stream['user_name'] = users_dict.get(stream['user_id'], stream['user_name'])
    return streams

  def _fetch_stream_game_names(self, streams):
    game_ids = list(set([stream['game_id'] for stream in streams]))
    games_dict = {}
    start_index = 0
    stop_index = 100
    while start_index == 0 or stop_index < len(game_ids) - 1:
      parameter_string = self._build_url_parameter_string('id', game_ids[start_index:stop_index])
      url = f'{self.BASE_URL}/games?{parameter_string}'
      res = requests.get(url, headers=self.HEADERS)
      data = res.json()['data']
      for game in data:
        games_dict[game['id']] = game['name']
      start_index += 100
      stop_index += 100
    for stream in streams:
      stream['game_name'] = games_dict[stream['game_id']]
    return streams

  @staticmethod
  def _build_url_parameter_string(key_in_string, value_list, key_in_list=None):
    parameter_string = ''
    for value in value_list:
      query_value = value[key_in_list] if key_in_list else value
      parameter_string += f'{key_in_string}={query_value}'
      if value is not value_list[-1]:
        parameter_string += '&'
    return parameter_string

  def subscribe_to_webhook(self, lease_seconds=1800):
    url = f'{self.BASE_URL}/webhooks/hub'
    subscription_options = {
      'hub.callback': 'https://d757b8e0.ngrok.io/webhooks/subscriber',  # replace hardcoded value
      'hub.mode': 'subscribe',
      'hub.topic': f'{self.BASE_URL}/users?id=59156455',  # replace hardcoded value
      'hub.lease_seconds': lease_seconds,
    }
    res = requests.post(url, headers=self.HEADERS, json=subscription_options)
    return res

  def fetch_webhook_subscriptions(self):
    url = f'{self.BASE_URL}/webhooks/subscriptions'
    res = requests.get(url, headers=self.HEADERS)
    if res.status_code == 401:
      self.fetch_token()
      self.fetch_webhook_subscriptions()
    return res
