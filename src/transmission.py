from dataclasses import dataclass
import numpy as np


@dataclass
class Transmission:
    Fs: int = 1e6
    fc: int = 100e2
    T: int = 5
    Td: float = 0.01

    def __post_init__(self):
        self.t = np.arange(0, self.T, 1 / self.Fs)
        self.n_samples = int(self.Td * self.Fs) if int(self.Td * self.Fs) != 0 else 1
        try:
            self.n_sym = int(np.floor(np.size(self.t) / self.n_samples))
        except:
            print("Error")
            print(f"self.Td:{self.Td}, self.Fs:{self.Fs}, n_samples {self.n_samples}")
        self.message = self.gen_message()

    def gen_message(self):
        rand_n = np.random.rand(self.n_sym)
        rand_n[np.where(rand_n >= 0.5)] = 1
        rand_n[np.where(rand_n <= 0.5)] = 0

        sig = np.zeros(int(self.n_sym * self.n_samples))

        # generating symbols
        id1 = np.where(rand_n == 1)
        for i in id1[0]:
            temp = int(i * self.n_samples)
            sig[temp:temp + self.n_samples] = 1
        return sig
