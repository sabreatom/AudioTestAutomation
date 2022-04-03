from asyncio.windows_events import NULL
import numpy as np
import math
import src.WaveFormGenerator as wfg
import src.AudioInterface as ai
import src.DutOutputAnalyzer as doa


class AfrTestManager:
    def __init__(self, audio_interface, waveform_generator, output_analyzer, test_frequencies = NULL):
        self.audio_interface = audio_interface
        self.waveform_generator = waveform_generator 
        self.output_analyzer = output_analyzer
        self.test_frequencies = test_frequencies
        self.current_freq = 0
        self.isRunning = False
        self.test_result = []

    def setTestFrequencies(self, test_frequencies):
        self.test_frequencies = test_frequencies

    def runTestIteration(self):
        #test frequencies array not initialized:
        if (self.test_frequencies == NULL):
            print('[ERROR] Test frequencies array not initialized')
            return NULL

        self.current_freq = 0
        self.audio_interface.start()
        self.isRunning = True
        
        while self.isRunning == True:
            pass

    def callbackMeasurementDone(self, result):
        if self.current_freq == 0:
            self.waveform_generator.setFrequency(self.test_frequencies[self.current_freq])
            self.output_analyzer.setRefFrequency(self.test_frequencies[self.current_freq])
            self.current_freq += 1
        else:
            if self.current_freq < len(self.test_frequencies):
                self.waveform_generator.setFrequency(self.test_frequencies[self.current_freq])
                self.output_analyzer.setRefFrequency(self.test_frequencies[self.current_freq])
                self.current_freq += 1
            else:
                self.current_freq = 0
                self.isRunning = False

            print('-------------------------------')
            print('[INFO] Max frequency: {}, amplitude: {}'.format(result['max_frequency'], result['max_frequency_amplitude']))
            print('[INFO] Reference frequency: {}, amplitude: {}'.format(result['ref_frequency'], result['ref_frequency_amplitude']))
            print('[INFO] THD: {}'.format(result['thd']))
            print('-------------------------------')