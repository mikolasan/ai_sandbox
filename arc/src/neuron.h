#include <memory>
#include <tuple>
#include <vector>

#include "math.h"

struct Sensor {
  int value;
  std::tuple<int, int> pos;

  void fire();
};

struct Neuron {
  std::unique_ptr<Sensor> sensor;
  std::vector<std::weak_ptr<Neuron>> dendrites;
  std::weak_ptr<Neuron> axon;
};

void create_network(const std::vector<Example>& training_data);