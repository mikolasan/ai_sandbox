#include <iostream>
#include <filesystem>
#include <fstream>

#include <json.hpp>
using json = nlohmann::json;

#include "arc.h"
#include "math.h"
#include "neuron.h"

int main(int argc, char const *argv[])
{
  std::filesystem::path file_path = "data";
  file_path /= "training";
  file_path /= "0a938d79.json";
  std::ifstream f(file_path);
  json data = json::parse(f);

  auto train_data = data["train"];
  int example_id = 0;
  std::vector<Example> training_data;
  for (const auto& example : train_data) {
    // std::cout << "Example id: " << example_id << std::endl;
    // std::cout << "Input" << std::endl;
    auto input_matrix = example["input"];
    Array2D input;
    input.reserve(input_matrix.size());
    for (const auto& input_row : input_matrix) {
      std::vector<int> row;
      row.assign(input_row.begin(), input_row.end());
      input.emplace_back(row);
      // for (auto& x : row) {
      //   std::cout << color_map[x] << " ";
      // }
      // std::cout << std::endl;
    }
    
    // std::cout << "Output" << std::endl;
    auto output_matrix = example["output"];
    Array2D output;
    output.reserve(output_matrix.size());
    for (const auto& output_row : output_matrix) {
      std::vector<int> row;
      row.assign(output_row.begin(), output_row.end());
      output.emplace_back(row);
      // for (auto& x : row) {
      //   std::cout << color_map[x] << " ";
      // }
      // std::cout << std::endl;
    }

    ++example_id;
    training_data.emplace_back(input, output);
  }

  create_network(training_data);

  //std::vector<Example> testing;
  //auto test_data = data["test"];
  return 0;
}
