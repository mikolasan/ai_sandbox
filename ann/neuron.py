import uuid
import numpy as np
# from scheduler import Scheduler


class Sensor:
  def __init__(self, scheduler):
    self.connections = []
    self.input = None
    self.id = uuid.uuid4()
    self.scheduler = scheduler

  def set_input(self, input_pattern):
    self.input = input_pattern

  def activate(self, time):
    # if self.input > 0.5:
    for dendrite in self.connections:
      dendrite.activate(time, self.input)


class Dendrite:
  def __init__(self, neuron, strength=0):
    self.neuron = neuron
    self.strength = strength

  def activate(self, time, _input):
    if self.strength > 0.5:
      print(f"Dendrite({self.strength}) time {time}")
      self.neuron.record_input(time, _input)
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
        dendrite.activate(time, output)
  
  def plasticity_on(self):
    return self.neuron.plasticity_on


class Neuron:
  def __init__(self, scheduler):
    self.dendrites = []
    self.axon = Axon(self)
    self.plasticity_on = False
    self.inputs = {}
    self.id = uuid.uuid4()
    self.transform_fn = sum
    self.scheduler = scheduler

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

  def record_input(self, time, _input):
    if time not in self.inputs:
      self.inputs[time] = [_input]
    else:
      self.inputs[time].append(_input)
    self.scheduler.add(time, self.activate)

  def activate(self, time):
    output = self.transform_fn(self.inputs[time])
    print(f"Neuron({self.id}) time {time}: output {output}")
    del self.inputs[time]
    self.axon.activate(time + 1, output)


class MultiplyingNeuron(Neuron):
  def __init__(self, scheduler, multiplier):
    super().__init__(scheduler)
    self.transform_fn = lambda x: x[0] * multiplier


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
