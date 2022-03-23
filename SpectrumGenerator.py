import numpy as np
from scipy.fftpack import fft
import math

class SpectrumGenerator:
    def __init__(self, sample_rate, spectrum_ready_callback):
        self.sample_rate = sample_rate
        self.spectrum_ready_callback = spectrum_ready_callback

        self.buffer_size = sample_rate // 20 #at least one 20 Hz sine wave period fits in buffer
        self.buffer = np.zeros(self.buffer_size)
        self.buffer_sample_count = 0

    def storeBuffer(self, data):
        audio_data = np.frombuffer(data, dtype=np.float32)
        #print("Sample count: {}, audio data len: {}".format(self.buffer_sample_count, len(audio_data)))

        if (self.buffer_sample_count == 0):
            self.buffer = audio_data
        else:
            self.buffer = np.append(self.buffer, audio_data)

        if ((self.buffer_sample_count + len(audio_data)) >= self.buffer_size):
            self.buffer_sample_count = 0
            return True
        else:
            self.buffer_sample_count += len(audio_data)
            return False

    def processDutData(self, data):
        if (self.storeBuffer(data)):
            spectrum = fft(self.buffer)
            spectrum = np.abs(spectrum)

            self.spectrum_ready_callback(spectrum)