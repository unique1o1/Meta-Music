import os
import numpy as np
from pydub import AudioSegment
from hashlib import sha1
from typing import Tuple, Optional


def unique_hash(filepath: str, blocksize: int=80)->str:
    """ Small function to generate a hash to uniquely generate a file.
    Default blocksize is `500`
    """
    s = sha1()
    with open(filepath, "rb") as f:
        buf = f.read(blocksize)
        s.update(buf)
    return s.hexdigest()


def read(filename: str, limit: Optional[int]=None) -> Tuple[list, int]:
    """
    Reads any file supported by pydub (ffmpeg) and returns the data contained
    within.
    returns: (channels, samplerate)
    """

    audiofile = AudioSegment.from_file(filename)

    if limit:
        audiofile = audiofile[:limit * 1000]

    data = np.fromstring(audiofile._data, np.int16)

    channels = [data[chn::audiofile.channels] for chn in range(audiofile.channels)]
    fs = audiofile.frame_rate

    return channels, fs


def path_to_songname(path: str)->str:
    """
    Extracts song name from a filepath. Used to identify which songs
    have already been fingerprinted on disk.
    """
    return os.path.splitext(os.path.basename(path))[0]
