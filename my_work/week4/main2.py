import numpy as np


class RingBuffer(object):

    def __init__(self, capacity):  # capacity:最大の容量
        self.capacity = capacity
        self.list = np.empty(capacity)
        # pythonのリストは使いたくないのでndarray(その代わり数字しか入らないが)
        self.begin = 0  # -capacity + 1 <= begin  <= 0
        self.end = 0  # capacity - 1 >= end >= 0

    def append_front(self, item):  # 先頭にitemを追加
        self.list[self.begin - 1] = item  # パワポの配列を左から0,1,2,3,...とindexづけ
        if self.begin + self.capacity == self.end:
            self.end_forward()
        self.begin_forward()

    def append_back(self, item):  # 最後尾にitemを追加
        self.list[self.end] = item
        if self.begin + self.capacity == self.end:
            self.begin_backward()
        self.end_backward()


# 関数定義しまくりで嫌だけどいい案が思いつかなかった

    def begin_forward(self):  # ポインタbeginを1つ最後尾方向に進める
        self.begin -= 1
        if self.begin == -self.capacity:
            self.begin = 0

    def begin_backward(self):  # ポインタbeginを1つ先頭方向に進める
        self.begin += 1
        if self.begin == 1:
            self.begin = -self.capacity + 1

    def end_forward(self):  # ポインタendを1つ最後尾方向に進める
        self.end -= 1
        if self.end == -1:
            self.end = self.capacity - 1

    def end_backward(self):  # ポインタendを1つ先頭方向に進める
        self.end += 1
        if self.end == self.capacity:
            self.end = 0

    def pop_front(self):  # 先頭のitemをreturnし削除
        self.begin_backward()

    def pop_back(self):  # 最後尾のitemをreturnし削除
        self.end_forward()

    def get_list(self):  # beginからendまでの値を配列として返す
        if self.begin + self.capacity >= self.end:
            lst = []
            for i in range(self.begin, 0):
                lst.append(self.list[i])
            for i in range(self.end):
                lst.append(self.list[i])
            print(lst)
        else:
            lst = []
            for i in range(self.begin + self.capacity, self.end):
                lst.append(self.list[i])
            print(lst)


def main():
    ringbuffer = RingBuffer(5)

    ringbuffer.append_front(1)
    ringbuffer.append_front(2)
    ringbuffer.append_front(3)
    ringbuffer.get_list()

    ringbuffer.append_back(4)
    ringbuffer.append_back(5)
    ringbuffer.append_back(6)
    ringbuffer.append_back(7)
    ringbuffer.get_list()

    ringbuffer.pop_front()
    ringbuffer.pop_front()
    ringbuffer.get_list()

    ringbuffer.pop_back()
    ringbuffer.get_list()

    ringbuffer.append_front(8)
    ringbuffer.get_list()


if __name__ == '__main__':
    main()