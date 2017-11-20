#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import math
import numpy as np
import pyaudio

RATE = 44100  # sample rate
CHANNEL_NUM = 1  # チャンネル数 今回はモノラルなので1


def sine(freq, length, rate):
    '''generate tone wave

    周波数，長さ，サンプルレートからsin波を作成する関数
    freq   : frequency [Hz]
    length : wave length [sec]
    rate   : sample rate
    '''
    length = int(length * rate)
    factor = float(freq) * (math.pi * 2) / rate
    return np.sin(np.arange(length) * factor)


def main():
    # 1000Hzのsin波を作る
    wave = sine(1000, 10, RATE)

    # pyaudioのストリームを開く
    # streamへ波形を書き込みすると音が出る
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32, channels=CHANNEL_NUM, rate=RATE,
                     output=True, frames_per_buffer=1024)

    # 鳴らす
    # pyaudioでは波形を量子化ビット数32ビット，
    # 16進数表示でstreamに書き込むことで音を鳴らせる
    stream.write(wave.astype(np.float32).tostring())


if __name__ == "__main__":
    main()
