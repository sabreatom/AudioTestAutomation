import enum
import math

class WaveFormType(enum.Enum):
    Sine = 0
    Pulse = 1
    Triangle = 2
    Saw = 3

class WaveFormGenerator:
    def __init__(self, waveFormType, frequency, sample_rate, amplitude = 1.0):
        if waveFormType in WaveFormType:
            self.waveFormType = waveFormType
        else:
            raise ValueError("Undefined waveform type, see WaveFormType class")

        self.frequency = frequency
        self.amplitude = amplitude
        self.current_angle = 0.0
        self.sample_rate = sample_rate

    def generateSamplesCallback(self, frame_length):
        angle_step = 2 * math.pi * self.frequency / self.sample_rate
        data_float = []
        for i in range(frame_length):
            self.current_angle = self.current_angle + angle_step
            data_float.append(self.amplitude * math.sin(self.current_angle))

        return data_float

    def setFrequency(self, frequency):
        self.frequency = frequency

    def getFrequency(self):
        return self.frequency

    def setAmplitude(self, amplitude):
        self.amplitude = amplitude

    def getAmplitude(self):
        return self.amplitude