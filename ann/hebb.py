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

from neuron import Sensor, Neuron, print_network

def main():
  sensor_1 = Sensor()
  sensor_2 = Sensor()
  sensor_3 = Sensor()
  sensors = [sensor_1, sensor_2, sensor_3]

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

  print_network(sensors)
  # send input
  sensor_1.set_input(1)
  sensor_2.set_input(0)
  sensor_3.set_input(0)
  print("-------------")
  print("Signal path")
  for sensor in sensors:
    time = 0.0
    sensor.activate(time)

  print("-------------")
  print_network(sensors)

if __name__ == "__main__":
  main()
