from enum import Enum


class Label(Enum):
    TRANSMISSION = 0
    ASK = 1
    PSK = 2
    FSK = 3
    MFSK = 4
    TONE = 5


def color(value):
    code = Label(value)
    if code == Label.TRANSMISSION:
        return "red"
    elif code == Label.ASK:
        return "black"
    elif code == Label.PSK:
        return "green"
    elif code == Label.FSK:
        return "blue"
    elif code == Label.MFSK:
        return "cyan"
    elif code == Label.TONE:
        return "black"
    return "white"
