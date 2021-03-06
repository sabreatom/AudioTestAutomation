import enum
import math
import threading
import numpy as np

class WaveFormType(enum.Enum):
    Sine = 0
    Pulse = 1
    Triangle = 2
    Saw = 3
    SineSweep = 4
    WhiteNoise = 5

class WaveFormGenerator:
    def __init__(self, waveFormType, frequency, sample_rate, amplitude = 1.0, generateSamplesDoneCallback = None):
        self.freq_lock = threading.Lock()

        self.amplitude = amplitude
        self.current_angle = 0.0
        self.sample_rate = sample_rate

        self.setWaveFormType(waveFormType)

        self.setFrequency(frequency)

        self.generateSamplesDoneCallback = generateSamplesDoneCallback

    def generateSamplesCallback(self, frame_length):
        if self.waveFormType == WaveFormType.Sine:
            data = self.generateSineWave(frame_length)
        elif self.waveFormType == WaveFormType.SineSweep:
            data = self.generateSineSweep(frame_length)
        elif self.waveFormType == WaveFormType.WhiteNoise:
            data = self.generateWhiteNoise(frame_length)

        if self.generateSamplesDoneCallback is not None:
            period_generated = (frame_length * self.angle_step) / (2 * math.pi)
            self.generateSamplesDoneCallback(period_generated)

        return data

    def setFrequency(self, frequency):
        self.freq_lock.acquire()
        self.frequency = frequency
        self.angle_step = 2 * math.pi * self.frequency / self.sample_rate
        self.freq_lock.release()
        if self.waveFormType == WaveFormType.SineSweep:
            self.createSweepWaveTable()
        self.sweep_index = 0

    def getFrequency(self):
        return self.frequency

    def setAmplitude(self, amplitude):
        self.amplitude = amplitude

    def getAmplitude(self):
        return self.amplitude

    def setWaveFormType(self, wfr_type):
        if wfr_type in WaveFormType:
            self.waveFormType = wfr_type
        else:
            raise ValueError("Undefined waveform type, see WaveFormType class")

    def getWaveFormType(self):
        return self.waveFormType

    def generateSineWave(self, frame_length):
        self.freq_lock.acquire()
        self.angle_step = 2 * math.pi * self.frequency / self.sample_rate
        self.freq_lock.release()
        data_float = []
        for i in range(frame_length):
            self.current_angle = self.current_angle + self.angle_step
            data_float.append(self.amplitude * math.sin(self.current_angle))

        return data_float

    def createSweepWaveTable(self):
        self.sweep_wave_table = []
        if self.frequency > 150:
            freq_range = range(50, 100, self.frequency)
        else:
            freq_range = [50, 150]

        current_angle = 0
        for i in range(len(freq_range)):
            angle_step = 2 * math.pi * freq_range[i] / self.sample_rate

            while current_angle < 2 * math.pi * (i + 1):
                self.sweep_wave_table.append(self.amplitude * math.sin(current_angle))
                current_angle = current_angle + angle_step

    def generateSineSweep(self, frame_length):
        if self.sweep_index + frame_length > len(self.sweep_wave_table):
            data_float = self.sweep_wave_table[self.sweep_index:len(self.sweep_wave_table)]
            remaining_samples = frame_length - (len(self.sweep_wave_table) - self.sweep_index)
            data_float.append(self.sweep_wave_table[0:remaining_samples])
            self.sweep_index = remaining_samples
        else:
            data_float = self.sweep_wave_table[self.sweep_index:self.sweep_index + frame_length]
            self.sweep_index += frame_length

        return data_float

    def generateWhiteNoise(self, frame_length):
        data_float = np.random.normal(0.0, 1.0, size=frame_length)
        return data_float