from mutagen.id3 import ID3, TYER
from Metamusic.recognize import FileRecognizer
from Metamusic import MetaMusic
import os
import requests
from model import fetcher_database
import eyed3
import asyncio
from termcolor import colored
from bs4 import BeautifulSoup
import re
import threading
import time


url = 'https://itunes.apple.com/search'
headers = {
    'Authorization': 'Bearer dp7sB4-Li2skNwHMdBuXz2yQYKm2moTTW7aVLI1yLBxVnB479rf3HFDJbB9hoDe0'}
search_url = "http://api.genius.com/search"

meta = MetaMusic(5)
fileRecognizer = FileRecognizer(meta)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def main(song_name):
    global url, headers, search_url
    data = {'q': song_name}

    loop = asyncio.get_event_loop()
    try:
        itunes = loop.run_in_executor(None, lambda: requests.get(url, params={
            "term": song_name, "media": "music", "entity": "song", "limit": 1}).json())

        genius = loop.run_in_executor(None, lambda: requests.get(
            search_url, params=data, headers=headers).json())
        response1 = await itunes
        response2 = await genius
    except Exception:

        print("Error occured when fetching data from servers")
        return 0
    return [response1, response2]


def sync_data(data, image_url, lyrics_url, song_path):
    page = requests.get(lyrics_url)
    html = BeautifulSoup(page.text, "html.parser")
    lyrics_ = html.find("div", class_="lyrics").get_text()

    tags = ID3()
    tags['TYER'] = TYER(encoding=3, text=data["releaseDate"][0:4])  # year
    tags.save(song_path)
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


def process_init(path, app, db, folders, total_songs):
    song_no = 0
    total_managed = 0
    isFile = False
    timeit = time.time()
    if os.path.isfile(path):
        isFile = True
    with app.app_context():
        db.create_all()
        for root in folders:

            for i in os.listdir(root):

                if i != os.path.basename(path) and isFile:

                    continue
                ext = os.path.splitext(i)[1]
                if i.endswith('.mp3'):

                    temp = os.path.splitext(i)[0]

                    i = re.sub(re.escape(ext), '', i)
                    i = re.sub(r'[^\w^,]', ' ', i)
                    i = re.sub(r'[_]', ' ', i)
                    i = re.sub(r'^[0-9]+[ _\-][0-9]*', '', i)
                    i = re.sub(r' \d{2,}', '', i)
                    i = re.sub(r'[^\x00-\x7F]+', '', i).strip()
                    if i != temp:
                        os.rename(os.path.join(root, temp + ext),
                                  os.path.join(root, i + ext))
                        print("{0}{2} renamed to {1}{2}".format(
                            temp, i, ext))

                    datas = loop.run_until_complete(main(i))

                    # check if datas dictionary has required object or not
                    def checkDataStatus(val):

                        data = datas[0]['results'][0]
                        genius_data = datas[1]["response"]["hits"][0]["result"]
                        if val and data['artistName'].lower().strip() != genius_data['primary_artist']['name'].lower().strip():
                            print(data['artistName'].lower().strip(
                            ) + " and " + genius_data['primary_artist']['name'].lower().strip())
                            raise IndexError
                        return data, genius_data
                    if datas == 0:
                        song_no += 1
                        continue
                    try:
                        # argument 1 for checking data without AudioRecognition
                        data, genius_data = checkDataStatus(1)

                    except IndexError:
                        print(colored("Searching Song's fingerprint " +
                                      os.path.join(root, i + ext), "blue"))
                        song = meta.recognize(
                            fileRecognizer, os.path.join(root, i + ext))
                        print(colored('Done', 'blue'))
                        try:
                            if song is None or song['confidence'] < 200:
                                raise IndexError

                            os.rename(os.path.join(root, i + ext),
                                      os.path.join(root, song['song_name'] + ext))
                            i = song['song_name']
                            datas = loop.run_until_complete(
                                main(song['song_name']))

                            # argument 0 for checking data without AudioRecognition
                            data, genius_data = checkDataStatus(0)

                        except IndexError:
                            print(
                                colored("Data related to {} was not found".format(i), 'red'))
                            fetched_data = fetcher_database(
                                uid=song_no, status=False)
                            db.session.add(fetched_data)
                            db.session.commit()
                            song_no += 1
                            continue
                        except Exception as e:
                            print(e)
                            continue

                    image_url = genius_data['song_art_image_thumbnail_url']

                    lyrics_url = genius_data['url']
                    releasedate = data["releaseDate"][0:4]
                    try:

                        fetched_data = fetcher_database(
                            trackname=data["trackName"], uid=song_no, tracknumber=data["trackNumber"], image_url=image_url, artistname=data["artistName"], albumname=data["collectionName"], releasedate=releasedate, genre=data["primaryGenreName"], status=True)
                        db.session.add(fetched_data)
                        db.session.commit()
                        total_managed += 1
                    except Exception:

                        print("Already in database")
                        song_no += 1
                        continue
                    song_no += 1
                    t = threading.Thread(target=sync_data, args=(
                        data, image_url, lyrics_url, os.path.join(root, i + ext)))
                    t.daemon = True
                    t.start()
                    if isFile:
                        break

        time.sleep(4)
        db.session.query(fetcher_database).delete()
        db.session.commit()
        print("{} out of {} songs were managed".format(
            total_managed, total_songs))
        print((time.time() - timeit) - 3)
