import src.WaveFormGenerator as wfg
import src.AudioInterface as ai
import time
import argparse

def playTone(frequency, duration):
    waveform_generator = wfg.WaveFormGenerator(wfg.WaveFormType.Sine, frequency, 44100)
    audio_interface = ai.AudioInterface(44100, None, waveform_generator.generateSamplesCallback)

    audio_interface.start()
    time.sleep(duration)
    audio_interface.stop()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--frequency', type=int, required=True)
    parser.add_argument('-d', '--duration', type=int, required=True)

    args = parser.parse_args()

    playTone(args.frequency, args.duration)

if __name__ == "__main__":
    main()