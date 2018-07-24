
import Metamusic.decoder as decoder
import numpy as np
import time


class BaseRecognizer(object):
    def __init__(self, metaMusic):
        self.metaMusic = metaMusic
        self.Fs = 44100

    def _recognize(self, data):
        matches = []
        for d in data:
            f = time.time()
            matches.extend(self.metaMusic.find_matches(d, Fs=self.Fs))
            print(time.time()-f)
        return self.metaMusic.align_matches(matches)

    def recognize(self):
        pass  # base class does nothing


class FileRecognizer(BaseRecognizer):
    def __init__(self, metaMusic):
        super().__init__(metaMusic)

    def recognize_file(self, filename):
        frames, self.Fs = decoder.read(
            filename, self.metaMusic.limit)

        t = time.time()
        match = self._recognize(frames)
        t = time.time() - t

        if match:
            match['match_time'] = t

        return match
