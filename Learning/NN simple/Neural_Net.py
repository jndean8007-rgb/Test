import numpy as np
import Hidden_Unit
import Output

class Neuralnet:
    def __init__(self, data, layers, sgd, type = "Quant"):
        self.data = data
        self.layers = layers
        self.epochs = sgd[0]
        self.minibatch = sgd[1]
        self.form = []
        self.input = []
        self.type = type
        self.output = Output.Output(self, self.type)


        for i in range(len(layers)):
            temp = []
            for j in range(layers[i]):
                temp.append(Hidden_Unit.Unit(self, i, 'Sigmoid'))
            self.form.append(temp)

        for i in range(self.epochs):
            self.train(self.minibatch)

    def get_prev_values(self, index):
        if index == 0:
            return self.input
        else:
            return (unit.value() for unit in self.form[index - 1])

    def get_prev_len(self, index):
        if index == 0:
            return len(self.input)
        else:
            return len(self.form[index-1])

    def __len__(self):
        return len(self.form)

    #def train(self, minibatch):


    def predict(self, input):
        self.input = input

        for i in self.form:
            for j in i:
                self.form[i][j].update()

        return self.output.reg_value