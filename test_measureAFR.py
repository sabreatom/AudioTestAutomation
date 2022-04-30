import AfrTestManager as afr_tm

import pytest
import time

import matplotlib.pyplot as plt
from datetime import datetime

meas_freq = range(1000, 10000, 500)

def test_afr():
    afr_tm_inst = afr_tm.AfrTestManager(44100, meas_freq)
    afr = afr_tm_inst.runTestIteration()

    x = []
    y = []
    for i in sorted(afr):
        x.append(i)
        y.append(afr[i])

    plt.plot(x, y)
    
    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
    plt.savefig('afr_test{}.png'.format(date_time))