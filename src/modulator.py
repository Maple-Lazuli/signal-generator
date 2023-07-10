import numpy as np


class Modulator:
    def ask(self, trans):
        carrier = np.sin(2 * np.pi * trans.fc * trans.t)

        return carrier * trans.message

    def fsk(self, trans):
        f = trans.fc + trans.fc * trans.message / 2

        return np.sin(2 * np.pi * f * trans.t)

    def psk(self, trans):
        phase = np.pi + np.pi * trans.message / 2

        return np.sin(2 * np.pi * trans.fc * trans.t + phase)
