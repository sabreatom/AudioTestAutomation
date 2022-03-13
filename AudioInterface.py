import pyaudio
import time
import struct
import WaveFormGenerator as wfg
import DutOutputAnalyzer as doa

class AudioInterface:
    def __stream_callback__(self, in_data, frame_count, time_info, status):
        #process input:
        self.input_callback(in_data)

        #process output:
        data_float = self.output_callback(frame_count)

        data = struct.pack("f" * len(data_float), *data_float)
        return (data, pyaudio.paContinue)

    def __init__(self, sample_rate, input_callback, output_callback):
        self.sample_rate = sample_rate
        self.input_callback = input_callback
        self.output_callback = output_callback

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format = pyaudio.paFloat32,
                channels = 1,
                rate = self.sample_rate,
                output = True,
                input=True,
                stream_callback = self.__stream_callback__)

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def getStreamState(self):
        return self.stream.is_active()

    def start(self):
        self.stream.start_stream()

    def stop(self):
        self.stream.stop_stream()


if __name__ == '__main__':
    waveformGnerator = wfg.WaveFormGenerator(wfg.WaveFormType.Sine, 500, 44100, 1.0)
    dutOutputAnalyzer = doa.DutOutputAnalyzer(44100, 500)
    audioInterface = AudioInterface(44100, dutOutputAnalyzer.processDutData, waveformGnerator.generateSamplesCallback)
    audioInterface.start()
    time.sleep(2)
    waveformGnerator.setFrequency(1000)
    time.sleep(1)
    waveformGnerator.setAmplitude(0.5)
    time.sleep(1)
    audioInterface.stop()