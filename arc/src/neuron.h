#include <list>
#include <memory>
#include <tuple>
#include <vector>

#include "math.h"

using SpatialPosition = std::tuple<int, int>;

struct Neuron;

struct Sensor {
  int _value;
  SpatialPosition _pos;
  std::list<std::shared_ptr<Neuron>> dendrite_connections;

  Sensor(int value, SpatialPosition pos) :
    _value(value),
    _pos(pos)
  {}
  void fire();
};

struct Neuron {
  Neuron(SpatialPosition pos) :
    _pos(pos)
  {}
  void receive_signal(int intensity);

  std::unique_ptr<Sensor> sensor;
  std::vector<std::weak_ptr<Neuron>> dendrites;
  std::weak_ptr<Neuron> axon;

  int potential;
  SpatialPosition _pos;
};

void create_network(const std::vector<Example>& training_data);