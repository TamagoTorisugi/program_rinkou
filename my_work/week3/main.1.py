import math
import time
import numpy as np
import pyaudio
import sys

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
}


def seek_freq(string, sharp, flat):
    offset = 0.0
    order_s = 'fcgdaeb'
    order_f = 'beadgcf'
    natural = False
    for s in string:
        if s in NOTE_OFFSET:
            note = s
            offset += NOTE_OFFSET[s] / 12
        elif s == 'N':  # ナチュラル
            natural = True
        elif s == '#':
            offset += 1.0 / 12
            natural = True
        elif s == 'F':  # フラット 
            offset -= 1.0 / 12
            natural = True
        elif s.isdigit():
            if not(natural):  # 臨時記号がない場合、調の指定からoffsetを調整
                if order_s.find(note) < sharp:
                    offset += 1.0 / 12
                elif order_f.find(note) < flat:
                    offset -= 1.0 / 12
            offset += int(s) - 4
        else:
            print("Error.")
            sys.exit(1)
    return 440 * 2**offset


class Score(object):  # 楽譜で一つのクラスにする BPMはクラスの引数とする

    def __init__(self, score, bpm, sf_str='#',sf_num=0):
        self.waveall = []  # 全ての波形
        self.bpm = bpm
        if sf_str == '#':
            self.sharp = sf_num
            self.flat = 0
        elif sf_str == 'F':
            self.sharp = 0
            self.flat = sf_num
        else:
            print("Error.")
            sys.exit(1)

        for tone_inf_lst in score:  # 和音を加える
            self.waveall.append(self.chord(tone_inf_lst))
        self.waveall = np.concatenate(self.waveall, axis=0)  # 全て合成
        self.waveall *= VOLUME

    def chord(self, tone_inf_lst):  # tone_inf_lstを並列に鳴らしたい
        waves = []
        for tone_inf in tone_inf_lst:  # tone_infは直列に鳴らす
            freq_lst = []  # tone_infの中身の周波数
            sub_wave = np.array([])
            for tone in tone_inf:
                if type(tone) == str:
                    freq_lst.append(seek_freq(tone, self.sharp, self.flat))
                else:
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

    def play(self):  # オブジェクト指向っぽさを出す
        pa = pyaudio.PyAudio()
        stream = pa.open(format=pyaudio.paFloat32, channels=CHANNEL_NUM, rate=RATE,
                         output=True)
        stream.write(self.waveall.astype(np.float32).tostring())


def main():

    # 調の指定に対応！

    scoreag = Score([
        [["d5", "b4", 1]],
        [["g5", "b4", 2]],
        [["b5", 0.5, "g5", 0.5], ["d5", 1]],
        [["b5", "d5", 2]],
        [["a5", "c5", 1]],
        [["g5", "b4", 2]],
        [["e5", "c5", 1]],
        [["d5", "b4", 2]],
    ], 120)

    scoreag.play()

    time.sleep(2)

    scorej = Score([
        [["g4", 0.5]],
        [["b4", 0.5]],
        [["c5", "a4", 1]],
        [["c5", 0.5]],
        [["e5", 0.5]],
        [["a4", "d5", 0.75]],
        [["b4", 0.25]],
        [["e5", "b4", 0.5]],
        [["f5", 0.5]],
        [["e5", 1]],
        [["d5", "b4", 1]],
        [["c5", "a4", 0.5]],
        [["d5", 0.5]],
        [["c5", 1]],
        [["b4", "f4", 1]],
        [["g4", "e4", 2]],
    ], 90, 'F', 3)

    scorej.play()

    time.sleep(2)

    scorec = Score([
        [["f4", "d5", 2], ["d3", 1, "f3", 1]],
        [["a4", "c5", 2], ["a3", 1, "g3", 1]],
        [["d4", "b4", 2], ["f3", 1, "d3", 1]],
        [["f4", "a4", 2], ["f3", 1, "e3", 1]],
        [["b3", "g4", 2], ["d3", 1, "b2", 1]],
        [["d4", "f4", 2], ["d3", 1, "a2", 1]],
        [["b3", "g4", 2], ["g2", 1, "b2", 1]],
        [["c4", "a4", 2], ["c3", 1, "a2", 1]],
    ], 60, '#', 2)
    scorec.play()


if __name__ == '__main__':
    main()
