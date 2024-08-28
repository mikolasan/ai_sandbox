#include <iostream>
#include <memory>

#include "arc.h"
#include "neuron.h"
#include "scheduler.h"
#include "task.h"

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
        auto sensor = std::make_shared<Sensor>();
        sensors.emplace_back(sensor);
        sensor->value = value;
        sensor->pos = std::make_tuple(x, y);

        scheduler->add_task(std::make_shared<SensorSpikeTrainTask>(sensor)); // -> sensor->fire();

        // better ?
        // scheduler->add_task([sensor](){ sensor->fire(); });
      }
    }

    for (size_t y = 0; y < output.size(); ++y) {
      for (size_t x = 0; x < output[y].size(); ++x) {
        int value = output[y][x];
        auto sensor = std::make_shared<Sensor>();
        sensors.emplace_back(sensor);
        sensor->value = value;
        sensor->pos = std::make_tuple(x, y);
      }
    }
    
    // std::cout << "Input" << std::endl;
    for (const auto& row : input) {
      for (auto& x : row) {
        std::cout << color_map[x] << " ";
      }
      std::cout << std::endl;
    }
    // std::cout << "Output" << std::endl;
    for (const auto& row : output) {
      for (auto& x : row) {
        std::cout << color_map[x] << " ";
      }
      std::cout << std::endl;
    }
  }

  std::cout << "Expanding the network" << std::endl;

  
  
  scheduler->main_loop();
  // for (/* every second*/) {
    for (const auto& sensor : sensors) {
      sensor->fire();
    }
  // }

}

void Sensor::fire() {

}