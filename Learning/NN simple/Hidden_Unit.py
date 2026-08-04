import Neural_Net
import numpy as np

class Unit:
    def __init__(self, nn, index, af='Sigmoid'):
        self.NN = nn
        self.index = index
        self.af = af

        input_count = self.NN.get_prev_len(self.index)
        output_count = self.NN.layers[self.index]

        limit = np.sqrt(6 / (input_count + output_count))

        self.params = np.empty(input_count + 1)
        self.params[0] = 0.0  # bias
        self.params[1:] = self.NN.rng.uniform(
            -limit,
            limit,
            size=input_count
        )

    def update(self):
        previous_values = self.NN.get_prev_values(self.index)
        inputs = np.concatenate(([1.0], previous_values))
        self.z = float(np.dot(self.params, inputs))

        if self.af == 'Sigmoid':
            self.value = 1.0 / (1.0 + np.exp(-self.z))

        elif self.af == 'ReLU':
            self.value = max(0.0, self.z)

        else:
            raise ValueError(f"Unknown activation function: {self.af}")

        return self.value
