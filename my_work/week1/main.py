import math

import numpy as np
import pyaudio

RATE = 44100  # sample rate
CHANNEL_NUM = 1  # チャンネル数 今回はモノラルなので1
NOTE_FREQ = {  # 音の周波数
    "d6": 1174.659,
    "c6": 1046.502,
    "d#5": 622.254,
    "b5": 987.767,
    "a5": 880.000,
    "g5": 783.991,
    "f#5": 739.989,
    "f5": 698.456,
    "e5": 659.255,
    "d5": 587.330,
    "c#5": 554.365,
    "c5": 523.521,
    "b4": 493.883,
    "a4": 440.000,
    "g4": 391.995,
    "rest": 0,
}
BPM = 120
VOLUME = 0.1


class Tone:  # 単音

    def __init__(self, scale, length):  # 引数は音名とx分音符のx
        self.scale = scale
        self.length = length


class Chord:  # 和音

    def __init__(self, tone_tuple_tuple):  # 引数は単音のタプルのタプル
        tones = [
            Tone(tone_tuple[0], tone_tuple[1])
            for tone_tuple in tone_tuple_tuple
        ]
        self.wave = Chord.calculate_wave(tones)

    @staticmethod
    def calculate_wave(tones):
        wave = 0
        for tone in tones:
            step = (
                2 * math.pi) * NOTE_FREQ[tone.scale] / 44100  # 2πf*(1/rate)
            wave += np.sin(step * np.arange(tone.length *
                                            (60 / BPM) * RATE))  # sin(2πft)
        return wave


class Tuplet:  # 連符

    def __init__(self, chord_lst_lst):  # 引数は和音のリストのリスト
        waves = []
        for chord_lst in chord_lst_lst:
            sub_waves = []
            for chord in chord_lst:
                sub_waves.append(chord.wave)
            sub_wave = np.concatenate(sub_waves)
            waves.append(sub_wave)
        self.wave = np.sum(waves, axis=0)


def main():
    # pyaudioのストリームを開く
    # streamへ波形を書き込みすると音が出る
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32, channels=CHANNEL_NUM, rate=RATE,
                     output=True)

    wave = []
    wave.append(Chord((("d5", 1), ("b4", 1))).wave)
    wave.append(Chord((("g5", 2), ("b4", 2))).wave)
    wave.append(
        Tuplet(((Chord((("b5", 8)), ("g5", 8))), (Chord((("d5", 4)))))).wave)
    wave.append(Chord((("b5", 2), ("d5", 2))).wave)
    wave.append(Chord((("a5", 1), ("c5", 1))).wave)
    wave.append(Chord((("g5", 2), ("b4", 2))).wave)
    wave.append(Chord((("e5", 1), ("c5", 1))).wave)
    wave.append(Chord((("d5", 2), ("b4", 2))).wave)
    # 全部のsin波をつなげる
    wave = np.concatenate(wave, axis=0)
    wave *= VOLUME

    # 鳴らす
    # pyaudioでは波形を量子化ビット数32ビット，
    # 16進数表示でstreamに書き込むことで音を鳴らせる
    stream.write(wave.astype(np.float32).tostring())


if __name__ == '__main__':
    main()
