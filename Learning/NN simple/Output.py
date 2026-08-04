import numpy as np

class Output:
    def __init__(self, nn, output_type = 'Quant'):
        self.NN = nn
        self.type = output_type
        self.params = np.zeros(len(self.NN.form[-1]) + 1, dtype=float)
        self.z = 0.0
        self.value = 0.0

    def update(self):
        previous_values = np.array(
            [unit.value for unit in self.NN.form[-1]], dtype=float
        )
        inputs = np.concatenate(([1.0], previous_values))
        self.z = float(np.dot(self.params, inputs))

        if self.type == 'Quant':
            # Linear output for a quantitative regression target.
            self.value = self.z

        elif self.type == 'Binary':
            self.value = 1.0 / (1.0 + np.exp(-self.z))

        else:
            raise ValueError(f"Unknown network type: {self.type}")

        return self.value