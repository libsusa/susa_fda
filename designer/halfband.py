import numpy as np
from scipy import signal

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def dB20(array):
    with np.errstate(divide='ignore'):
        return 20 * np.log10(array)


def fir_calc_filter(Fs, Fpb, Fsb, Apb, Asb, N):

    bands = np.array([0., Fpb/Fs, Fsb/Fs, .5])

    err_pb = (1 - 10**(-Apb/20))/2
    err_sb = 10**(-Asb/20)

    w_pb = 1/err_pb
    w_sb = 1/err_sb

    h = signal.remez(N + 1, bands, [1,0], [w_pb, w_sb])

    (w,H) = signal.freqz(h)

    Hpb_min = min(np.abs(H[0:int(Fpb/Fs*2 * len(H))]))
    Hpb_max = max(np.abs(H[0:int(Fpb/Fs*2 * len(H))]))
    Rpb = 1 - (Hpb_max - Hpb_min)

    Hsb_max = max(np.abs(H[int(Fsb/Fs*2 * len(H)+1):len(H)]))
    Rsb = Hsb_max

    logger.debug("Rpb: %fdB" % (-dB20(Rpb)))
    logger.debug("Rsb: %fdB" % -dB20(Rsb))

    return (h, w, H, Rpb, Rsb, Hpb_min, Hpb_max, Hsb_max)

def fir_find_optimal_N(Fs, Fpb, Fsb, Apb, Asb, Nmin = 1, Nmax = 1000):
    for N in range(Nmin, Nmax):
        logger.debug("Trying N=%d" % N)
        (h, w, H, Rpb, Rsb, Hpb_min, Hpb_max, Hsb_max) = fir_calc_filter(Fs, Fpb, Fsb, Apb, Asb, N)
        if -dB20(Rpb) <= Apb and -dB20(Rsb) >= Asb:
            return N

    return None


def half_band_calc_filter(Fs, Fpb, N):
    assert Fpb < Fs/4, "A half-band filter requires that Fpb is smaller than Fs/4"
    assert N % 2 == 0, "Filter order N must be a multiple of 2"
    assert N % 4 != 0, "Filter order N must not be a multiple of 4"

    g = signal.remez(
            N//2+1,
            [0., 2*Fpb/Fs, .5, .5],
            [1, 0],
            [1, 1]
            )

    zeros = np.zeros(N//2+1)

    h = [item for sublist in zip(g, zeros) for item in sublist][:-1]
    h[N//2] = 1.0
    h = np.array(h)/2

    (w,H) = signal.freqz(h)

    Fsb = Fs/2-Fpb

    Hpb_min = min(np.abs(H[0:int(Fpb/Fs*2 * len(H))]))
    Hpb_max = max(np.abs(H[0:int(Fpb/Fs*2 * len(H))]))
    Rpb = 1 - (Hpb_max - Hpb_min)

    Hsb_max = max(np.abs(H[int(Fsb/Fs*2 * len(H)+1):len(H)]))
    Rsb = Hsb_max

    logger.debug("Rpb: %fdB" % (-dB20(Rpb)))
    logger.debug("Rsb: %fdB" % -dB20(Rsb))

    return (h, w, H, Rpb, Rsb, Hpb_min, Hpb_max, Hsb_max)

def half_band_find_optimal_N(Fs, Fpb, Apb, Asb, Nmin = 2, Nmax = 1000):
    for N in range(Nmin, Nmax, 4):
        logger.debug("Trying N=%d" % N)
        (h, w, H, Rpb, Rsb, Hpb_min, Hpb_max, Hsb_max) = half_band_calc_filter(Fs, Fpb, N)
        if -dB20(Rpb) <= Apb and -dB20(Rsb) >= Asb:
            return N

    return None


class HalfbandDesign(object):

    def __init__(self) -> None:
        super().__init__()