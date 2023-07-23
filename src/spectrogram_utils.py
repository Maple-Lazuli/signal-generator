import numpy as np
import matplotlib.pyplot  as plt


def create_spectrogram(signal, fft_size):
    num_rows = len(signal) // fft_size # // is an integer division which rounds down
    spectrogram = np.zeros((num_rows, fft_size))
    for i in range(num_rows):
        spectrogram[i,:] = np.log10(np.abs(np.fft.fftshift(np.fft.fft(signal[i*fft_size:(i+1)*fft_size])))**2)
    return spectrogram


def plot_spectrogram(spectrogram, sample_rate, sig, MHz=False):
    if MHz:
        spectrogram_boundary = [sample_rate / -2 / 1e6, sample_rate / 2 / 1e6, 0, len(sig) / sample_rate]
    else:
        spectrogram_boundary = [sample_rate / -2, sample_rate / 2, 0, len(sig) / sample_rate]

    plt.imshow(spectrogram, aspect='auto', extent=spectrogram_boundary)
    plt.xlabel(f"Frequency [{'MHz' if MHz else 'Hz'}]")
    plt.ylabel("Time [s]")
    plt.show()
