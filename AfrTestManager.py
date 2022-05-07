from asyncio.windows_events import NULL
import numpy as np
import time
import src.WaveFormGenerator as wfg
import src.AudioInterface as ai
import src.DutOutputAnalyzer as doa

class AfrTestManager:
    FREQ_TEST_LENGTH = 10.0   #periods

    def __init__(self, sample_rate, test_frequencies = NULL):
        self.waveform_generator = wfg.WaveFormGenerator(wfg.WaveFormType.Sine, 50, sample_rate, 1.0, self.generateSamplesDoneCallback)
        self.output_analyzer = doa.DutOutputAnalyzer(sample_rate)
        self.audio_interface = ai.AudioInterface(sample_rate, self.output_analyzer.storeBuffer, self.waveform_generator.generateSamplesCallback)
        self.test_frequencies = test_frequencies
        self.current_freq = 0
        self.isRunning = False
        self.test_result = {}
        
        self.freq_period_count = 0.0

    def setTestFrequencies(self, test_frequencies):
        self.test_frequencies = test_frequencies

    def runTestIteration(self):
        #test frequencies array not initialized:
        if (self.test_frequencies == NULL):
            print('[ERROR] Test frequencies array not initialized')
            return NULL

        self.test_result = {}
        self.current_freq = 0
        self.waveform_generator.setFrequency(self.test_frequencies[self.current_freq])
        self.current_freq += 1
        self.audio_interface.start()
        self.isRunning = True
        
        while self.isRunning == True:
            pass
        
        self.audio_interface.stop()
        time.sleep(0.5) #wait for remaining frames to be captured
        return self.output_analyzer.calculateSpectrum()

    def generateSamplesDoneCallback(self, period_generated):
        self.freq_period_count += period_generated
        if self.freq_period_count >= self.FREQ_TEST_LENGTH:
            self.freq_period_count = 0.0

            if self.current_freq < len(self.test_frequencies):
                self.waveform_generator.setFrequency(self.test_frequencies[self.current_freq])
                self.current_freq += 1
            else:
                self.current_freq = 0
                self.isRunning = False