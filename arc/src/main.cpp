#include <iostream>
#include <filesystem>
#include <fstream>

#include "arc.h"
#include "math.h"
#include "neuron.h"

int main(int argc, char const *argv[])
{
  
  auto training_data = read_training_data("0a938d79");
  create_network(training_data);

  //std::vector<Example> testing;
  //auto test_data = data["test"];
  return 0;
}
