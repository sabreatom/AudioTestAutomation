import src.WaveFormGenerator as wfg
import src.AudioInterface as ai
import src.DutOutputAnalyzer as doa

import pytest
import time

def test_afr():
    def measureEndCallback(tone, amplitude, thd):
        print("Callback: Tone value: {}, THD: {}, amplitude: {}".format(tone, thd, amplitude))
        audioInterface.stop()

    testInProgress = True
    waveformGnerator = wfg.WaveFormGenerator(wfg.WaveFormType.Sine, 500, 44100, 1.0)
    dutOutputAnalyzer = doa.DutOutputAnalyzer(44100, 500, measureEndCallback)
    audioInterface = ai.AudioInterface(44100, dutOutputAnalyzer.processDutData, waveformGnerator.generateSamplesCallback)
    audioInterface.start()

    while audioInterface.isRunning():
        time.sleep(0.1)

    assert True

