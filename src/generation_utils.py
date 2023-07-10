import random
import numpy as np
from PIL import Image, ImageDraw
import hashlib
from datetime import datetime
import os
import json
from modulator import Modulator
from transmission import Transmission


def create_notcher(size):
    mode = random.randint(1, 3)
    notcher = np.zeros(size)
    if mode == 1:  # Continuous Mode
        start = int(random.randint(1, 50) / 100)
        end = int(random.randint(6, 90) / 100)
        for idx in range(0, len(notcher)):
            if start < idx < end:
                notcher[idx] = 1

    elif mode == 2:
        toggle_rate = int(random.randint(20, 300) / 1000 * size)
        power = random.randint(0, 1)
        counter = 0
        for idx in range(len(notcher)):
            counter += 1
            notcher[idx] = power
            if counter > toggle_rate:
                counter = 0
                power = 1 if power == 0 else 0

    elif mode == 3:
        toggle_rate = int(random.randint(80, 300) / 1000 * size)
        toggle_on = int(toggle_rate * random.randint(10, 90) / 100)
        toggle_off = toggle_rate - toggle_on
        power = random.randint(0, 1)
        toggle = [toggle_on, toggle_off]
        counter = 0
        for idx in range(len(notcher)):
            counter += 1
            notcher[idx] = power
            if counter > toggle[power]:
                counter = 0
                power = 1 if power == 0 else 0

    return notcher


def generate_signal():
    mod = Modulator()

    rate = 1 / 10 ** random.randint(1, 6)

    center = random.randint(160, 235) * 1000

    t = Transmission(Fs=1e6, fc=center, T=5, Td=rate)

    modulation_type = random.randint(1, 3)

    if modulation_type == 1:
        return mod.fsk(t), "fsk", rate

    elif modulation_type == 2:
        return mod.ask(t), "ask", rate

    elif modulation_type == 3:
        return mod.psk(t), "psk", rate


def create_box(x_start, y_start, x_end, y_end, shape):
    return {
        "x_0": x_start,
        "y_0": y_start,
        "w": x_end - x_start,
        "h": y_end - y_start,
        "x_1": x_end,
        "y_1": y_end,
        "shape": shape
    }


def annotate_spectrogram(spectrogram):
    s = spectrogram
    s = (s - s.min()) / (s.max() - s.min())
    s_map = s > s.mean() + s.std() * 3
    boxes = []
    idx = 0
    while idx < s_map.shape[0]:
        if s_map[idx,].max() != 0:
            vertical_start = idx
            while idx < s_map.shape[0]:
                if s_map[idx,].max() == 0:
                    break
                idx += 1
            vertical_end = idx - 1

            starts = []
            for idx in range(vertical_start, vertical_end + 1):
                count = 0
                for val in s_map[idx,]:
                    if val != 0:
                        break
                    count += 1
                starts.append(count)

            horiziontal_start = int(np.min(starts))

            ends = []
            for idx in range(vertical_start, vertical_end + 1):
                count = 0
                for val in s_map[idx,][::-1]:
                    if val != 0:
                        break
                    count += 1
                ends.append(count)

            horiziontal_end = s_map.shape[1] - int(np.min(ends))

            boxes.append(
                create_box(horiziontal_start, vertical_start, horiziontal_end, vertical_end, spectrogram.shape))
        idx += 1
    return boxes


def rescale_annotation(annotation, shape):
    new_height = shape[0]
    new_width = shape[1]

    old_height = annotation['shape'][0]
    old_width = annotation['shape'][1]

    x_start = annotation["x_0"]
    y_start = annotation["y_0"]
    x_end = annotation["x_1"]
    y_end = annotation["y_1"]

    x_start = x_start / old_width * new_width if x_start != 0 else 0
    y_start = y_start / old_height * new_height if y_start != 0 else 0
    x_end = x_end / old_height * new_height if x_end != 0 else 0
    y_end = y_end / old_height * new_height if y_end != 0 else 0

    return {
        "x_0": x_start,
        "y_0": y_start,
        "w": x_end - x_start,
        "h": y_end - y_start,
        "x_1": x_end,
        "y_1": y_end,
        "shape": shape
    }


def annotate(spectrogram, size, save_directory):
    save_name = create_name()

    new_height = size[0]
    new_width = size[1]

    annotations = annotate_spectrogram(spectrogram)

    annotations = [rescale_annotation(a, (new_height, new_width)) for a in annotations]

    spectrogram = (spectrogram - spectrogram.min()) / (spectrogram.max() - spectrogram.min())

    im = Image.fromarray(spectrogram * 255).convert('L').convert("RGB")
    im = im.resize((new_width, new_height), Image.Resampling.LANCZOS)

    im.save(os.path.join(save_directory, f"{save_name}.jpg"))

    im_draw = ImageDraw.Draw(im)
    for scaled in annotations:
        # scaled = rescale_annotation(an, (new_height, new_width))
        im_draw.rectangle((scaled['x_0'], scaled['y_0'], scaled['x_1'], scaled['y_1']), outline="red")

    im.save(os.path.join(save_directory, f"{save_name}_annotated.jpg"))

    with open(os.path.join(save_directory, f"{save_name}.json"), "w") as fout:
        json.dump(annotations, fout)


def create_name():
    hasher = hashlib.sha512()
    hasher.update(f"{datetime.now()} {random.randint(1, 100000)}".encode())
    return hasher.hexdigest()


def create_signals(max_signals):
    num_signals = random.randint(1, max_signals)

    if random.randint(1, 2) == 1:
        sigs, mod, rate = generate_signal()
        notcher = create_notcher(len(sigs))
        for idx in range(1, num_signals):
            sig, mod, rate = generate_signal()
            sigs += sig
        sigs *= notcher
        return sigs
    else:
        sigs, mod, rate = generate_signal()
        notcher = create_notcher(len(sigs))
        sigs *= notcher
        for idx in range(1, num_signals):
            sig, mod, rate = generate_signal()
            sig *= create_notcher(len(sig))
            sigs += sig
        return sigs
