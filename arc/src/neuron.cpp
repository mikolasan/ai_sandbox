#include <iostream>

#include "arc.h"
#include "neuron.h"

void create_network(const std::vector<Example>& training_data) {
  std::vector<std::shared_ptr<Sensor>> sensors;
  std::vector<std::weak_ptr<Neuron>> network;

  for (const auto& [input, output] : training_data) {
    
    // std::cout << "Input" << std::endl;
    // for (const auto& row : input) {
    //   for (auto& x : row) {
    //     std::cout << color_map[x] << " ";
    //   }
    //   std::cout << std::endl;
    // }
    // std::cout << "Output" << std::endl;
    // for (const auto& row : output) {
    //   for (auto& x : row) {
    //     std::cout << color_map[x] << " ";
    //   }
    //   std::cout << std::endl;
    // }
  }
}