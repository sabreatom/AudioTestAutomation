from asyncio.windows_events import NULL
import numpy as np
import math
import src.WaveFormGenerator as wfg
import src.AudioInterface as ai
import src.DutOutputAnalyzer as doa

class AfrTestManager:
    AVERAGE_NUM = 5

    def __init__(self, sample_rate, test_frequencies = NULL):
        self.waveform_generator = wfg.WaveFormGenerator(wfg.WaveFormType.Sine, 50, sample_rate)
        self.output_analyzer = doa.DutOutputAnalyzer(sample_rate, self.callbackMeasurementDone)
        self.audio_interface = ai.AudioInterface(sample_rate, self.output_analyzer.processDutData, self.waveform_generator.generateSamplesCallback)
        self.test_frequencies = test_frequencies
        self.current_freq = 0
        self.isRunning = False
        self.test_result = []
        self.iteration = 0

    def setTestFrequencies(self, test_frequencies):
        self.test_frequencies = test_frequencies

    def runTestIteration(self):
        #test frequencies array not initialized:
        if (self.test_frequencies == NULL):
            print('[ERROR] Test frequencies array not initialized')
            return NULL

        self.current_freq = 0
        self.waveform_generator.setFrequency(self.test_frequencies[self.current_freq])
        self.current_freq += 1
        self.audio_interface.start()
        self.isRunning = True
        
        while self.isRunning == True:
            pass

    def callbackMeasurementDone(self, result):
        if self.iteration < self.AVERAGE_NUM:
            self.iteration += 1
        else:
            self.iteration = 0

            if self.current_freq < len(self.test_frequencies):
                self.waveform_generator.setFrequency(self.test_frequencies[self.current_freq])
                self.current_freq += 1
            else:
                self.current_freq = 0
                self.isRunning = False

        print('-------------------------------')
        print('[INFO] Max frequency: {}, amplitude: {}'.format(result['max_frequency'], result['max_frequency_amplitude']))
        print('[INFO] THD: {}'.format(result['thd']))
        print('-------------------------------')