from asyncio.windows_events import NULL
import numpy as np
from scipy.fftpack import fft
import math

class DutOutputAnalyzer:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.buffer = b''

    def resetBuffer(self):
        self.buffer = b''

    def storeBuffer(self, data):
        self.buffer += data

    def convertFrequencyToHarmonic(self, frequency, fft_window_length):
        #n0 = f0 * N / fs
        harmonic = frequency * fft_window_length // self.sample_rate
        return harmonic

    def convertHarmonicToFrequency(self, harmonic, fft_window_length):
        #f0 = fs * n0 / N
        frequency = harmonic * self.sample_rate / fft_window_length
        return frequency

    def calculateSpectrum(self):
        result = {}
        data = np.frombuffer(self.buffer, dtype=np.float32)
        y_f = fft(data)
        y_f = np.abs(y_f)
        result['fft'] = y_f[0:(y_f.size // 2)]
        result['f_step'] = self.convertHarmonicToFrequency(1, y_f.size)
        return result
