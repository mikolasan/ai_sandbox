# from pyfinite import ffield
from neuron import Sensor, Neuron
from scheduler import Scheduler


def main():
  scheduler = Scheduler()
  
  input = [-2, 3, -5, 1]
  output = [-2, 3, -5, 1, -18, 17]
  generator = [-1, -3, 2]

  sensor_1 = Sensor(scheduler)
  neuron_1 = Neuron(scheduler)
  neuron_1.add_input(sensor_1)
  neuron_2 = Neuron(scheduler)
  neuron_2.add_connection(neuron_1, 1.0)
  
  sensor_1.set_input(input[0])
  scheduler.start([sensor_1])
  

if __name__ == "__main__":
  main()
