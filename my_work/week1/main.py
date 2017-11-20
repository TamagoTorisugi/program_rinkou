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

    def __init__(self, scale, note):  # 引数は音名とx分音符のx
        self.scale = scale
        self.length = 4.0 / note


class Chord:  # 和音

    wave = 0

    def __init__(self, tone_list):  # 引数は単音のリスト
        for tone in tone_list:
            step = (
                2 * math.pi) * NOTE_FREQ[tone.scale] / 44100  # 2πf*(1/rate)
            self.wave += np.sin(
                step * np.arange(tone.length * (60 / BPM) * RATE))  # sin(2πft)


class Tuplet:  # 連符

    wave = []

    def __init__(self, chord_lst_lst):  # 引数は和音のリストのリスト
        for chord_lst in chord_lst_lst:
            len_sum = 0
            for chord in chord_lst:
                for i in range(len(chord.wave)):
                    try:
                        self.wave[i + len_sum] += chord.wave[i]
                    except IndexError:
                        self.wave.append(chord.wave[i])
                len_sum += len(chord.wave)


def main():
    # pyaudioのストリームを開く
    # streamへ波形を書き込みすると音が出る
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32, channels=CHANNEL_NUM, rate=RATE,
                     output=True)

    wave = []
    wave.append(Chord([Tone("d5", 4), Tone("b4", 4)]).wave)
    wave.append(Chord([Tone("g5", 2), Tone("b4", 2)]).wave)
    wave.append(
        Tuplet([[Chord([Tone("b5", 8)]),
                 Chord([Tone("g5", 8)])], [Chord([Tone("d5", 4)])]]).wave)
    wave.append(Chord([Tone("b5", 2), Tone("d5", 2)]).wave)
    wave.append(Chord([Tone("a5", 4), Tone("c5", 4)]).wave)
    wave.append(Chord([Tone("g5", 2), Tone("b4", 2)]).wave)
    wave.append(Chord([Tone("e5", 4), Tone("c5", 4)]).wave)
    wave.append(Chord([Tone("d5", 2), Tone("b4", 2)]).wave)
    # 全部のsin波をつなげる
    wave = np.concatenate(wave, axis=0)
    wave *= VOLUME

    # 鳴らす
    # pyaudioでは波形を量子化ビット数32ビット，
    # 16進数表示でstreamに書き込むことで音を鳴らせる
    stream.write(wave.astype(np.float32).tostring())


if __name__ == '__main__':
    main()
