# Database
from Metamusic import database
import multiprocessing
import os
import traceback
import sys
from Metamusic import decoder
from Metamusic import fingerprint
from sqlalchemy import func


class MetaMusic():

    SONG_ID = "song_id"
    SONG_NAME = 'song_name'
    CONFIDENCE = 'confidence'
    MATCH_TIME = 'match_time'
    OFFSET = 'offset'
    OFFSET_SECS = 'offset_seconds'

    def __init__(self, limit):
        database.delete_unfingerprinted_songs()
        self.limit = limit
        self.get_fingerprinted_songs()

    def get_fingerprinted_songs(self):
        # get songs previously indexed
        self.songs = database.get_songs()
        self.songhashes_set = set()  # to know which ones we've computed before
        for song in self.songs:
            song_hash = song.file_sha1
            self.songhashes_set.add(song_hash.decode())

    def fingerprint_directory(self, path, nprocesses=None):

        # Try to use the maximum amount of processes if not given.
        try:
            nprocesses = nprocesses or multiprocessing.cpu_count()

        except NotImplementedError:
            nprocesses = 1
        else:
            nprocesses = 1 if nprocesses <= 0 else nprocesses

        pool = multiprocessing.Pool(nprocesses)

        filenames_to_fingerprint = []
        mp3_file = []
        temp_hash = []

        for dirpath, dirnames, files in os.walk(path):
            for i in files:
                if i.endswith('.mp3'):
                    mp3_file.append(os.path.join(dirpath, i))

        hashes_sha1 = pool.map(decoder.unique_hash, mp3_file)
        pool.close()
        pool.join()

        # don't refingerprint already fingerprinted files
        for n, i in enumerate(hashes_sha1):
            if i in self.songhashes_set:
                print("{} already fingerprinted, continuing...".format(
                    os.path.basename(mp3_file[n])))
                temp_hash.append(i)
                continue

            filenames_to_fingerprint.append(mp3_file[n])
        for i in temp_hash:
            hashes_sha1.remove(i)

        mp3_file = None
        temp_hash = None

        # Prepare _fingerprint_worker input
        worker_input = zip(filenames_to_fingerprint, [
                           self.limit] * len(filenames_to_fingerprint), range(len(hashes_sha1)))
        pool = multiprocessing.Pool(nprocesses)

        # Send off our tasks
        iterator = pool.imap_unordered(_fingerprint_worker, worker_input)

        # Loop till we have all of them
        while True:
            try:
                song_name, song_hashes, num = iterator.next()
            except multiprocessing.TimeoutError:
                continue
            except StopIteration:
                break
            except:
                print("Failed fingerprinting")
                # Print traceback because we can't reraise it here
                traceback.print_exc(file=sys.stdout)
            else:

                database.insert_song(file_hash=hashes_sha1[num],
                                     song_name=song_name)
                fingerprint()
                database.set_fingerprinted_flag()
        pool.close()
        pool.join()

    def fingerprint_file(self, filepath):
        songname = decoder.path_to_songname(filepath)
        file_hash = decoder.unique_hash(filepath)
        # don't refingerprint already fingerprinted files
        if file_hash in self.songhashes_set:
            print("{} already fingerprinted, continuing...".format(songname))
        else:
            song_name, hashes, _ = _fingerprint_worker(
                (filepath, self.limit, '_'))
            database.insert_song(file_hash=file_hash,
                                 song_name=song_name)
            database.set_fingerprinted_flag()


def _fingerprint_worker(filename):
    # Pool.imap sends arguments as tuples so we have to unpack
    # them ourself.
    try:
        filename, limit, num = filename
        song_name = None
    except ValueError:
        pass

    songname, extension = os.path.splitext(os.path.basename(filename))
    song_name = song_name or songname
    channels, Fs = decoder.read(filename, limit)
    result = set()
    channel_amount = len(channels)

    for channeln, channel in enumerate(channels):
        # TODO: Remove prints or change them into optional logging.
        print("Fingerprinting channel %d/%d for %s" % (channeln + 1,
                                                       channel_amount,
                                                       filename))
        hashes = fingerprint.fingerprint(channel, Fs=Fs)
        print("Finished channel %d/%d for %s" % (channeln + 1, channel_amount,
                                                 filename))
        result = set(hashes)

    return song_name, result, num
