import numpy as np
import os
import shutil
from generation_utils import annotate, create_signals
from spectrogram_utils import create_spectrogram

import argparse


def verify_directory(directory, clear):
    if os.path.exists(directory) and clear:
        shutil.rmtree(directory)
    os.makedirs(directory)


def main(flags):
    max_signals = flags['max_signals']
    image_size = (flags['image_height'], flags['image_width'])
    directory = flags['generation_directory']

    verify_directory(directory, flags['clear_generation_directory'])

    for _ in range(flags['quantity']):
        sigs = create_signals(max_signals=max_signals)

        spectrogram = create_spectrogram(sigs + 1.15 * np.random.randn(len(sigs)), 2 ** 11)
        spectrogram = np.hsplit(spectrogram, 2)[0]

        spectrogram = ((spectrogram - spectrogram.min()) * (
                1 / (spectrogram.max() - spectrogram.min()) * 255)).astype('uint8')

        annotate(spectrogram, image_size, directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--max_signals', type=int,
                        default=40,
                        help='The number of signals to generate in each spectrogram')

    parser.add_argument('--image_height', type=int,
                        default=1500,
                        help='The height of the generated images')

    parser.add_argument('--image_width', type=int,
                        default=600,
                        help='The width of the generated images')

    parser.add_argument('--generation_directory', type=str,
                        default="../data_gen/",
                        help='The directory to store the data in')

    parser.add_argument('--quantity', type=int,
                        default=200,
                        help='The number of examples to generate')

    parser.add_argument('--clear_generation_directory', type=bool,
                        default=True,
                        help='Boolean to indicate whether to clear the genration directory before use.')

    parsed_flags, _ = parser.parse_known_args()

    main(parsed_flags)
