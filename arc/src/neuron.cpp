#include <iostream>
#include <memory>

#include "arc.h"
#include "neuron.h"
#include "scheduler.h"
#include "task.h"

constexpr int squared_distance(SpatialPosition a, SpatialPosition b) {
  auto [ax, ay] = a;
  auto [bx, by] = b;
  return (bx - ax) * (bx - ax) + (by - ay) * (by - ay);
}

void Sensor::fire() {
  // for already connected neurons
  int spent = 0;
  for (auto& neuron : dendrite_connections) {
    neuron->receive_signal(_value);
    ++spent;
  }
  if (spent >= _value) {
    return;
  }


  // find near neurons that are not connected yet
  // or create new neurons

  auto neuron = std::make_shared<Neuron>(_pos);
}

void Neuron::receive_signal(int intensity) {
  potential += intensity;
}

class SensorSpikeTrainTask : public Task {
public:
  SensorSpikeTrainTask(const std::shared_ptr<Sensor>& sensor) :
    _sensor(sensor)
  {}

  void run() {
    _sensor->fire();
  }
private:
  std::shared_ptr<Sensor> _sensor;
};

void create_network(const std::vector<Example>& training_data) {
  std::vector<std::shared_ptr<Sensor>> sensors;
  std::vector<std::weak_ptr<Neuron>> network;

  std::unique_ptr<Scheduler> scheduler = std::make_unique<Scheduler>();

  std::cout << "Creating the network sensors" << std::endl;

  for (const auto& [input, output] : training_data) {
    
    
    for (size_t y = 0; y < input.size(); ++y) {
      for (size_t x = 0; x < input[y].size(); ++x) {
        int value = input[y][x];
        auto [red, green, blue] = value_to_saturations_map[value];
        auto pos = std::make_tuple(x, y);
        auto sensor_red = std::make_shared<Sensor>(red, pos);
        auto sensor_green = std::make_shared<Sensor>(green, pos);
        auto sensor_blue = std::make_shared<Sensor>(blue, pos);
        // sensors.emplace_back(sensor);

        scheduler->add_task(std::make_shared<SensorSpikeTrainTask>(sensor_red)); // -> sensor->fire();
        scheduler->add_task(std::make_shared<SensorSpikeTrainTask>(sensor_green));
        scheduler->add_task(std::make_shared<SensorSpikeTrainTask>(sensor_blue));

        // better ?
        // scheduler->add_task([sensor](){ sensor->fire(); });
      }
    }

    // for (size_t y = 0; y < output.size(); ++y) {
    //   for (size_t x = 0; x < output[y].size(); ++x) {
    //     int value = output[y][x];
    //     auto [red, green, blue] = value_to_saturations_map[value];
    //     auto pos = std::make_tuple(x, y);
    //     auto sensor_red = std::make_shared<Sensor>(red, pos);
    //     auto sensor_green = std::make_shared<Sensor>(green, pos);
    //     auto sensor_blue = std::make_shared<Sensor>(blue, pos);
    //     // sensors.emplace_back(sensor);

    //     scheduler->add_task(std::make_shared<SensorSpikeTrainTask>(sensor_red)); // -> sensor->fire();
    //     scheduler->add_task(std::make_shared<SensorSpikeTrainTask>(sensor_green));
    //     scheduler->add_task(std::make_shared<SensorSpikeTrainTask>(sensor_blue));
    //   }
    // }
    
    // // std::cout << "Input" << std::endl;
    // for (const auto& row : input) {
    //   for (auto& x : row) {
    //     std::cout << color_map[x] << " ";
    //   }
    //   std::cout << std::endl;
    // }
    // // std::cout << "Output" << std::endl;
    // for (const auto& row : output) {
    //   for (auto& x : row) {
    //     std::cout << color_map[x] << " ";
    //   }
    //   std::cout << std::endl;
    // }
  }

  std::cout << "Created " << scheduler->get_size() << " sensors" << std::endl;
  std::cout << "Expanding the network" << std::endl;

  scheduler->main_loop();
}

