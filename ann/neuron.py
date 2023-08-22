import uuid
import numpy as np


class Sensor:
  def __init__(self):
    self.connections = []
    self.input = None
    self.id = uuid.uuid4()

  def set_input(self, input_pattern):
    self.input = input_pattern

  def activate(self, time):
    print(f"Sensor({self.id}) time {time}")
    # if self.input > 0.5:
    for dendrite in self.connections:
      dendrite.activate(time, self.input)


class Dendrite:
  def __init__(self, neuron, strength=0):
    self.neuron = neuron
    self.strength = strength

  def activate(self, time, input):
    if self.strength > 0.5:
      print(f"Dendrite({self.strength}) time {time}")
      self.neuron.record_signal(time, input)
      self.strength += 0.1
  
  def plasticity_on(self):
    return self.neuron.plasticity_on


class Axon:
  def __init__(self, neuron):
    self.neuron = neuron
    self.connections = {}

  def add_dendrite(self, neuron, dendrite):
    if neuron not in self.connections:
      self.connections[neuron.id] = []
    self.connections[neuron.id].append(dendrite)

  def activate(self, time, output):
    for connections in self.connections.values():
      for dendrite in connections:
        dendrite.activate(time)
  
  def plasticity_on(self):
    return self.neuron.plasticity_on


class Neuron:
  def __init__(self):
    self.dendrites = []
    self.axon = Axon(self)
    self.plasticity_on = False
    self.inputs = {}
    self.id = uuid.uuid4()
    self.transform_fn = sum

  def add_connection(self, neuron, strength=None):
    dendrite = Dendrite(self, strength=(strength or np.random.uniform()))
    # add connections to pre-synaptic neuron
    neuron.axon.add_dendrite(self, dendrite)
    # add connections to post-synaptic neuron (this)
    self.dendrites.append(dendrite)

  def add_input(self, sensor):
    dendrite = Dendrite(self, strength=1.0)
    # pre-synaptic part
    sensor.connections.append(dendrite)
    # add connections to post-synaptic neuron (this)
    self.dendrites.append(dendrite)

  def record_input(self, time, input):
    if time not in self.inputs:
      self.inputs[time] = [input]
    else:
      self.inputs[time].append(input)

  def activate(self, time):
    print(f"Neuron({self.id}) time {time}")
    output = self.transform_fn(self.inputs[time])
    self.axon.activate(time, output)


def print_conections(connections, prefix):
  for dendrite in connections:
    connection_type = "strong" if dendrite.strength > 0.5 else "weak"
    prefix += f"-[{connection_type} {dendrite.strength}]- neuron({dendrite.neuron.id})"
    if len(dendrite.neuron.axon.connections) > 0:
      for neuron, dendrites in dendrite.neuron.axon.connections.items():
        print_conections(dendrites, prefix + "->")
    else:
      print(prefix)

def print_network(sensors):
  print("Network:")
  for i, s in enumerate(sensors):
    print_conections(s.connections, f"sensor({s.id}) ")
