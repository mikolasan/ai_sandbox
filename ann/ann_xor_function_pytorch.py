"""
Original code:
https://courses.cs.washington.edu/courses/cse446/18wi/sections/section8/XOR-Pytorch.html

Another reference from:
https://medium.com/mlearning-ai/learning-xor-with-pytorch-c1c11d67ba8e
https://colab.research.google.com/drive/1sKJfB5YAfAUD9PU-SNDGlMdKa9M7yCcH?usp=sharing

Made it work in Python 3, PyTorch 1.11
"""

import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

# for reproducible results
# torch.manual_seed(2)
# np.random.seed(2)

X = torch.Tensor([[0,0], [0,1], [1,0], [1,1]])
Y = torch.Tensor([0, 1, 1, 0]).view(-1,1)


class XOR(nn.Module):
    def __init__(self, input_dim = 2, output_dim=1):
        super(XOR, self).__init__()
        self.linear1 = nn.Linear(input_dim, 2)
        self.linear2 = nn.Linear(2, output_dim)
    
    def forward(self, x):
        x = self.linear1(x)
        x = torch.sigmoid(x)
        x = self.linear2(x)
        return x


model = XOR()
mseloss = nn.MSELoss() # mean squared error
optimizer = torch.optim.SGD(model.parameters(), lr=0.2, momentum=0.0)
# optimizer = torch.optim.Adam(model.parameters(), lr=0.03)
N = 1000
loss_values = []
accuracy_values = []
model.train()
for i in range(N):
    y_hat = model.forward(X)
    loss = mseloss(y_hat, Y)
    loss.backward()
    optimizer.step() # update model weights
    optimizer.zero_grad() # remove current gradients for next iteration

    loss_values.append(loss.item())
    with torch.no_grad():
        z = model.forward(X)
        pred = z.round().int() == Y
        accuracy = pred.sum().item()
        accuracy_values.append(accuracy / len(X))


xdata = np.arange(0, N, 1)

fig, ax1 = plt.subplots()
ax1.set_xlabel('epochs')
ax1.set_ylabel('accuracy', color='tab:blue')
ax1.plot(xdata, accuracy_values, color='tab:blue')
ax2 = ax1.twinx()
ax2.set_ylabel('loss', color='tab:red')
ax2.plot(xdata, loss_values, color='tab:red')

plt.show()

# use the model

model.eval()
with torch.no_grad():
    a = model.forward(X)
print(a)

model_params = list(model.parameters()) # returns weights and biases
model_weights = model_params[0].data.numpy()
print(f' Model weights: {model_weights}')
model_bias = model_params[1].data.numpy()
print(f' Model bias: {model_bias}')
# model_weights = model_params[2].data.numpy()
# print(f' Model weights: {model_weights}')
# model_bias = model_params[3].data.numpy()
# print(f' Model bias: {model_bias}')

# plt.scatter(X.numpy()[[0,-1], 0], X.numpy()[[0, -1], 1], s=50)
# plt.scatter(X.numpy()[[1,2], 0], X.numpy()[[1, 2], 1], c='red', s=50)


x_range = np.linspace(-2, 2, 30)
y_range = np.linspace(-2, 2, 30)
xx, yy = np.meshgrid(x_range, y_range, indexing='ij')
zz = [model.forward(torch.Tensor([[xx[i][j], yy[i,j]] for i in range(30)])).detach().cpu().numpy().flatten() for j in range(30)]
z = np.array(zz)
plt.figure(figsize=(20, 20))
plt.axis('scaled')
plt.xlim(-2, 2)
plt.ylim(-2, 2)
colors = {0: "wo", 1: "ko"}
# plotting the four datapoints
for i in range(len(X)):
    plt.plot(X[i][0], X[i][1], colors[int(Y[i][0])], markersize=20)

# using the contourf function to create the plot
plt.contourf(xx, yy, z, alpha=0.4)
plt.show()