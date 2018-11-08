from pprint import pprint
import requests
from spotipy.util import prompt_for_user_token

CLIENT_ID = "1f6ebe9f1c8e4478a3ed3a6a3b071859"
CLIENT_SECRET = "89efae6388b8468baac49203496a77f6"
REDIRECT_URI = "http://localhost/"

head: any = None


def get_top_tracks(time_range="medium_term", limit=20, offset=0):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range={}&limit={}&offset={}".format(time_range, limit, offset)
    response = requests.get(url, headers=head).json()
    return response


def get_features(ids):
    url = "https://api.spotify.com/v1/audio-features/?ids={}".format(",".join(ids))
    features = requests.get(url, headers=head).json()
    return features["audio_features"]


def get_data_from_track_id(id):
    f = get_features(id)
    l = list()
    for fe in f:
        l.append([fe[key] for key in fe.keys()][:-7])
    return l


def set_head():
    global head
    scopes = "user-top-read"
    token = prompt_for_user_token("", scopes, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    head = {
        'Authorization': 'Bearer ' + token
    }


def main():
    set_head()

    top = get_top_tracks(limit=50)["items"]

    data = list()
    x = [e["id"] for e in top]
    features = get_features(x)
    for f in features:
        data_line = [f[key] for key in f.keys()]
        data.append(data_line[:-7])


if __name__ == '__main__':
    main()
