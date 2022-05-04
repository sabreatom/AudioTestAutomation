import pyaudio
import time
import struct

class AudioInterface:
    def __stream_callback__(self, in_data, frame_count, time_info, status):
        #process input:
        if self.input_callback is not None:
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

        self.running = False

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

    def start(self):
        self.running = True
        self.stream.start_stream()

    def stop(self):
        self.running = False
        self.stream.stop_stream()

    def isRunning(self):
        return self.running
