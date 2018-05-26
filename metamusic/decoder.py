import os
import fnmatch
import numpy as np
from pydub import AudioSegment
from pydub.utils import audioop
from hashlib import sha1


def unique_hash(filepath, blocksize=500):
    """ Small function to generate a hash to uniquely generate
    a file. 
    """
    if os.path.abspath(filepath).endswith('.mp3'):
        s = sha1()
        with open(filepath, "rb") as f:
            buf = f.read(blocksize)
            s.update(buf)
        return s.hexdigest().upper()


def read(filename, limit=None, num):
    """
    Reads any file supported by pydub (ffmpeg) and returns the data contained
    within. If file reading fails due to input being a 24-bit wav file,
    wavio is used as a backup.

    Can be optionally limited to a certain amount of seconds from the start
    of the file by specifying the `limit` parameter. This is the amount of
    seconds from the start of the file.

    returns: (channels, samplerate)
    """

    audiofile = AudioSegment.from_file(filename)

    if limit:
        audiofile = audiofile[:limit * 1000]

    data = np.fromstring(audiofile._data, np.int16)

    channels = []
    for chn in range(audiofile.channels):
        channels.append(data[chn::audiofile.channels])

    fs = audiofile.frame_rate

    return channels, fs, num


def path_to_songname(path):
    """
    Extracts song name from a filepath. Used to identify which songs
    have already been fingerprinted on disk.
    """
    return os.path.splitext(os.path.basename(path))[0]
