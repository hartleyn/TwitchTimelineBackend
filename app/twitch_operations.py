import requests
from environs import Env


class TwitchClient:
  """
  Twitch API client class.
  
  Methods:
    fetch_token
    fetch_user_id
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

  def reset_user(self):
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
      self.reset_user()
    url = f'{self.BASE_URL}/users/follows?from_id={user_id}&first=100'
    if self.pagination_cursor != '':
      url = f'{url}&after={self.pagination_cursor}'
    res = requests.get(url, headers=self.HEADERS)
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
