# from pyfinite import ffield
from neuron import Sensor, Neuron, MultiplyingNeuron, RegisterNeuron
from scheduler import Scheduler


def main():
  scheduler = Scheduler()
  
  input = [-2, 3, -1, 10, -4]
  output = [-2, 3, -5, 1, -18, 17]
  generator = [-1, -3, 2]

  sensor_polynom = Sensor("polynom", scheduler)
  neuron_sum2 = Neuron("sum2", scheduler)
  neuron_sum2.add_input(sensor_polynom)
  neuron_negative = MultiplyingNeuron("negative", scheduler, -1.0)
  neuron_negative.add_connection(neuron_sum2, 1.0)
  
  neuron_g0 = MultiplyingNeuron("g0", scheduler, -1.0)
  neuron_g0.add_connection(neuron_negative, 1.0)
  neuron_g1 = MultiplyingNeuron("g1", scheduler, 2.0, activation_delay=1)
  neuron_g1.add_connection(neuron_negative, 1.0)
  neuron_g2 = MultiplyingNeuron("g2", scheduler, -3.0, activation_delay=3)
  neuron_g2.add_connection(neuron_negative, 1.0)
  
  neuron_r0 = RegisterNeuron("r0", scheduler)
  neuron_r1 = RegisterNeuron("r1", scheduler)
  neuron_r2 = RegisterNeuron("r2", scheduler)
  
  neuron_sum0 = Neuron("sum0", scheduler)
  neuron_sum0.add_connection(neuron_r0, 1.0)
  neuron_sum0.add_connection(neuron_g1, 1.0)
  neuron_sum1 = Neuron("sum1", scheduler)
  neuron_sum1.add_connection(neuron_r1, 1.0)
  neuron_sum1.add_connection(neuron_g2, 1.0)
  
  neuron_r0.add_connection(neuron_g0, 1.0)
  neuron_r1.add_connection(neuron_sum0, 1.0)
  neuron_r2.add_connection(neuron_sum1, 1.0)
  # neuron_sum2.add_connection(neuron_r2, 1.0)
  neuron_sum2.add_connection(neuron_sum1, 1.0)
  
  neuron_memory = Neuron("memory", scheduler)
  neuron_memory.add_connection(neuron_sum2, 1.0)
  
  sensor_polynom.set_input_sequence({
    0: -2,
    7: 3,
    14: -1,
    21: 10,
    28: -4
  })
  scheduler.start([sensor_polynom])
  

if __name__ == "__main__":
  main()
