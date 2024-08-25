#include <memory>
#include <tuple>
#include <vector>

#include "math.h"

struct Sensor {
  int value;
  std::tuple<int, int> pos;
};

struct Neuron {
  std::unique_ptr<Sensor> sensor;
  std::vector<std::weak_ptr<Neuron>> dendrites;
  std::weak_ptr<Neuron> axon;
};

void create_network(const Array2D& input, const Array2D& output);