import math
import time
import numpy as np
import pyaudio

RATE = 44100  # sample rate
CHANNEL_NUM = 1  # チャンネル数 今回はモノラルなので1

VOLUME = 0.1
NOTE_OFFSET = {  # ラ基準
    "a": 0,
    "b": 2,
    "c": -9,
    "d": -7,
    "e": -5,
    "f": -4,
    "g": -2,
    "#": 1,
    "F": -1,  # フラットこれ
}


def seek_freq(string):
    if type(string) != str:
        raise TypeError
    offset = 0.0
    for s in string:
        try:
            offset += NOTE_OFFSET[s] / 12
        except KeyError:
            offset += int(s) - 4
    return 440 * 2**offset


class Score:  # 楽譜で一つのクラスにする BPMはクラスの引数とする

    def __init__(self, score, bpm):
        self.waveall = []  # 全ての波形
        self.bpm = bpm
        for tone_inf_lst in score:  # 和音を加える
            self.waveall.append(self.chord(tone_inf_lst))
        self.waveall = np.concatenate(self.waveall, axis=0)  # 全て合成
        self.waveall *= VOLUME

    def chord(self, tone_inf_lst):  # tone_inf_lstを並列に鳴らしたい
        waves = []
        for tone_inf in tone_inf_lst:  # tone_infは直列に鳴らす
            freq_lst = []  # tone_infの中身の周波数
            length = 0
            sub_wave = np.array([])
            for tone in tone_inf:
                try:
                    freq_lst.append(seek_freq(tone))
                except TypeError:
                    length = tone
                    sub_wave = np.append(sub_wave,
                                         self.make_wave(freq_lst, length))
                    freq_lst = []  # 加えたので周波数初期化
            waves.append(sub_wave)  # 直列に合成
        return np.sum(waves, axis=0)  # 並列に合成

    def make_wave(self, freq_lst, length):  # 同時に鳴らしたい周波数リストとその長さを指定し、波形を返す関数
        wave = 0
        for freq in freq_lst:
            step = (2 * math.pi) * freq / 44100  # 2πf*(1/rate)
            wave += np.sin(step * np.arange(length * (
                60 / self.bpm) * RATE))  # sin(2πft) ここでクラス作った意味が生きる
            wave *= np.linspace(1.5, 0.3, len(wave))
        return wave


def main():
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paFloat32, channels=CHANNEL_NUM, rate=RATE,
                     output=True)

    # 調の指定はまた今度がんばる

    waveag = Score([
        [["d5", "b4", 1]],
        [["g5", "b4", 2]],
        [["b5", 0.5, "g5", 0.5], ["d5", 1]],
        [["b5", "d5", 2]],
        [["a5", "c5", 1]],
        [["g5", "b4", 2]],
        [["e5", "c5", 1]],
        [["d5", "b4", 2]],
    ], 120).waveall

    stream.write(waveag.astype(np.float32).tostring())

    time.sleep(3)

    wavej = Score([
        [["g4", 0.5]],
        [["bF4", 0.5]],
        [["c5", "aF4", 1]],
        [["c5", 0.5]],
        [["eF5", 0.5]],
        [["aF4", "d5", 0.75]],
        [["bF4", 0.25]],
        [["eF5", "bF4", 0.5]],
        [["f5", 0.5]],
        [["eF5", 1]],
        [["d5", "bF4", 1]],
        [["c5", "aF4", 0.5]],
        [["d5", 0.5]],
        [["c5", 1]],
        [["bF4", "f4", 1]],
        [["g4", "eF4", 2]],
    ], 90).waveall

    stream.write(wavej.astype(np.float32).tostring())


if __name__ == '__main__':
    main()
