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
    "b4": 493.883,
    "g4": 391.995,
}
BPM = 120
VOLUME = 0.1


def tone(scale, length):
    '''generate tone wave

    周波数と長さからsin波を作成する関数
    scale  : frequency [Hz]
    length : length (quater note is 1)
    '''

    step = (2 * math.pi) * NOTE_FREQ[scale] / 44100  # 2πf*(1/rate)
    wave = np.sin(step * np.arange(length * (60 / BPM) * RATE))  # sin(2πft)
    return wave


def rest(length):  # 休符
    wave = np.zeros(int(length * (60 / BPM) * RATE))
    return wave


def main():
    # pyaudioのストリームを開く
    # streamへ波形を書き込みすると音が出る
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32, channels=CHANNEL_NUM, rate=RATE,
                     output=True)

    # 波形を作成する（星に願いを）
    wave = []
    wave.append(tone("g4", 1))
    wave.append(tone("g5", 1))
    wave.append(tone("f5", 1))
    wave.append(tone("e5", 1))
    wave.append(tone("c#5", 1))
    wave.append(tone("d5", 1))
    wave.append(tone("a5", 2))

    wave.append(tone("b4", 1))
    wave.append(tone("b5", 1))
    wave.append(tone("a5", 1))
    wave.append(tone("g5", 1))
    wave.append(tone("f#5", 1))
    wave.append(tone("g5", 1))
    wave.append(tone("c6", 2))

    wave.append(tone("d6", 1))
    wave.append(tone("c6", 1))
    wave.append(tone("b5", 1))
    wave.append(tone("a5", 1))
    wave.append(tone("g5", 1))
    wave.append(tone("f5", 1))
    wave.append(tone("e5", 1))
    wave.append(tone("d5", 1))
    wave.append(tone("c6", 1.9))
    wave.append(rest(0.1))
    wave.append(tone("c6", 2))
    wave.append(tone("d6", 4))

    # 全部のsin波をつなげる
    wave = np.concatenate(wave, axis=0)
    wave *= VOLUME

    # 鳴らす
    # pyaudioでは波形を量子化ビット数32ビット，
    # 16進数表示でstreamに書き込むことで音を鳴らせる
    stream.write(wave.astype(np.float32).tostring())


if __name__ == '__main__':
    main()
