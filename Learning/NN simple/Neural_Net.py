import numpy as np
import Hidden_Unit
import Output
from sklearn.preprocessing import StandardScaler

class Neuralnet:
    def __init__(self, data, target, layers, sgd_spec, output_type = "Quant", random_state=42):
        self.data = np.asarray(data, dtype=float)
        self.target = np.asarray(target, dtype=float)

        self.layers = tuple(layers)
        self.epochs = int(sgd_spec[0])
        self.minibatch = int(sgd_spec[1])
        self.learn_rate = float(sgd_spec[2])


        self.rng = np.random.default_rng(random_state)
        self.output_type = output_type
        self.form = []
        self.loss_history = []

        if self.data.ndim != 2:
            raise ValueError("data must be a two-dimensional array")

        if len(self.target) != len(self.data):
            raise ValueError("data and target must contain the same number of rows")

        if not self.layers or any(width <= 0 for width in self.layers):
            raise ValueError("layers must contain positive layer widths")

        if self.minibatch <= 0:
            raise ValueError("minibatch size must be positive")

        if self.learn_rate <= 0:
            raise ValueError("learning rate must be positive")

        self.scaler = StandardScaler()
        self.data_standard = self.scaler.fit_transform(self.data)

        self.input_size = self.data.shape[1]
        self.input = np.zeros(self.input_size, dtype=float)

        for layer_index, width in enumerate(self.layers):
            layer = []

            for _ in range(width):
                layer.append(Hidden_Unit.Unit(self, layer_index, 'Sigmoid'))
            self.form.append(layer)

        self.output = Output.Output(self, self.output_type)

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

    def _forward_standardized(self, input_values):
        #forward pass for standardized input
        self.input = np.asarray(input_values, dtype=float)

        if self.input.ndim != 1 or len(self.input) != self.input_size:
            raise ValueError(
                f"Expected one row containing {self.input_size} values"
            )

        for layer in self.form:
            for unit in layer:
                unit.update()

        return self.output.update()
    def predict(self, input_values):
        row = np.asarray(input_values, dtype=float)

        if row.ndim != 1 or len(row) != self.input_size:
            raise ValueError(
                f"predict expects one row containing "
                f"{self.input_size} values"
            )

        standardized_row = self.scaler.transform(
            row.reshape(1, -1)
        )[0]

        return self._forward_standardized(standardized_row)

    def predict_many(self, input_values):
        data = np.asarray(input_values, dtype=float)

        if data.ndim != 2 or data.shape[1] != self.input_size:
            raise ValueError(
                f"predict_many expects an array with "
                f"{self.input_size} columns"
            )

        standardized_data = self.scaler.transform(data)

        return np.array(
            [
                self._forward_standardized(row)
                for row in standardized_data
            ],
            dtype=float
        )

    def _calculate_deltas(self, target):

        prediction = self.output.value

        if self.output_type == "Quant":
            self.output.delta = prediction - target

        elif self.output_type == "Binary":
            self.output.delta = prediction - target

        else:
            raise ValueError(
                f"Unknown output type: {self.output_type}"
            )

        # Work backwards through the hidden layers.
        for layer_index in range(len(self.form) - 1, -1, -1):
            current_layer = self.form[layer_index]

            for unit_index, unit in enumerate(current_layer):

                if layer_index == len(self.form) - 1:
                    # Last hidden layer connects directly to output.
                    #
                    # params[0] is bias, so params[unit_index + 1]
                    # is the weight from this hidden unit.
                    downstream_error = (
                            self.output.params[unit_index + 1]
                            * self.output.delta
                    )

                else:
                    next_layer = self.form[layer_index + 1]

                    downstream_error = 0.0

                    for next_unit in next_layer:
                        # Weight connecting current unit to next_unit.
                        connecting_weight = (
                            next_unit.params[unit_index + 1]
                        )

                        downstream_error += (
                                connecting_weight * next_unit.delta
                        )

                unit.delta = (
                        unit.activation_derivative()
                        * downstream_error
                )

    def _empty_gradients(self):
        hidden_gradients = []

        for layer in self.form:
            layer_gradients = []

            for unit in layer:
                layer_gradients.append(
                    np.zeros_like(unit.params)
                )

            hidden_gradients.append(layer_gradients)

        output_gradient = np.zeros_like(self.output.params)

        return hidden_gradients, output_gradient

    def _accumulate_gradients(
            self,
            hidden_gradients,
            output_gradient
    ):
        """
        Add the current observation's gradients to the minibatch totals.
        """

        # Output gradient:
        # dL/dw = delta * input_to_weight
        output_inputs = np.concatenate(
            (
                [1.0],
                [
                    unit.value
                    for unit in self.form[-1]
                ]
            )
        )

        output_gradient += (
                self.output.delta * output_inputs
        )

        # Hidden-unit gradients.
        for layer_index, layer in enumerate(self.form):
            previous_values = self.get_prev_values(layer_index)

            unit_inputs = np.concatenate(
                ([1.0], previous_values)
            )

            for unit_index, unit in enumerate(layer):
                hidden_gradients[layer_index][unit_index] += (
                        unit.delta * unit_inputs
                )

    def _apply_gradients(
            self,
            hidden_gradients,
            output_gradient,
            batch_size
    ):
        """
        Apply the average minibatch gradient.
        """
        scale = self.learn_rate / batch_size

        for layer_index, layer in enumerate(self.form):
            for unit_index, unit in enumerate(layer):
                unit.params -= (
                        scale
                        * hidden_gradients[layer_index][unit_index]
                )

        self.output.params -= scale * output_gradient

    def train_batch(self, batch_indices):
        """
        Train on one minibatch and return its average loss.
        """
        hidden_gradients, output_gradient = (
            self._empty_gradients()
        )

        total_loss = 0.0

        for index in batch_indices:
            x = self.data_standard[index]
            y = self.target[index]

            prediction = self._forward_standardized(x)

            if self.output_type == "Quant":
                total_loss += 0.5 * (prediction - y) ** 2

            elif self.output_type == "Binary":
                epsilon = 1e-12
                clipped = np.clip(
                    prediction,
                    epsilon,
                    1.0 - epsilon
                )

                total_loss += -(
                        y * np.log(clipped)
                        + (1.0 - y) * np.log(1.0 - clipped)
                )

            self._calculate_deltas(y)

            self._accumulate_gradients(
                hidden_gradients,
                output_gradient
            )

        batch_size = len(batch_indices)

        self._apply_gradients(
            hidden_gradients,
            output_gradient,
            batch_size
        )

        return total_loss / batch_size

    def train(self, verbose=True):
        """
        Run minibatch SGD for all epochs.
        """
        sample_count = len(self.data_standard)

        for epoch in range(self.epochs):
            shuffled_indices = self.rng.permutation(sample_count)

            epoch_loss = 0.0
            observations_seen = 0

            for start in range(
                    0,
                    sample_count,
                    self.minibatch
            ):
                batch_indices = shuffled_indices[
                    start:start + self.minibatch
                ]

                batch_loss = self.train_batch(batch_indices)

                epoch_loss += batch_loss * len(batch_indices)
                observations_seen += len(batch_indices)

            epoch_loss /= observations_seen
            self.loss_history.append(epoch_loss)

            if verbose:
                print(
                    f"Epoch {epoch + 1:>3}/{self.epochs}: "
                    f"loss = {epoch_loss:.6f}"
                )