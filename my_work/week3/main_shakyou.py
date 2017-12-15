import math
import numpy as np
import pyaudio

class TonePlayer(object):
    def __init__(self,length=1,rate=44100):
        self.length = length
        self.rate  = rate

    def generate_wave(self,freq_obj):
        step = (2 * math.pi) * freq_obj.freq / self.rate
        wave = np.sin(step*np.arange(int(self.length * self.rate)))
        return wave

    def play(self,freq_obj):
        wave = self.generate_wave(freq_obj)
        pa = pyaudio.PyAudio()
        stream = pa.open(format = pyaudio.paFloat32, channels = 1,  rate = self.rate, output = True)
        stream.write(wave.astype(np.float32).tostring())

class Frequency(object):
    def __init__(self,scale):
        key, octave = scale[0], int(scale[1])
        scale_name = 'cxdxefxgxaxb'
        key_index = scale_name.find(key)
        factor = key_index - 9
        self.freq = 55 * 2 **((octave - 1) + factor /12)

freq_c4 = Frequency("c4")
player = TonePlayer()
player.play(freq_c4)
player.play(Frequency("d4"))
player.length = 3
player.play(Frequency("e4"))
