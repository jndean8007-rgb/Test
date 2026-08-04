import Neural_Net
import numpy as np

class Unit:
    def __init__(self, nn, index, af = 'Sigmoid'):
        self.NN =nn
        self.index = index
        self.af = af

        self.params = [0]
        self.z = 0
        self.value = 0

        for i in self.NN.get_prev_len(self.index):
            self.params.append(0)

    def update(self):
        ins = [1, self.NN.get_prev_values(self.index)]

        for i  in range(len(self.params)):
            self.z += self.params[i-1] * ins[i-1]

        if self.af == 'Sigmoid':
            self.value = np.exp(self.z) / (1 + np.exp(self.z))

        elif self.af == 'ReLU':
            self.value = np.max(0, self.z)

        return self.value

    def value(self):
        return self.value
