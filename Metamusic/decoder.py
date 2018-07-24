import os
import fnmatch
import numpy as np
from pydub import AudioSegment
from pydub.utils import audioop
from hashlib import sha1


def unique_hash(filepath, blocksize=80):
    """ Small function to generate a hash to uniquely generate
    a file.
    Default blocksize is `500`
    """
    s = sha1()
    with open(filepath, "rb") as f:
        buf = f.read(blocksize)
        s.update(buf)
    return s.hexdigest()


def read(filename, limit=None):
    """
    Reads any file supported by pydub (ffmpeg) and returns the data contained
    within.
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

    return channels, fs


def path_to_songname(path):
    """
    Extracts song name from a filepath. Used to identify which songs
    have already been fingerprinted on disk.
    """
    return os.path.splitext(os.path.basename(path))[0]
