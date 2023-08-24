import uuid
import numpy as np
# from scheduler import Scheduler


class Sensor:
  def __init__(self, name, scheduler):
    self.connections = []
    self.input = None
    self.input_sequence = None
    self.name = name
    self._id = uuid.uuid4()
    self.scheduler = scheduler

  def set_input(self, input_pattern):
    self.input = input_pattern
    
  def set_input_sequence(self, input_sequence):
    self.input_sequence = input_sequence

  def activate(self, time):
    # if self.input > 0.5:
    if time in self.input_sequence:
      print(f"Sensor({self.name}) time {time}")
      for dendrite in self.connections:
        dendrite.activate(time, self.input_sequence[time])


class Dendrite:
  def __init__(self, neuron, strength=0):
    self.neuron = neuron
    self.strength = strength

  def activate(self, time, _input):
    if self.strength > 0.5:
      print(f"{{time {time}}} ->({self.neuron.name}) {_input}")
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
      self.connections[neuron._id] = []
    self.connections[neuron._id].append(dendrite)

  def activate(self, time, output):
    for connections in self.connections.values():
      for dendrite in connections:
        dendrite.activate(time, output)
  
  def plasticity_on(self):
    return self.neuron.plasticity_on


class Neuron:
  def __init__(self, name, scheduler, activation_delay=0):
    self.dendrites = []
    self.axon = Axon(self)
    self.plasticity_on = False
    self.inputs = {}
    self.name = name
    self._id = uuid.uuid4()
    self.transform_fn = sum
    self.scheduler = scheduler
    self.activation_delay = activation_delay

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
    activation_time = time + self.activation_delay
    if activation_time not in self.inputs:
      self.inputs[activation_time] = [_input]
    else:
      self.inputs[activation_time].append(_input)
    self.scheduler.add(activation_time, self)

  def activate(self, time):
    output = self.transform_fn(self.inputs[time])
    print(f"{{time {time}}} Neuron({self.name}) output -> {output}")
    del self.inputs[time]
    self.axon.activate(time + 1, output)


class MultiplyingNeuron(Neuron):
  def __init__(self, name, scheduler, multiplier, activation_delay=0):
    super().__init__(name, scheduler, activation_delay)
    self.transform_fn = lambda x: x[0] * multiplier


class RegisterNeuron(Neuron):
  """
  Register neurons will store the input and output it only when the new input arrives
  First time it outputs 0
  """
  def __init__(self, name, scheduler):
    super().__init__(name, scheduler)
    self.memory = None
    # self.transform_fn = None

  def record_input(self, time, _input):
    if self.memory:
      self.inputs[time] = self.memory
    self.memory = _input
    self.scheduler.add(time, self)

  def activate(self, time):
    if time not in self.inputs:
      output = 0
    else:
      output = self.inputs[time]
      del self.inputs[time]
    print(f"{{time {time}}} Neuron({self.name}) output -> {output}")
    self.axon.activate(time + 1, output)


class InhibitionNeuron(Neuron):
  """
  First stimulus defines if all following inputs will be ignored
  If the first stimulus is 0, then inhibition is on
  """
  def __init__(self, name, scheduler, activation_delay=0):
    super().__init__(name, scheduler, activation_delay)
    self.inhibition = False

  def record_input(self, time, _input):
    activation_time = time + self.activation_delay
    if abs(_input - 0.0) < 1e-6:
      self.inhibition = True
      self.inputs[activation_time] = [0]
    else:
      self.inhibition = False
      if activation_time not in self.inputs:
        self.inputs[activation_time] = [_input]
      else:
        self.inputs[activation_time].append(_input)
    self.scheduler.add(activation_time, self)
    
  def activate(self, time):
    _input = self.inputs[time]
    if _input
    output = self.transform_fn()
    print(f"{{time {time}}} Neuron({self.name}) output -> {output}")
    del self.inputs[time]
    self.axon.activate(time + 1, output)
    
    return super().activate(time)


def print_conections(connections, prefix):
  for dendrite in connections:
    connection_type = "strong" if dendrite.strength > 0.5 else "weak"
    prefix += f"-[{connection_type} {dendrite.strength}]- neuron({dendrite.neuron._id})"
    if len(dendrite.neuron.axon.connections) > 0:
      for neuron, dendrites in dendrite.neuron.axon.connections.items():
        print_conections(dendrites, prefix + "->")
    else:
      print(prefix)

def print_network(sensors):
  print("Network:")
  for i, s in enumerate(sensors):
    print_conections(s.connections, f"sensor({s._id}) ")
