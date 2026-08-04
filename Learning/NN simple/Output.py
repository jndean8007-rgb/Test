import numpy as np

class Output:
    def __init__(self, nn, af = 'Sigmoid', type = 'Quant'):
        self.NN = nn
        self.type = type
        self.af = af
        self.params = [0]
        self.z = 0
        self.value = 0

        for i in self.NN.get_prev_len(len(self.NN)-1):
            self.params.append(0)

    def reg_value(self):
        ins = [1, self.NN.get_prev_values(len(self.NN)-1)]

        for i in range(len(self.params)):
            self.z += self.params[i - 1] * ins[i - 1]

        if self.af == 'Sigmoid':
            self.value = np.exp(self.z) / (1 + np.exp(self.z))

        elif self.af == 'ReLU':
            self.value = np.max(0, self.z)

        return self.value