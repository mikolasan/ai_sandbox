"""
hebbian_neuron

Program that simulates two artificial neurons and contains the main function 
to train connections with Hebbian rule. 
Each neuron is a class and has a list of dendrites and one axon. 
Connections defined by two strengths: strong and weak. 
It's not a fully connected network, so connections can be absent. 
Every axon can inhibit or actuate a dendrite which it is connected to. 

TODO: test on cartpole environment
https://gymnasium.farama.org/environments/classic_control/cart_pole/
"""

import uuid
import numpy as np


class Dendrite:
  def __init__(self, neuron, strength=0):
    self.neuron = neuron
    self.strength = strength

  def activate(self, time=0):
    if self.strength > 0.5:
      self.neuron.activate(time)
      self.strength += 0.1


class Sensor:
  def __init__(self):
    self.connections = []
    self.input = None

  def set_input(self, input_pattern):
    self.input = input_pattern

  def activate(self):
    if self.input > 0.5:
      for dendrite in self.connections:
        dendrite.activate(0.0)


class Axon:
  def __init__(self):
    self.connections = {}

  def add_dendrite(self, neuron, dendrite):
    if neuron not in self.connections:
      self.connections[neuron.id] = []
    self.connections[neuron.id].append(dendrite)

  def activate(self, time):
    for connections in self.connections.values():
      for dendrite in connections:
        dendrite.activate(time)


class Neuron:
  def __init__(self):
    self.dendrites = []
    self.axon = Axon()
    self.id = uuid.uuid4()

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

  def activate(self, time):
    activation_time = 0.01
    self.axon.activate(time + activation_time)


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
    print_conections(s.connections, f"sensor {i} ")


def main():
  sensor_1 = Sensor()
  sensor_2 = Sensor()
  sensor_3 = Sensor()

  neuron_1_1 = Neuron()
  neuron_1_1.add_input(sensor_1)
  neuron_1_2 = Neuron()
  neuron_1_2.add_input(sensor_2)
  neuron_1_3 = Neuron()
  neuron_1_3.add_input(sensor_3)

  neuron_2_1 = Neuron()
  neuron_2_1.add_connection(neuron_1_1)
  neuron_2_1.add_connection(neuron_1_2)
  neuron_2_2 = Neuron()
  neuron_2_2.add_connection(neuron_1_2)
  neuron_2_3 = Neuron()
  neuron_2_3.add_connection(neuron_1_3)
  neuron_2_3.add_connection(neuron_1_2)

  sensors = [sensor_1, sensor_2, sensor_3]
  print_network(sensors)
  # send input
  sensor_1.set_input(1)
  sensor_2.set_input(0)
  sensor_3.set_input(0)
  for s in sensors:
    s.activate()

  print("-------------")
  print_network(sensors)

if __name__ == "__main__":
  main()
