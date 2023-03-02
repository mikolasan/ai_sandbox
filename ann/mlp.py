"""
Multi layer perceptron = MLP
"""

import numpy as np

def sigmoid(x):
  return 1 / (1 + np.exp(-1 * x))


def relu(x):
  return max(0, x)


class MLP(object):
  epochs = 3000
  learning_rate = 0.1
  
  def __init__(self, inputs, outputs, layer_sizes):
    self.data_inputs = inputs
    self.data_outputs = outputs
    self.n_neurons_per_layer = layer_sizes

    self.weights_1 = np.random.randn(self.n_neurons_per_layer[0], self.n_neurons_per_layer[1]) * 0.1
    self.weights_2 = np.random.randn(self.n_neurons_per_layer[1], self.n_neurons_per_layer[2]) * 0.1

    self.bias_1 = np.zeros((1, self.n_neurons_per_layer[1]))
    self.bias_2 = np.zeros((1, self.n_neurons_per_layer[2]))

  def learn(self):
    print("Learning started >>>>>>")
    for i in range(self.epochs):
      print("Itreation ", i)
      n_training_steps = self.data_inputs.shape[0]
      for idx in range(n_training_steps):
        x = self.data_inputs[idx, :]
        y = self.data_outputs[idx] # scalar
        
        x = x[:, np.newaxis].T # column vector
        # first hidden layer
        y_1 = np.dot(x, self.weights_1) + self.bias_1 # why x is first? (bias - column vector)
        y_1 = sigmoid(y_1) # column vector
        # output
        y_2 = np.dot(y_1, self.weights_2) + self.bias_2 # column vector (just one row)
        y_2 = relu(y_2)
        
        diff = y - y_2 # 1 element matrix (column vector)
        grad_2 = 1 # y_2 * (1 - y_2) # sigmoid derivative
        d_2 = diff * grad_2 # 1 element matrix (column vector)
        dw2 = y_1.T.dot(d_2)
        self.weights_2 += self.learning_rate * dw2
        self.bias_2 += self.learning_rate * d_2
        
        grad_1 = y_1 * (1 - y_1) # sigmoid derivative
        d_1 = (self.weights_2.T * d_2) * grad_1
        dw1 = x.T.dot(d_1)
        self.weights_1 += self.learning_rate * dw1
        self.bias_1 += self.learning_rate * d_1
        
        print('weights 1', self.weights_1)
        print('bias 1', self.bias_1)
        print('weights 2', self.weights_2)
        print('bias 2', self.bias_2)

  def forward(self, x):
    y_1 = np.dot(x, self.weights_1) + self.bias_1
    y_1 = sigmoid(y_1)
    y_2 = np.dot(y_1, self.weights_2) + self.bias_2
    y_2 = relu(y_2)
    if isinstance(y_2, np.ndarray):
      y_2 = y_2.item()
    return y_2

if __name__ == "__main__":
  mlp = MLP(
    inputs=np.array([[0, 0], [0, 1], [1, 0], [1, 1]]),
    outputs=np.array([0, 1, 1, 0]),
    layer_sizes=[2, 2, 1])
  mlp.learn()