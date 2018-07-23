import datetime
import time
import os
import sys


class ProgressBar:
    # this the the no. of chars that are always displayed on the screen
    # default is 6 for "[{}{}]({__})(:.7)"
    # 			^    ^^ ^^ ^

    @staticmethod
    def getTermSizeWidth():
        return int(os.popen("stty size", "r").read().split()[1])

    def __init__(self, size=None, filler='█', empty=' ', output_stream=sys.stdout):
        self.output_stream = output_stream
        self.output_stream.write("\r")
        self.adjFactor = 15
        self.filled = 0
        self.filler = filler
        self.empty = empty
        if size is None:
            self.size = self.getTermSizeWidth()-3
        else:
            self.size = size
        self.output_stream.write("[{}](PP)(timeETA)".format(
            self.empty * (self.size-self.adjFactor)))
        self.storedLog = []
        self.output_stream.write("\b" * (self.size-1))
        self.output_stream.flush()
        self.then = time.time()

    def __enter__(self):
        return self

    def log(self, k):
        self.storedLog.append(k)

    def fraction(self, percent):
        if percent >= 1:
            time_elapsed = time.time()-self.then
            self.output_stream.write("\r")
            self.output_stream.write("[{}]({:2})({:.7s})".format(
                self.filler*(self.size-self.adjFactor), "99",
                str(datetime.timedelta(seconds=time_elapsed))))
        else:
            printed_this_much = int(
                percent*(self.size-self.adjFactor) - self.filled)
            if printed_this_much < 0:
                self.output_stream.write("\r"*abs(printed_this_much))
            else:
                self.output_stream.write(self.filler*printed_this_much)
            self.filled += printed_this_much
            eta = 0
            if percent == 0:
                self.then = time.time()
            else:
                eta = (time.time() - self.then)*(1/percent-1)

            blanks = self.size-self.filled-self.adjFactor
            self.output_stream.write(self.empty*blanks)
            self.output_stream.write(
                "]({:2d})".format((int(percent*100) % 100)))
            try:
                self.output_stream.write("({:.7s})".format(
                    str(datetime.timedelta(seconds=eta))))
            except OverflowError:
                self.output_stream.write("(forever)")
            self.output_stream.write("\b"*(self.adjFactor-1))
            self.output_stream.write("\b"*blanks)
        self.output_stream.flush()

    def __exit__(self, *a):
        self.fraction(1)
        self.output_stream.flush()
        print(*self.storedLog)


class iterable(ProgressBar):
    def __init__(self, start, end=None, step=1, size=None,
                 filler='█', empty=' '):
        super().__init__(size, filler, empty)
        if end is None:
            self.end = start
            self.at = 0
        else:
            self.end = end
            self.at = start
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.at >= self.end:
            self.__exit__()
            raise StopIteration
        else:
            self.fraction(self.at/self.end)
            self.at += self.step
            return self.at - self.step


if __name__ == "__main__":
    print("Testing")
    iterations = 10000
    for i in iterable(iterations):
        time.sleep(0.0001)        # Heavy load!

    print("Testing 2")
    my_bar = ProgressBar(filler="O", empty="o")
    for k in range(iterations):
        my_bar.fraction(k/iterations)
        time.sleep(0.0001)        # Heavy load!
    my_bar.__exit__()

    then = time.time()
    count = 0
    print("Without any bar...(stay patient)")
    for i in range(iterations):
        time.sleep(0.0001)        # Heavy load!
    print("{:.7} iterations = {} without any bar printing".format(
        str(datetime.timedelta(seconds=(time.time()-then))), count))
    print("Few more tests")
    import random
    my_bar = ProgressBar()
    test_types = ["I", "-", "_", "=", "+", "0", "O", "o", "*", ".", "#"]
    for k in range(10):
        my_bar.empty = random.choice(test_types)
        test_types.remove(my_bar.empty)
        my_bar.filler = random.choice(test_types)
        time.sleep(0.001)
        my_bar.fraction(random.random())
        my_bar.filled = 0
        print()
