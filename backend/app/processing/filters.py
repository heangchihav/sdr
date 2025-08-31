from scipy.signal import butter, lfilter

class BandPassFilter:
    def __init__(self, lowcut, highcut, fs, order=5):
        self.lowcut = lowcut
        self.highcut = highcut
        self.fs = fs
        self.order = order

    def filter(self, data):
        nyq = 0.5 * self.fs
        low = self.lowcut / nyq
        high = self.highcut / nyq
        b, a = butter(self.order, [low, high], btype='band')
        return lfilter(b, a, data)
