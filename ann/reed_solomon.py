# from pyfinite import ffield
from neuron import Sensor, Neuron, MultiplyingNeuron
from scheduler import Scheduler


def main():
  scheduler = Scheduler()
  
  input = [-2, 3, -5, 1]
  output = [-2, 3, -5, 1, -18, 17]
  generator = [-1, -3, 2]

  sensor_polynom = Sensor(scheduler)
  neuron_sum2 = Neuron(scheduler)
  neuron_sum2.add_input(sensor_polynom)
  neuron_negative = MultiplyingNeuron(scheduler, -1.0)
  neuron_negative.add_connection(neuron_sum2, 1.0)
  
  neuron_g0 = MultiplyingNeuron(scheduler, -1.0)
  neuron_g0.add_connection(neuron_negative, 1.0)
  neuron_g1 = MultiplyingNeuron(scheduler, 2.0)
  neuron_g1.add_connection(neuron_negative, 1.0)
  neuron_g2 = MultiplyingNeuron(scheduler, -3.0)
  neuron_g2.add_connection(neuron_negative, 1.0)
  
  neuron_r0 = MultiplyingNeuron(scheduler, 0.0)
  neuron_r1 = MultiplyingNeuron(scheduler, 0.0)
  neuron_r2 = MultiplyingNeuron(scheduler, 0.0)
  
  neuron_sum0 = Neuron(scheduler)
  neuron_sum0.add_connection(neuron_r0, 1.0)
  neuron_sum0.add_connection(neuron_g1, 1.0)
  neuron_sum1 = Neuron(scheduler)
  neuron_sum1.add_connection(neuron_r1, 1.0)
  neuron_sum1.add_connection(neuron_g2, 1.0)
  
  neuron_r0.add_connection(neuron_g0, 1.0)
  neuron_r1.add_connection(neuron_sum0, 1.0)
  neuron_r2.add_connection(neuron_sum1, 1.0)
  neuron_sum2.add_connection(neuron_r2, 1.0)
  
  sensor_polynom.set_input(input[0])
  scheduler.start([sensor_polynom])
  

if __name__ == "__main__":
  main()
