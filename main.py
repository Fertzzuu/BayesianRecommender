import json

import pandas as pd
import pylab as pl
import requests
from spotipy.util import prompt_for_user_token
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans

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


def main_pandas():
    set_head()

    top_medium = get_top_tracks(limit=50)["items"]
    top_short = get_top_tracks(limit=50, time_range="short_term")["items"]

    print(len(top_medium))

    tops = top_medium + top_short

    ids = [e["id"] for e in tops]
    features = get_features(ids)

    df: pd.DataFrame = pd.read_json(json.dumps(features))
    df = df.drop(["analysis_url", "duration_ms", "id", "time_signature", "track_href",
                  "type", "uri"], axis=1)
    print(df.head())

    clusters = get_clusters(df)
    print(clusters)

    data_in_cluster = [[], [], [], [], []]
    for i in range(len(clusters)):
        data_in_cluster[clusters[i]].append(df.ix[i])

    # todo: PLOTTING!

    to_pred = get_data_from_track_id(["7tpJvC1WpUPJ6sD2pQqHpb"])

    for data in data_in_cluster:
        x = isolation_forest(pd.DataFrame(data), to_pred)
        if x[0] == 1:
            s = "inliner"
        else:
            s = "outlier"
        print("Cluster[{}]: {}".format(data_in_cluster.index(data), s))


def isolation_forest(df_original: pd.DataFrame, df_test: list):
    clf = IsolationForest(behaviour="new", random_state=13, contamination=0.01)
    clf.fit(df_original)
    is_outlier = clf.predict(list(df_test))
    return is_outlier


def get_clusters(df: pd.DataFrame) -> list:
    clf = KMeans(n_clusters=5).fit(df).labels_
    return clf


if __name__ == '__main__':
    # main()
    main_pandas()
