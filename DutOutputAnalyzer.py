import numpy as np
from scipy.fftpack import fft
import math

class DutOutputAnalyzer:
    def __init__(self, sample_rate, frequency, ref_amplitude):
        self.sample_rate = sample_rate
        self.frequency = frequency
        self.ref_amplitude = ref_amplitude

        self.buffer_size = sample_rate // 20 #at least one 20 Hz sine wave period fits in buffer
        self.buffer = np.zeros(self.buffer_size)
        self.buffer_sample_count = 0

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
        return np.argmax(spectrum[fundamentalHarmonic - threshold:fundamentalHarmonic + threshold])

    def processDutData(self, data):
        if (self.storeBuffer(data)):
            y_f = fft(self.buffer)
            y_f = np.abs(y_f)
            tone = self.findTone(y_f[:self.buffer_size // 2], self.frequency, 10)
            thd = self.calculateTHD(tone, y_f[:self.buffer_size // 2])
            print("Tone value: {}, THD: {}".format(tone, thd))


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

