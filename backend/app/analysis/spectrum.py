import numpy as np

class SpectrumAnalyzer:
    def spectrum(self, data):
        fft_vals = np.fft.fft(data)
        fft_freq = np.fft.fftfreq(len(data))
        magnitude = np.abs(fft_vals)
        return fft_freq[:len(data)//2], magnitude[:len(data)//2]
