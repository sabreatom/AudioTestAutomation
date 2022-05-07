import AfrTestManager as afr_tm

import pytest
import time

import matplotlib.pyplot as plt
from datetime import datetime

import math

meas_freq = range(100, 5000, 100)

def test_afr():
    afr_tm_inst = afr_tm.AfrTestManager(44100, meas_freq)
    afr = afr_tm_inst.runTestIteration()

    print("Harmonic step value is: {}".format(afr['f_step']))

    plt.plot(afr['fft'][0:math.ceil(max(meas_freq) / afr['f_step'])])
    
    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
    plt.savefig('afr_test{}.png'.format(date_time))