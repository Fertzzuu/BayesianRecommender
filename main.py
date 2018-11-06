import spotipy
from spotipy.util import prompt_for_user_token
from pprint import pprint
from sklearn.naive_bayes import GaussianNB
import numpy as np
import requests
from keras.models import Sequential
from keras.layers import Dense, Activation


CLIENT_ID = "1f6ebe9f1c8e4478a3ed3a6a3b071859"
CLIENT_SECRET = "89efae6388b8468baac49203496a77f6"
REDIRECT_URI = "http://localhost/"
sp: spotipy.Spotify = None
head = None


def get_top_tracks(time_range="medium_term", limit=20, offset=0):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range={}&limit={}&offset={}".format(time_range, limit, offset)
    response = requests.get(url, headers=head).json()
    return response


def get_features(id):
    features = sp.audio_features(id)
    return features

def get_y_from_track_id(id):
    f = get_features(id)
    l = list()
    for fe in f:
        l.append([fe["key"] for key in fe.keys()][:-7])
    return l

def main():
    global sp, head
    scopes = "user-top-read"
    token = prompt_for_user_token("", scopes, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    print(token)
    sp = spotipy.Spotify(token)

    head = {
        'Authorization': 'Bearer ' + token
    }

    top = get_top_tracks(limit=50)["items"]

    data = list()
    x = [e["id"] for e in top]
    features = get_features(x)
    y = np.linspace(1,0,50)
    feature = []
    for f in features:
        data.append([f[key] for key in f.keys()][:-7])

    # data = np.array(data)
    # print(len(data))

    # clf = GaussianNB()
    # clf.fit(data, y)
    #
    # print(clf.predict(get_y_from_track_id(["4RRNgDu0Mas7w3DUZm62Jk"])))

    model = Sequential([
        Dense(32, input_shape=(len(data), len(data[0]))),
        Activation("linear"),
        Dense(20),
        Activation("softmax"),
        Dense(1),
        Activation("softmax")
    ])

    model.compile(optimizer="rmsprop",
                  loss="mean_squared_error",
                  metrics=["accuracy"])

    model.fit(data, y, epochs=10, batch_size=2)
    score = model.evaluate(get_y_from_track_id("0dOng51bwXmdxLNjQCX81i"))
    print(score)


def main_with_requests(token):
    head = {
        'Authorization': 'Bearer ' + token
    }
    url = "https://api.spotify.com/v1/me/top/tracks?limit=100"
    response = requests.get(url, headers=head)
    pprint(len(response.json()["items"]))




if __name__ == '__main__':
    main()
# thats me
