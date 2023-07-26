import dask
from dask.diagnostics import ProgressBar
import os
import shutil
import argparse
from generation_utils import generate_example


def verify_directory(directory, clear):
    if os.path.exists(directory) and clear:
        shutil.rmtree(directory)
    os.makedirs(directory)


def main(flags):
    max_signals = flags.max_signals
    image_size = flags.image_height, flags.image_width
    directory = flags.generation_directory

    verify_directory(directory, flags.clear_generation_directory)

    if flags.use_dask:
        dask_tasks = [dask.delayed(generate_example)(directory, max_signals,
                                                     flags.noise_intensity,
                                                     image_size, flags.sub_labels) for _ in range(flags.quantity)]
        with ProgressBar():
            dask.compute(*[dask_tasks])
    else:
        for _ in range(flags.quantity):
            generate_example(directory, max_signals, flags.noise_intensity, image_size, flags.sub_labels)

            print(f"Finished {_} of {flags.quantity}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--max-signals', type=int,
                        default=40,
                        help='The number of signals to generate in each spectrogram')

    parser.add_argument('--image-height', type=int,
                        default=1500,
                        help='The height of the generated images')

    parser.add_argument('--image-width', type=int,
                        default=600,
                        help='The width of the generated images')

    parser.add_argument('--generation-directory', type=str,
                        default="../data_gen/",
                        help='The directory to store the data in')

    parser.add_argument('--quantity', type=int,
                        default=1000,
                        help='The number of examples to generate')

    parser.add_argument('--clear-generation-directory', type=bool,
                        default=True,
                        help='Boolean to indicate whether to clear the generation directory before use.')

    parser.add_argument('--noise-intensity', type=float,
                        default=0.999,
                        help='The scalar to multiply the noise by')

    parser.add_argument('--sub-labels', type=bool,
                        default=False,
                        help='Boolean to indicate whether to create labels for the individual signals in the spectrogram')

    parser.add_argument('--use-dask', type=bool,
                        default=True,
                        help='Boolean to indicate whether to use dask for parallel processing')

    parsed_flags, _ = parser.parse_known_args()

    main(parsed_flags)
