import os
import requests
from model import fetcher_database


def process_init(path, app, db):

    song_no = 0
    url = 'https://itunes.apple.com/search'
    with app.app_context():
        for root, dirs, files in os.walk(path):
            for i in files:
                if i.endswith('.mp3'):
                    data = requests.get(url, params={"term": os.path.splitext(
                        i)[0], "media": "music", "entity": "song", "limit": 1}).json()

                    data = data['results'][0]

                    fetched_data = fetcher_database(
                        trackname=data["trackName"], uid=song_no, tracknumber=data["trackNumber"], image_url=data["artworkUrl100"], artistname=data["artistName"], albumname=data["collectionName"], releasedate=data["releaseDate"], genre=data["primaryGenreName"])
                    db.session.add(fetched_data)
                    db.session.commit()
                    song_no += 1
            if False:
                db.session.query(fetcher_database).delete()
                db.session.commit()
