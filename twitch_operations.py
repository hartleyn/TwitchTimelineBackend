import requests


BASE_URL = 'https://api.twitch.tv'

def fetch_token(client_id, client_secret, grant_type):
  url = f'{BASE_URL}/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type={grant_type}'
  res = requests.post(url)

def fetch_user_id(username):
  url = f'{BASE_URL}/users?login={username}'
  res = requests.get(url)
  
