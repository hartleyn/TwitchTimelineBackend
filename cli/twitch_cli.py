import click
from app.twitch_operations import TwitchClient


@click.command()
@click.argument('twitch_username')
def fetch_follow_list_streams(twitch_username):
  twitch_client = TwitchClient()
  user_id = twitch_client.fetch_user_id(twitch_username)
  twitch_client.fetch_user_follow_list(user_id)
  streams = twitch_client.fetch_follow_list_streams()
  print(f'There are, currently, {len(streams)} channels streaming.\n')
  for stream in streams:
    print(f'{stream["user_name"]} is streaming {stream["game_name"]} for {stream["viewer_count"]} viewers.\n')


if __name__ == "__main__":
  fetch_follow_list_streams()
