import sys
import copy
import scipy.io.wavfile
import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt
from pylab import stem
from pylab import fft

testing_frequency = 140


def main(file):
    w, signal = scipy.io.wavfile.read(file)
    if len(np.shape(signal)) == 2:
        signal = [s[0] for s in signal]

    part = len(signal) / 5
    signal = signal[int(part):int(2*part)]
    spec = abs(fft(signal))
    clear_spectrum = copy.copy(spec)
    for i in range(2, 6):
        dec_spec = sig.decimate(clear_spectrum, i)
        spec[:len(dec_spec)] *= dec_spec
    # fig = plt.figure(figsize=(15, 15), dpi=80)
    # ax = fig.add_subplot(111)
    #
    # freqs = range(int(len(spec)))
    #
    # ax.set_yscale('log')
    # stem(freqs, spec, '-.')
    # ax.set_xlabel('Frequency [Hz]')
    # ax.set_ylabel('Amplitude [j]')
    # plt.show()
    peak = np.argmax(spec)
    if peak > testing_frequency:
        print("K")
        return 0
    else:
        print("M")
        return 1


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("give the path")