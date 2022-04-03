from asyncio.windows_events import NULL
import numpy as np
from scipy.fftpack import fft
import math

class DutOutputAnalyzer:
    def __init__(self, sample_rate, frequency):
        self.sample_rate = sample_rate
        self.frequency = frequency
        self.frequency_tolerance = 20

        self.buffer_size = sample_rate // 20 #at least one 20 Hz sine wave period fits in buffer
        self.buffer = np.zeros(self.buffer_size)
        self.buffer_sample_count = 0

        self.measurement_done_callback = NULL

        self.last_thd = None

    def setRefFrequency(self, frequency):
        self.frequency = frequency

    def getRefFrequency(self):
        return self.frequency

    def setRefAmplitude(self, amplitude):
        self.ref_amplitude = amplitude

    def getRefAmplitude(self):
        return self.ref_amplitude

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

    def convertFrequencyToHarmonic(self, frequency, fft_window_length):
        #n0 = f0 * N / fs
        harmonic = frequency * fft_window_length // self.sample_rate
        return harmonic

    def convertHarmonicToFrequency(self, harmonic, fft_window_length):
        #f0 = fs * n0 / N
        frequency = harmonic * self.sample_rate // fft_window_length
        return frequency

    def processDutData(self, data):
        if (self.storeBuffer(data)):
            y_f = fft(self.buffer)
            y_f = np.abs(y_f)

            result = {}

            max_harmonic = np.argmax(y_f[:self.buffer_size // 2])
            result['max_frequency_amplitude'] = y_f[max_harmonic]
            result['max_frequency'] = self.convertHarmonicToFrequency(max_harmonic, len(y_f))

            ref_harmonic = self.convertFrequencyToHarmonic(self.frequency, len(y_f))
            harmonic_tolerance = self.convertFrequencyToHarmonic(self.frequency_tolerance, len(y_f))
            ref_harmonic = np.argmax(y_f[ref_harmonic - harmonic_tolerance:ref_harmonic + harmonic_tolerance])
            result['thd'] = self.calculateTHD(ref_harmonic, y_f[:self.buffer_size // 2])
            result['ref_frequency_amplitude'] = y_f[ref_harmonic]
            result['ref_frequency'] = self.convertHarmonicToFrequency(ref_harmonic, len(y_f))
            result['fft'] = y_f

            self.measurement_done_callback(result)

    def calculateTHD(self, fundamentalHarmonic, arr):
        sum = 0
        for i in range(len(arr)):
            if i != fundamentalHarmonic:
                sum += arr[i] ** 2

        return math.sqrt(sum) / arr[fundamentalHarmonic]

    def normalizeArray(self,arr):
        max_val = max(arr)
        ret = np.zeros(len(arr))
        for i in range(len(arr)):
            ret[i] = arr[i] / max_val
        return ret

