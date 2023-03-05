"""
Original code:
https://github.com/ardendertat/Applied-Deep-Learning-with-Keras/blob/master/notebooks/Part%201%20-%20Artificial%20Neural%20Networks.ipynb

Visualization similar to one from here:
https://towardsdatascience.com/how-neural-networks-solve-the-xor-problem-59763136bdd7
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

# train

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
Y = np.array([0, 1, 1, 0])

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(2, input_shape=(2,), activation='sigmoid'))
model.add(tf.keras.layers.Dense(1, activation='linear'))
optimizer = tf.keras.optimizers.experimental.SGD(
    learning_rate=0.2,
    momentum=0.0,
    nesterov=True,
    amsgrad=False)
#optimizer = tf.keras.optimizers.experimental.RMSprop(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='mse', metrics=['accuracy'])

N = 1000
history = model.fit(X, Y, verbose=0, epochs=N)

xdata = history.epoch
loss = history.history['loss']
acc = history.history['accuracy']

fig, ax1 = plt.subplots()
ax1.set_xlabel('epochs')
ax1.set_ylabel('accuracy', color='tab:blue')
ax1.plot(xdata, acc, color='tab:blue')
ax2 = ax1.twinx()
ax2.set_ylabel('loss', color='tab:red')
ax2.plot(xdata, loss, color='tab:red')

plt.show()

# use the model

# test key points
print([model.predict(np.array([[0,0]])),
model.predict(np.array([[1,0]])),
model.predict(np.array([[0,1]])),
model.predict(np.array([[1,1]]))])

print(model.weights)

x_range = np.linspace(-2, 2, 30)
y_range = np.linspace(-2, 2, 30)
xx, yy = np.meshgrid(x_range, y_range, indexing='ij')
zz = [model.predict(np.array([[xx[i][j], yy[i,j]] for i in range(30)]), verbose=0).flatten() for j in range(30)]
z = np.array(zz)

plt.figure(figsize=(20, 20))
plt.axis('scaled')
plt.xlim(-2, 2)
plt.ylim(-2, 2)
colors = {0: "wo", 1: "ko"}
# plotting the four datapoints
for i in range(len(X)):
    plt.plot(X[i][0], X[i][1], colors[int(Y[i])], markersize=20)

plt.contourf(xx, yy, z, alpha=0.4)
plt.show()