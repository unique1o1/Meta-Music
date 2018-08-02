
import Metamusic.decoder as decoder
import numpy as np
import time

import sounddevice as sd


class BaseRecognizer(object):
    def __init__(self, metaMusic):
        self.metaMusic = metaMusic
        self.Fs = 44100

    def _recognize(self, data):

        matches = []
        for d in data:
            matches.extend(self.metaMusic.find_matches(d, Fs=self.Fs))

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
        # print(len(frames[0]))
        match = self._recognize(frames)
        t = time.time() - t

        if match:
            match['match_time'] = t

        return match

    def recognize(self, filename):
        return self.recognize_file(filename)


class MicrophoneRecognizer(BaseRecognizer):
    default_channels = 2
    default_samplerate = 44100
    default_format = np.int16

    def __init__(self, dejavu):
        super(MicrophoneRecognizer, self).__init__(dejavu)
        sd.default.samplerate = MicrophoneRecognizer.default_samplerate
        sd.default.channels = MicrophoneRecognizer.default_channels
        sd.default.dtype = MicrophoneRecognizer.default_format
        self.data = [[], []]
        self.recorded = False

    def start_recording(self, seconds):
        print(seconds)
        self.myrecording = sd.rec(int(seconds * self.default_samplerate))

    # def process_recording(self):
    #     data = self.stream.read(self.chunksize)
    #     nums = np.fromstring(data, np.int16)
    #     for c in range(self.channels):
    #         self.data[c].extend(nums[c::self.channels])

    def stop_recording(self):
        sd.wait()
        self.recorded = True

    def recognize_recording(self):
        if not self.recorded:
            raise NoRecordingError("Recording was not complete/begun")
        data = self.myrecording.flatten()

        for c in range(self.default_channels):
            self.data[c].extend(data[c::self.default_channels])
        # print(len(self.data[0]))
        return self._recognize(self.data)

    def get_recorded_time(self):
        return len(self.data[0]) / self.rate

    def recognize(self, seconds=10):
        print('starting')
        self.start_recording(seconds)
        # for i in range(0, int(self.samplerate / self.chunksize * seconds)):
        #     self.process_recording()
        self.stop_recording()

        return self.recognize_recording()


class NoRecordingError(Exception):

    pass
