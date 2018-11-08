from pprint import pprint
import requests
from spotipy.util import prompt_for_user_token
from sklearn.cluster import KMeans
import pylab as pl
import pandas as pd
import json

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


def thowing_elbows(x: list):
    num_of_classes = range(1, 20)
    kmeans = [KMeans(n_clusters=n) for n in num_of_classes]
    score = [kmeans[i].fit(x).score(x) for i in range(len(kmeans))]
    pl.plot(num_of_classes, score)
    pl.xlabel("Number of Cluster")
    pl.ylabel("Score")
    pl.title("Elbow Curve")
    pl.show()


def main():
    set_head()

    top_medium = get_top_tracks(limit=50)["items"]
    top_short = get_top_tracks(limit=50, time_range="short_term")["items"]

    tops = top_medium + top_short

    ids = [e["id"] for e in tops]
    data = list()
    features = get_features(ids)

    for f in features:
        data_line = [f[key] for key in f.keys()]
        data.append(data_line[:-7])

    k_means = KMeans(n_clusters=5).fit(data)
    print(k_means.labels_)


def main_pandas():
    set_head()

    top_medium = get_top_tracks(limit=50)["items"]
    top_short = get_top_tracks(limit=50, time_range="short_term")["items"]

    tops = top_medium + top_short

    ids = [e["id"] for e in tops]
    features = get_features(ids)

    df: pd.DataFrame = pd.read_json(json.dumps(features))
    df = df.drop(["analysis_url", "duration_ms", "id", "time_signature", "track_href",
                  "type", "uri"], axis=1)
    print(df.head())

    kmeans = KMeans(n_clusters=5).fit(df)
    print(kmeans.labels_)




if __name__ == '__main__':
    # main()
    main_pandas()
