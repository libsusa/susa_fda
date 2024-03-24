import enum
import numpy as np

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class FilterResponse(enum.Enum):
    LowPass = 1
    HighPass = 2
    BandPass = 3
    BandStop = 4

class WindowType(enum.Enum):
    Rectangular = 1
    Triangular = 2
    Welch = 3
    Sine = 4
    Hann = 5
    Hamming = 6
    Blackman = 7
    Nuttall = 8
    BlackmanNuttall = 9
    BlackmanHarris = 10
    FlatTop = 11
    Kaiser = 12

class WindowDesign(object):
    SAMPLE_TIME_S = 0.01
    CUTOFF_FREQUENCY_HZ = 10.0
    CUTOFF_FREQUENCY2_HZ = 100.0
    NUM_TOTAL_SAMPLES = 128
    NUM_SHIFT_SAMPLES = 64
    WIN_TYPE = WindowType.Blackman
    RESPONSE_TYPE = FilterResponse.BandPass
    NUM_FREQ_SAMPLES = 1024

    def __init__(self) -> None:
        super().__init__()

    def ComputeTimeVector(self):
        self.vec_samples = np.arange(0, self.NUM_TOTAL_SAMPLES)
        self.vec_time = self.vec_samples * self.SAMPLE_TIME_S

    def ComputeFrequencyVector(self):
        df = (0.5 / self.SAMPLE_TIME_S) / (self.NUM_FREQ_SAMPLES - 1.0)
        self.vec_freqs = np.arange(0,self.NUM_FREQ_SAMPLES) * df

    def ComputeWindow(self):

        if self.WIN_TYPE == WindowType.Rectangular:
            self.window = np.ones(self.NUM_TOTAL_SAMPLES)
        elif self.WIN_TYPE == WindowType.Triangular:
            self.window = 1.0 - np.abs((self.vec_samples - 0.5 * self.NUM_TOTAL_SAMPLES) / (0.5 * self.NUM_TOTAL_SAMPLES))
        elif self.WIN_TYPE == WindowType.Blackman:
            self.window = 0.42 - 0.5 * np.cos(2.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES) + 0.08 * np.cos(4.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES)
        elif self.WIN_TYPE == WindowType.Welch:
            self.window = 1.0 - np.power((self.vec_samples - 0.5 * self.NUM_TOTAL_SAMPLES) / (0.5 * self.NUM_TOTAL_SAMPLES), 2.0)
        elif self.WIN_TYPE == WindowType.Sine:
            self.window = np.sin(np.pi * self.vec_samples / (self.NUM_TOTAL_SAMPLES))
        elif self.WIN_TYPE == WindowType.Hann:
            self.window = 0.5 * (1 - np.cos(2.0 * np.pi * self.vec_samples / (self.NUM_TOTAL_SAMPLES)))
        elif self.WIN_TYPE == WindowType.Hamming:
            self.window = (25.0 / 46.0) - (21.0 / 46.0) * np.cos(2.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES)
        elif self.WIN_TYPE == WindowType.Nuttall:
            self.window = 0.355768 - 0.487396 * np.cos(2.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES) + 0.144232 * np.cos(4.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES) - 0.012604 * np.cos(6.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES)
        elif self.WIN_TYPE == WindowType.BlackmanNuttall:
            self.window = 0.3635819 - 0.4891775 * np.cos(2.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES) + 0.1365995 * np.cos(4.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES) - 0.0106411 * np.cos(6.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES)
        elif self.WIN_TYPE == WindowType.BlackmanHarris:
            self.window = 0.35875 - 0.48829 * np.cos(2.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES) + 0.14128 * np.cos(4.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES) - 0.01168 * np.cos(6.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES)
        elif self.WIN_TYPE == WindowType.FlatTop:
            self.window = 0.21557895 - 0.41663158 * np.cos(2.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES) + 0.277263158 * np.cos(4.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES) - 0.083578947 * np.cos(6.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES) + 0.006947368 * np.cos(8.0 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES)
        elif self.WIN_TYPE == WindowType.Kaiser:
            self.window = 0.54 - 0.46 * np.cos(2 * np.pi * self.vec_samples / self.NUM_TOTAL_SAMPLES)
        else:
            self.window = np.ones(self.NUM_TOTAL_SAMPLES)

    def ComputeResponse(self):
        vec_shift = self.vec_samples - self.NUM_SHIFT_SAMPLES
        vec_shift[self.NUM_SHIFT_SAMPLES] = 1
        vec_time_shift = self.SAMPLE_TIME_S * vec_shift
        if self.RESPONSE_TYPE == FilterResponse.LowPass:
            self.ir = np.sin(2.0 * np.pi * self.CUTOFF_FREQUENCY_HZ * vec_time_shift) / (np.pi * vec_time_shift)
            self.ir[self.NUM_SHIFT_SAMPLES] = 2.0 * self.CUTOFF_FREQUENCY_HZ
        elif self.RESPONSE_TYPE == FilterResponse.HighPass:
            self.ir = (np.sin(np.pi * vec_shift) - np.sin(2.0 * np.pi * self.CUTOFF_FREQUENCY_HZ * vec_time_shift)) / (np.pi * vec_time_shift)
            self.ir[self.NUM_SHIFT_SAMPLES] = 1.0 / self.SAMPLE_TIME_S - 2.0 * self.CUTOFF_FREQUENCY_HZ
        elif self.RESPONSE_TYPE == FilterResponse.BandPass:
            self.ir = (np.sin(2.0 * np.pi * self.CUTOFF_FREQUENCY2_HZ * vec_time_shift) - np.sin(2.0 * np.pi * self.CUTOFF_FREQUENCY_HZ * vec_time_shift)) / (np.pi * vec_time_shift)
            self.ir[self.NUM_SHIFT_SAMPLES] = 2.0 * self.CUTOFF_FREQUENCY2_HZ - 2.0 * self.CUTOFF_FREQUENCY_HZ
        elif self.RESPONSE_TYPE == FilterResponse.BandStop:
            self.ir = (np.sin(2.0 * np.pi * self.CUTOFF_FREQUENCY_HZ * vec_time_shift) - np.sin(2.0 * np.pi * self.CUTOFF_FREQUENCY2_HZ * vec_time_shift) + np.sin(np.pi * vec_shift)) / (np.pi * vec_time_shift)
            self.ir[self.NUM_SHIFT_SAMPLES] = 2.0 * self.CUTOFF_FREQUENCY_HZ - 2.0 * self.CUTOFF_FREQUENCY2_HZ + 1.0 / self.SAMPLE_TIME_S

        self.ir *= self.SAMPLE_TIME_S

    def ComputeWindowedResponses(self):
        self.wir = self.ir * self.window
        logger.debug(f'number of taps: {self.wir.shape[0]}')

    def DFT_matrix(self):
        i, j = np.meshgrid(self.vec_time, self.vec_freqs)
        W = np.exp( - 2.0 * np.pi * 1J * i * j ) #/ math.sqrt(self.vec_time.shape[0])
        return W

    def ComputeRespBode(self):
        W = self.DFT_matrix()
        with np.errstate(divide='ignore'):
            self.bode_window = 20.0 * np.log10(np.absolute(np.dot(W, self.window)))
            self.bode_wir = 20.0 * np.log10(np.absolute(np.dot(W, self.wir)))
            self.phase_wir = np.angle(np.dot(W, self.wir))

    def update(self):
        self.ComputeTimeVector()
        self.ComputeWindow()
        self.ComputeResponse()
        self.ComputeWindowedResponses()

        self.ComputeFrequencyVector()
        self.ComputeRespBode()
