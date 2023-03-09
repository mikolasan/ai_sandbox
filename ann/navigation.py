from tensorflow import keras

class Navigation:
  def __init__(self):
    self.model = keras.models.load_model('navigation.1.model')
