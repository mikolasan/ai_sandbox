from pyfinite import ffield
from neuron import Sensor, Neuron


def reed_solomon_encode(data, n, k):
    """
    Encode a list of integers using Reed-Solomon code.

    Args:
    data (list of int): The data to be encoded (0 to 255 integers). Length should be <= k.
    n (int): Total number of codewords (n - k is the number of parity codewords).
    k (int): Number of data codewords.

    Returns:
    list of int: The encoded codewords.
    """
    if len(data) > k:
        raise ValueError("Input data length should be less than or equal to k")

    # Create a finite field GF(256)
    gf = ffield.FField(8)

    # Initialize the generator polynomial for Reed-Solomon
    generator = []
    for i in range(n - k, n):
        generator.append(gf.exp(i))

    encoded_data = []

    # Iterate over the input data
    for i in data:
        term = [i]  # Start with the current data element
        for j in range(n - k):
            # Multiply by the generator polynomial
            term.append(gf.mul(i, generator[j]))
        encoded_data.extend(term)

    # If the input data was less than k, add zero-padding
    if len(data) < k:
        encoded_data.extend([0] * (k - len(data)))

    return encoded_data

# Example usage:
data = list(range(8))  # Numbers from 0 to 7, length <= k
n = 10  # Total codewords
k = 8   # Data codewords
encoded_data = reed_solomon_encode(data, n, k)
print(encoded_data)


def main():
  input = [-2, 3, -5, 1]
  output = [-2, 3, -5, 1, -18, 17]
  generator = [-1, -3, 2]

  sensor_1 = Sensor()
  # sensor_2 = Sensor()
  # sensor_3 = Sensor()
  # sensor_4 = Sensor()
  # sensors = [sensor_1, sensor_2, sensor_3, sensor_4]

  # neuron_1_1 = Neuron()
  # neuron_1_1.add_input(sensor_1)
  # neuron_1_2 = Neuron()
  # neuron_1_2.add_input(sensor_2)
  # neuron_1_3 = Neuron()
  # neuron_1_3.add_input(sensor_3)
  # neuron_1_4 = Neuron()
  # neuron_1_4.add_input(sensor_4)
  
  # neuron_2_1 = Neuron()
  # neuron_2_1.add_connection(neuron_1_1)
  # neuron_2_1.add_connection(neuron_1_2)
  # neuron_2_2 = Neuron()
  # neuron_2_2.add_connection(neuron_1_2)
  # neuron_2_3 = Neuron()
  # neuron_2_3.add_connection(neuron_1_3)
  # neuron_2_3.add_connection(neuron_1_2)

  neuron_1 = Neuron()
  neuron_1.add_input(sensor_1)
  neuron_2 = Neuron()
  neuron_2.add_connection(neuron_1)
  
  sensor_1.set_input(input[0])
  
  propagating = True
  activation_time = 0.0
  sensor_1.activate(activation_time)
  while propagating:
    activation_time += 0.1
    neuron_1.activate(activation_time)
    
  
  # print("-------------")
  # print("Signal path")
  # for i, sensor in enumerate(sensors):
  #   sensor.set_input(input[i])
  #   time = 0.0
  #   sensor.activate(time)

  # print("-------------")
  # print_network(sensors)


if __name__ == "__main__":
  main()
