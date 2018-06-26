import os
import sys


class ProgressBar:
    storedLog = []
    # this the the no. of chars that are always displayed on the screen
    # default is 6 for "[{}{}]({__})"
    # 					^    ^^ ^^ ^

    @staticmethod
    def getTermSizeWidth():
        return int(os.popen("stty size", "r").read().split()[1])

    def __init__(self, size=None, filler='-', empty=' '):
        self.adjFactor = 6
        self.filler = filler
        self.empty = empty
        if size is None:
            self.size = self.getTermSizeWidth()-5
        else:
            self.size = size
        sys.stdout.write("[{}](__)".format(
            self.empty * (self.size-self.adjFactor)))
        # sys.stdout.flush()
        # sys.stdout.write("\b" * (self.size-1))
        # self.size -= 7

    def __enter__(self):
        return self

    def log(self, k):
        self.storedLog.append(k)

    def percent(self, percent):

        sys.stdout.write("\b"*self.size)
        if percent >= 1:
            sys.stdout.write("[{}]({})".format(
                self.filler*(self.size-self.adjFactor), "99"))
        else:
            sys.stdout.write("[{}{}]({})".
                             format(self.filler*int(percent *
                                                    (self.size -
                                                     self.adjFactor)),
                                    self.empty*int((1-percent) *
                                                   (self.size-self.adjFactor)),
                                    str(percent*100)[:2]))

        # self.diff = int(percent*self.size - self.filled)
        # sys.stdout.write(self.empty*(self.size-self.filled+1))
        # sys.stdout.write(self.
        # if self.diff:
        #     sys.stdout.write(self.filler*self.diff)
        #     self.filled += self.diff
        #     sys.stdout.flush()
        sys.stdout.flush()

    def __exit__(self, *a):
        self.percent(1)
        sys.stdout.flush()
        print(*self.storedLog)


class iter(ProgressBar):
    def __init__(self, start, end=None, step=1, size=None,
                 filler='-', empty=' '):
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
            self.percent(self.at/self.end)
            self.at += self.step
            return self.at - self.step
