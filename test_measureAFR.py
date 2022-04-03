import src.WaveFormGenerator as wfg
import src.AudioInterface as ai
import src.DutOutputAnalyzer as doa
import AfrTestManager as afr_tm

import pytest
import time

meas_freq = [500, 1000, 1500, 2000, 4000, 10000]

def test_afr():
    wfg_inst = wfg.WaveFormGenerator(wfg.WaveFormType.Sine, 50, 44100)
    doa_inst = doa.DutOutputAnalyzer(44100, 50)
    ai_inst = ai.AudioInterface(44100, doa_inst.processDutData, wfg_inst.generateSamplesCallback)
    afr_tm_inst = afr_tm.AfrTestManager(ai_inst, wfg_inst, doa_inst, meas_freq)
    doa_inst.measurement_done_callback = afr_tm_inst.callbackMeasurementDone
    afr_tm_inst.runTestIteration()