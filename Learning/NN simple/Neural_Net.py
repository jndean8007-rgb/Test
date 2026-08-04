import numpy as np
import Hidden_Unit
import Output
from sklearn.preprocessing import StandardScaler

class Neuralnet:
    def __init__(self, data, target, layers, sgd_spec, output_type = "Quant"):
        self.data = np.asarray(data, dtype=float)
        scaler = StandardScaler()
        self.data_standard = scaler.fit_transform(self.data)
        self.target = np.asarray(target, dtype=float)
        self.layers = tuple(layers)
        self.epochs = sgd_spec[0]
        self.minibatch = sgd_spec[1]
        self.learn_rate = sgd_spec[2]

        self.form = []
        self.rng = np.random.default_rng(42)
        self.output_type = output_type

        if self.data.ndim != 2:
            raise ValueError("data must be a two-dimensional array")
        if len(self.target) != len(self.data):
            raise ValueError("data and target must contain the same number of rows")
        if not self.layers or any(width <= 0 for width in self.layers):
            raise ValueError("layers must contain positive layer widths")

        self.input_size = self.data.shape[1]
        self.input = np.zeros(self.input_size, dtype=float)

        for i, width in enumerate(self.layers):
            temp = []
            for _ in range(width):
                temp.append(Hidden_Unit.Unit(self, i, 'Sigmoid'))
            self.form.append(temp)

        self.output = Output.Output(self, self.output_type)

        # Training will be added once SGD/backpropagation is implemented.
        for i in range(self.epochs):
            self.train(self.minibatch)

    def get_prev_values(self, index):
        if index == 0:
            return self.input
        return np.array([unit.value for unit in self.form[index - 1]], dtype=float)

    def get_prev_len(self, index):
        if index == 0:
            return self.input_size
        return len(self.form[index - 1])

    def __len__(self):
        return len(self.form)

    #def train(self, minibatch):
        #MSE loss sum (output - predict)^2
        #if self.output_type == "Quant":

        #else:


    def predict(self, input_values):
        scaler = StandardScaler()
        self.input = scaler.fit_transform(np.asarray(input_values, dtype=float))
        if self.input.ndim != 1 or len(self.input) != self.input_size:
            raise ValueError(
                f"predict expects one row containing {self.input_size} values"
            )

        for layer in self.form:
            for unit in layer:
                unit.update()

        return self.output.update()