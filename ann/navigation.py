from keras.utils.np_utils import to_categorical
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

max_0 = 360
max_1 = 250
max_2 = 270


class Navigation:
    def __init__(self):
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                print(gpus[0])
                # Currently, memory growth needs to be the same across GPUs
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                logical_gpus = tf.config.experimental.list_logical_devices(
                    'GPU')
                print(len(gpus), "Physical GPUs,", len(logical_gpus),
                      "Logical GPUs")
            except RuntimeError as e:
                # Memory growth must be set before GPUs have been initialized
                print(e)

    def _prepare_raw_data(self, x):
        return x / np.array([max_0, max_1])
    
    def read_train_data(self):
        train_data = np.genfromtxt('nav_robot_train.csv', delimiter=',')

        y = np.delete(train_data, [0,1], 1)
        y_max = np.array([90])
        y = (y + 90) / y_max
        
        x = np.delete(train_data, 2, 1)
        x = x / np.array([180, max_1]) * np.array([np.pi, 1])

        return x, y
    
    def read_test_data(self):
        test_data = np.genfromtxt('nav_robot_test.csv', delimiter=',')
        # test_data
        eval_x = np.delete(test_data, 2, 1)
        # eval_x = eval_x / x_max
        # eval_x[:10]
        eval_y = np.delete(test_data, [0,1], 1)
        y_max = np.array([90])
        eval_y = (eval_y + 90) / y_max
        # eval_y[:10]
        
    def plot_data(self, x, y):
        fig = plt.figure(figsize=(5,5))
        ax = fig.add_subplot(projection='polar')

        categories = np.unique(y)
        colors = np.linspace(0,1,len(categories))
        colordict = dict(zip(categories, colors))
        color_map = list(map(lambda x: colordict[x], y.flatten().tolist()))

        ax.scatter(x[:, 0], x[:, 1], c=color_map)
        ax.set_rticks([0.25, 0.5, 0.75, 1.0])  # Less radial ticks
        ax.grid(True)
        ax.set_title("5x5 grid world and first move data")
        plt.show()

        
        fig = plt.figure(figsize=(7,7))
        ax = fig.add_subplot()

        ax.scatter(x[:, 0], x[:, 1], c=color_map)
        ax.grid(True)
        ax.set_xlabel('head rotation')
        ax.set_ylabel('approx distance')
        ax.set_title("5x5 grid world and first move data")
        plt.show()
        
    def train(self, x, y):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(32, input_shape=(2,), activation='tanh'))
        model.add(tf.keras.layers.Dense(16, activation='tanh'))
        model.add(tf.keras.layers.Dense(8, activation='tanh'))
        model.add(tf.keras.layers.Dense(4, activation='softmax'))
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy'])
        
        self.model = model
        N=500
        y_cat = to_categorical(y, num_classes=4)
        # np.concatenate([y,y_cat], 1)[:60]
        # y_cat[:60]

        history = model.fit(x / np.array([2 * np.pi, 1]), y_cat, verbose=0, epochs=N)
        self.history = history
        # model.weights
        return history

    def plot_accurancy(self, history):
        loss = history.history['loss']
        acc = history.history['accuracy']
        xdata = history.epoch

        fig, ax1 = plt.subplots()
        ax1.set_xlabel('epochs')
        ax1.set_ylabel('accuracy', color='tab:blue')
        ax1.plot(xdata, acc, color='tab:blue')
        ax2 = ax1.twinx()
        ax2.set_ylabel('loss', color='tab:red')
        ax2.plot(xdata, loss, color='tab:red')
        plt.show()        

    def plot_prediction(self):
        x_ticks = 100
        x_range = np.linspace(0, 1, x_ticks)
        y_ticks = 100
        y_range = np.linspace(0, 1, y_ticks)
        xx, yy = np.meshgrid(x_range, y_range, indexing='ij')
        zz = [np.argmax(self.model.predict(np.array([[xx[i][j], yy[i,j]] for i in range(x_ticks)]), verbose=0), axis=-1).flatten() for j in range(y_ticks)]
        z = np.transpose(np.array(zz))
        # z

        plt.figure(figsize=(10,10))
        # plt.axis('scaled')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.contourf(xx, yy, z, alpha=0.4)
        plt.show()

    def load(self, path):
        self.model = tf.keras.models.load_model(path)

    def save(self, path):
        self.model.save(path)
        
    def train_fresh(self):
        x, y = self.read_train_data()
        self.plot_data(x, y)
        history = self.train(x, y)
        self.plot_accurancy(history)
        self.plot_prediction() # uses self.model internally
        # self.save('navigation.1.model')
    
    # prediction = model.predict(eval_x)
    # prediction[:5]
    # np.concatenate([prediction[:10], eval_y[:10]], 1)
    # p = np.argmax(prediction, axis=-1)
    # np.concatenate([p[..., None], eval_y], 1)[:30]
    
    def predict(self, x):
        a = self._prepare_raw_data(x)
        p = self.model.predict(a)
        return np.argmax(p, axis=-1)