# Database
from Metamusic import database
import multiprocessing
import os
import traceback
import sys
from Metamusic import decoder
from Metamusic import fingerprint

from Metamusic.recognize import FileRecognizer, MicrophoneRecognizer
import binascii
from typing import Union, Iterator, Optional


class MetaMusic():

    SONG_ID = "song_id"
    SONG_NAME = 'song_name'
    CONFIDENCE = 'confidence'
    MATCH_TIME = 'match_time'
    OFFSET = 'offset'
    OFFSET_SECS = 'offset_seconds'

    def __init__(self, limit: int)->None:
        database.delete_unfingerprinted_songs()
        self.limit = limit
        self.get_fingerprinted_songs()

    def get_fingerprinted_songs(self):
        # get songs previously indexed
        self.songs = database.get_songs()
        self.songhashes_set = set()  # to know which ones we've computed before
        for song in self.songs:
            self.songhashes_set.add(binascii.hexlify(
                song.file_sha1).decode('utf-8'))

    def fingerprint_directory(self, path: str, nprocesses: int=None)->None:

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

        worker_input = zip(filenames_to_fingerprint, [
                           self.limit] * len(filenames_to_fingerprint), range(len(hashes_sha1)))
        pool = multiprocessing.Pool(nprocesses)

        iterator = pool.imap_unordered(_fingerprint_worker, worker_input)

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
                sid = database.insert_song(file_hash=hashes_sha1[num],
                                           song_name=song_name)
                database.insert_hashes(sid, song_hashes)

                database.set_fingerprinted_flag(sid)
        pool.close()
        pool.join()

    def fingerprint_file(self, filepath: str)->None:
        songname = decoder.path_to_songname(filepath)
        file_hash = decoder.unique_hash(filepath)
        print(type(file_hash))
        # don't refingerprint already fingerprinted files
        if file_hash in self.songhashes_set:
            print("{} already fingerprinted, continuing...".format(songname))
        else:
            song_name, hashes, _ = _fingerprint_worker(
                (filepath, self.limit, '_'))
            sid = database.insert_song(file_hash=file_hash,
                                       song_name=song_name)
            database.insert_hashes(sid, hashes)

            database.set_fingerprinted_flag(sid)

    def recognize(self, recognizer: Union[FileRecognizer, MicrophoneRecognizer], *options, **kwoptions)->dict:
        return recognizer.recognize(*options, **kwoptions)

    def find_matches(self, samples: list, Fs: int =fingerprint.DEFAULT_FS)->Iterator[tuple]:
        hashes: Iterator = fingerprint.fingerprint(samples, Fs=Fs)
        return database.return_matches(hashes)

    def align_matches(self, matches: list)->Optional[dict]:
        """
            Finds hash matches that align in time with other matches and finds
            consensus about which hashes are "true" signal from the audio.
            Returns a dictionary with match information.
        """
        # align by diffs
        diff_counter: dict = {}
        largest = 0
        largest_count = 0
        song_id = -1
        for sid, diff in matches:

            if diff not in diff_counter:
                diff_counter[diff] = {}
            if sid not in diff_counter[diff]:
                diff_counter[diff][sid] = 0
            diff_counter[diff][sid] += 1

            if diff_counter[diff][sid] > largest_count:
                largest = diff
                largest_count = diff_counter[diff][sid]
                song_id = sid

        # extract idenfication
        song = database.get_song_by_id(song_id)
        if song:
            songname = song.song_name
        else:
            return None

        # return match info
        nseconds = round(
            float(largest) / fingerprint.DEFAULT_FS *
            fingerprint.DEFAULT_WINDOW_SIZE * fingerprint.DEFAULT_OVERLAP_RATIO,
            5
        )
        song = {
            'song_id': song_id,
            'song_name': songname,
            MetaMusic.CONFIDENCE: largest_count,
            MetaMusic.OFFSET: int(largest),
            'offset_seconds': nseconds,
            'file_sha1': binascii.hexlify(song.file_sha1).decode('utf-8'),
        }
        return song


def _fingerprint_worker(filename: tuple)->tuple:
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
    result: set = set()
    channel_amount = len(channels)

    for channeln, channel in enumerate(channels):
        # TODO: Remove prints or change them into optional logging.
        print("Fingerprinting channel %d/%d for %s" % (channeln + 1,
                                                       channel_amount,
                                                       filename))
        hashes = fingerprint.fingerprint(channel, Fs=Fs)

        print("Finished channel %d/%d for %s" % (channeln + 1, channel_amount,
                                                 filename))
        result |= set(hashes)
        print(len(result))
    return song_name, result, num
