import os
import sys
import warnings
import scipy.io.wavfile

from copy import deepcopy
from numpy import shape, mean, argmax
from random import choice

from numpy.fft import rfft
from numpy.ma import multiply
from scipy.signal import decimate

if not sys.warnoptions:
    warnings.simplefilter("ignore")


def main(file_path):
    frequency, signal = scipy.io.wavfile.read(file_path)
    full_time = len(signal) / frequency

    if len(shape(signal)) == 2:
        signal = [mean(s) for s in signal]

    part = int(len(signal) / 5)
    signal = signal[2 * part:3 * part]
    cut_time = full_time * 1 / 5

    spec = abs(rfft(signal))
    clean_spec = deepcopy(spec)

    for i in range(2, 6):
        dec_spec = decimate(clean_spec, i)
        spec = multiply(spec[:len(dec_spec)], dec_spec)

    peak = (35 + argmax(spec[35:])) / cut_time
    if peak > 170:
        return "K"
    else:
        return "M"


Md, M, Kd, K = 0, 0, 0, 0
files = os.listdir("data/train/")
files = files[1:]

for file in files:
    try:
        test = main("data/train/" + file)

    except:
        test = choice(['M', 'K'])

    shouldBe = file[4]
    if shouldBe == 'M':
        M += 1
        if test == 'M':
            Md += 1
    if shouldBe == 'K':
        K += 1
        if test == 'K':
            Kd += 1

print(Md, M, Kd, K)
print((Md + Kd) / (M + K))

# if __name__ == '__main__':
#     try:
#         print(main(sys.argv[1]))
#     except:
#         print(choice(['M', 'K']))
