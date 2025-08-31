from gnuradio import gr, analog, blocks
import numpy as np

class SDRSource(gr.top_block):
    def __init__(self, samp_rate=1e6, freq=100e3, amplitude=1):
        super().__init__()
        self.samp_rate = samp_rate
        self.freq = freq
        self.amplitude = amplitude

        self.src = analog.sig_source_f(self.samp_rate, analog.GR_SIN_WAVE, self.freq, self.amplitude)
        self.sink = blocks.vector_sink_f()
        self.connect(self.src, self.sink)

    def update_params(self, freq=None, samp_rate=None, amplitude=None):
        if freq: self.src.set_frequency(freq)
        if samp_rate: self.src.set_sampling_freq(samp_rate)
        if amplitude: self.src.set_amplitude(amplitude)

    def run_capture(self):
        self.run()
        return np.array(self.sink.data())
