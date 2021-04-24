from app.twitch_operations import TwitchClient


tc = TwitchClient()
tc.fetch_token()

pagination_cursor = ''
clip_links = []

while True:
    url = 'https://api.twitch.tv/helix/clips?broadcaster_id=83402203&first=100'
    url += f'&after={pagination_cursor}' if pagination_cursor else ''

    res = tc.session.get()
    res.raise_for_status()

    data = res.json()

    clip_links.extend([clip.get('url') for clip in data.get('data')])
    print(len(clip_links))

    if len(data.get('data')) < 100 or not data.get('pagination'):
        break
    pagination_cursor = data.get('pagination')
