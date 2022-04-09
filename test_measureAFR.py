import AfrTestManager as afr_tm

import pytest
import time

meas_freq = range(50, 15000, 1000)

def test_afr():
    afr_tm_inst = afr_tm.AfrTestManager(44100, meas_freq)
    afr_tm_inst.runTestIteration()