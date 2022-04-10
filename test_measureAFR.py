import AfrTestManager as afr_tm

import pytest
import time

import matplotlib.pyplot as plt

meas_freq = range(1000, 10000, 1000)

def test_afr():
    afr_tm_inst = afr_tm.AfrTestManager(44100, meas_freq)
    afr = afr_tm_inst.runTestIteration()

    x = []
    y = []
    for i in sorted(afr):
        x.append(i)
        y.append(afr[i]['amplitude'])

    plt.plot(x, y)
    plt.show()