import spotipy
from spotipy.util import prompt_for_user_token
from pprint import pprint
CLIENT_ID = "1f6ebe9f1c8e4478a3ed3a6a3b071859"
CLIENT_SECRET = "89efae6388b8468baac49203496a77f6"
REDIRECT_URI = "http://localhost/"
sp: spotipy.Spotify = None


def main():
    global sp
    scopes = "user-top-read"
    token = prompt_for_user_token("", scopes, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    sp = spotipy.Spotify(token)
    top = sp.current_user_top_tracks(time_range="short_term")
    print(top["items"][0]["name"])
    pprint(get_features(top["items"][0]["id"]))


def get_features(id):
    features = sp.audio_features([id])
    return features


if __name__ == '__main__':
    main()

#thats me