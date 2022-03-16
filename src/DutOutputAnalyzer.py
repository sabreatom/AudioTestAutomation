import numpy as np
from scipy.fftpack import fft
import math

class DutOutputAnalyzer:
    def __init__(self, sample_rate, frequency, measurement_done_callback):
        self.sample_rate = sample_rate
        self.frequency = frequency

        self.buffer_size = sample_rate // 20 #at least one 20 Hz sine wave period fits in buffer
        self.buffer = np.zeros(self.buffer_size)
        self.buffer_sample_count = 0

        self.measurement_done_callback = measurement_done_callback

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

    def findTone(self, spectrum, fundamentalHarmonic, threshold):
        #f0 = fs*n0/N
        fft_harmonic = fundamentalHarmonic * len(spectrum) // self.sample_rate
        fft_threshold = threshold * len(spectrum) // self.sample_rate
        return np.argmax(spectrum[fft_harmonic - fft_threshold:fft_harmonic + fft_threshold])

    def processDutData(self, data):
        if (self.storeBuffer(data)):
            y_f = fft(self.buffer)
            y_f = np.abs(y_f)
            tone = self.findTone(y_f, self.frequency, 10)
            thd = self.calculateTHD(tone, y_f[:self.buffer_size // 2])
            amplitude = y_f[tone]
            print("Tone value: {}, THD: {}, amplitude: {}".format(tone, thd, amplitude))

            if (self.last_thd == None):
                self.last_thd = thd
            else:
                if (self.last_thd > thd):
                    self.last_thd = thd
                else:
                    self.last_thd = None
                    self.measurement_done_callback(tone, amplitude, thd)


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

