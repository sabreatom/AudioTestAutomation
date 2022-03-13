import time
import WaveFormGenerator as wfg
import math

import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt

def normalizeArray(arr):
    max_val = max(arr)
    ret = np.zeros(len(arr))
    for i in range(len(arr)):
        ret[i] = arr[i] / max_val
    return ret

def calculateTHD(fundamentalHarmonic, arr):
    sum = 0
    for i in range(len(arr)):
        if i != fundamentalHarmonic:
            sum += arr[i] ** 2

    return math.sqrt(sum) / arr[fundamentalHarmonic]

ANALYZE_WINDOW_LEN = 44100

SINE_FREQ = 50

waveformGnerator = wfg.WaveFormGenerator(wfg.WaveFormType.Sine, SINE_FREQ, 44100, 1.0)

buf = waveformGnerator.generateSamplesCallback(ANALYZE_WINDOW_LEN)

# for i in range(len(buf)):
#     if buf[i] > 0.8:
#         buf[i] = 0.8
#     elif buf[i] < -0.8:
#         buf[i] = -0.8
#plt.plot(buf)

y_f = fft(buf)

y_f = np.abs(y_f)

thd = calculateTHD(SINE_FREQ, y_f[:ANALYZE_WINDOW_LEN // 2])
print("THD: " + str(thd))

y_f = normalizeArray(y_f)
#plt.plot(y_f[:ANALYZE_WINDOW_LEN // 2])
plt.plot(y_f[:500])

plt.show()