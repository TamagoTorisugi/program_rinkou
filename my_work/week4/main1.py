import math
import re

import numpy as np
import pyaudio


class Note(object):
    """音符を表すクラス"""

    base_key_factor = {  # ラの音を基準にしたときの半音の隔たり
        'c': -9,
        'd': -7,
        'e': -5,
        'f': -4,
        'g': -2,
        'a': 0,
        'b': 2,
    }

    def __init__(self, scale, length=1):
        """イニシャライザ
 
        scale: 単一の音名
        length: 音の長さ(4分音符が1)
        """
        self.freq = self.freq_from_scale(scale)
        self.length = length

    def freq_from_scale(self, scale):
        """単一のscaleに対する周波数を返す
 
        例： "c#5" -> 554.365, "a5"-> 880.000
        """

        # 正規表現で音階，変化記号，オクターブ番号を抽出
        match = re.match(r'([a-gA-G])([b#]?)([0-9]+)$', scale)
        key, accidental, octave_str = match.groups()
        octave = int(octave_str)

        factor = self.__class__.base_key_factor[key]

        if accidental == '#':
            factor += 1
        elif accidental == 'b':
            factor -= 1

        freq = 440 * 2**((octave - 4) + factor / 12)
        return freq

    def generate_wave(self, bpm, rate):
        """波形を返すメソッド
 
        bpm: 曲の速さ
        rate: sample rate
        """

        length = int(self.length * (60 / bpm) * rate)
        factor = 2 * math.pi * self.freq / rate

        wave = np.sin(factor * np.arange(length))

        return wave


class SimpleMusic(object):
    volume = 0.1  # 音量
    channel_num = 1  # チャンネル数，今回はモノラルなので1
    """簡単な音楽を鳴らすクラス"""

    def __init__(self, bpm, rate=44100):
        """Initializer
 
        bpm: 曲の速度
        rate: サンプルレート
        """
        self.bpm = bpm
        self.rate = rate
        self.notes = []

    def append_note(self, note):
        """Noteオブジェクトをnotesに追加"""
        self.notes.append(note)

    def play(self):
        """notesを元に音を鳴らす"""
        waves = [
            note.generate_wave(self.bpm, self.rate) for note in self.notes
        ]
        wave = np.concatenate(waves, axis=0)
        wave *= self.__class__.volume

        pa = pyaudio.PyAudio()
        stream = pa.open(format=pyaudio.paFloat32,
                         channels=self.__class__.channel_num, rate=self.rate,
                         output=True)

        # 鳴らす
        stream.write(wave.astype(np.float32).tostring())

    @classmethod
    def sample_music(cls):
        music = cls(bpm=120)
        music.append_note(Note("c4"))
        music.append_note(Note("d4"))
        music.append_note(Note("e4"))
        music.append_note(Note("f4"))
        music.append_note(Note("g4"))
        music.append_note(Note("a4"))
        music.append_note(Note("b4"))
        music.append_note(Note("c5"))
        music.play()


def main():
    SimpleMusic(bpm=120).sample_music() # これでいいのか...


if __name__ == '__main__':
    main()