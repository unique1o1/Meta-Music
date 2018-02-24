import os
import requests
from model import fetcher_database
import eyed3
import asyncio
from bs4 import BeautifulSoup
import threading
import time
import glob
data = {}


async def main(song_name):
    base_url = "http://api.genius.com"
    url = 'https://itunes.apple.com/search'
    headers = {
        'Authorization': 'Bearer dp7sB4-Li2skNwHMdBuXz2yQYKm2moTTW7aVLI1yLBxVnB479rf3HFDJbB9hoDe0'}
    search_url = base_url + "/search"
    data = {'q': song_name}

    loop = asyncio.get_event_loop()

    itunes = loop.run_in_executor(None, lambda: requests.get(url, params={
        "term": song_name, "media": "music", "entity": "song", "limit": 1}).json())

    genius = loop.run_in_executor(None, lambda: requests.get(
        search_url, params=data, headers=headers).json())
    response1 = await itunes
    response2 = await genius
    return [response1, response2]


def sync_data(image_url, lyrics_url, root, i):

    page = requests.get(lyrics_url)

    html = BeautifulSoup(page.text, "html.parser")
    lyrics_ = html.find("div", class_="lyrics").get_text()

    song_path = os.path.join(root, i)
    audiofile = eyed3.load(song_path)
    eyed3.log.setLevel("ERROR")
    audiofile.tag.artist = data["artistName"]
    audiofile.tag.album = data["collectionName"]
    audiofile.tag.album_artist = data["artistName"]
    audiofile.tag.title = data["trackName"]
    audiofile.tag.track_num = data["trackNumber"]
    audiofile.tag.release_date = data["releaseDate"][0:4]

    audiofile.tag.genre = data["primaryGenreName"]
    img = requests.get(image_url).content

    audiofile.tag.images.set(3, img, "image/jpeg")

    audiofile.tag.lyrics.set(lyrics_)
    audiofile.tag.save()


def process_init(path, app, db):
    song_no = 0
    isFile = False
    if os.path.isfile(path):
        isFile = True
    with app.app_context():
        db.create_all()
        print(os.path.dirname(path))
        for root, dirs, files in os.walk(os.path.dirname(path) if isFile else path):

            for i in files:
                if i != os.path.basename(path) and isFile:
                    print('asdfasdfasdf')

                    continue

                if i.endswith('.mp3'):

                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    datas = loop.run_until_complete(main(os.path.splitext(
                        i)[0]))
                    try:
                        global data
                        data = datas[0]['results'][0]
                        genius_data = datas[1]["response"]["hits"][0]["result"]
                        image_url = genius_data['song_art_image_thumbnail_url']
                    except IndexError:
                        print("Data related to {} was not found".format(i))
                        continue
                    lyrics_url = genius_data['url']
                    releasedate = data["releaseDate"][0:4]
                    try:

                        fetched_data = fetcher_database(
                            trackname=data["trackName"], uid=song_no, tracknumber=data["trackNumber"], image_url=image_url, artistname=data["artistName"], albumname=data["collectionName"], releasedate=releasedate, genre=data["primaryGenreName"], status=True)
                        db.session.add(fetched_data)
                        db.session.commit()
                    except Exception:
                        fetched_data = fetcher_database(
                            uid=song_no, status=False)
                        db.session.add(fetched_data)
                        db.session.commit()
                        print("Already in database")
                        continue
                    song_no += 1
                    t = threading.Thread(target=sync_data, args=(
                        image_url, lyrics_url, root, i))
                    t.daemon = True
                    t.start()
            time.sleep(3)
            if isFile:
                break
        time.sleep(1)
        db.session.query(fetcher_database).delete()
        db.session.commit()
